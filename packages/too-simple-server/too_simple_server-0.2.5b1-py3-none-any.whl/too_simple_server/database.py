from typing import List
from uuid import uuid4

from peewee import DatabaseProxy, Model, PostgresqlDatabase, SqliteDatabase, TextField, UUIDField
from psycopg2 import connect
from psycopg2.errors import DuplicateDatabase
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from .configuration import Configuration, EntityStruct, _IN_USER_DIR, _try_dir

DB = DatabaseProxy()


class BaseModel(Model):
    class Meta:
        database = DB


class Entity(BaseModel):
    """Some stub entity"""

    uuid = UUIDField()
    data = TextField()


def _create_psql_database(db_name, user, password, host, port):
    conn = connect(dbname="postgres", user=user, password=password, host=host, port=port)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    try:
        cursor.execute(f"create database {db_name}")
    except DuplicateDatabase:
        pass
    cursor.close()
    conn.close()


def init_db(configuration: Configuration):
    if configuration.debug:
        local_dir = _try_dir("/opt/too-simple", _IN_USER_DIR)
        database = SqliteDatabase(f"{local_dir}/debug.db")
    else:

        host, port = configuration.pg_db_url.split(":")
        connection_kwargs = dict(host=host,
                                 port=port,
                                 user=configuration.pg_username,
                                 password=configuration.pg_password)
        _create_psql_database(configuration.pg_database, **connection_kwargs)
        database = PostgresqlDatabase(configuration.pg_database, **connection_kwargs)

    DB.initialize(database)
    if not database.table_exists(Entity.__name__):
        database.create_tables([Entity])
        database.commit()


@DB.atomic()
def create_entity(data: dict) -> str:
    """Create new entity returning uuid of created record"""
    new_uuid = str(uuid4())
    Entity.create(uuid=new_uuid, data=data["data"])
    return new_uuid


def get_entity_data(uuid: str) -> dict:
    entity: Entity = Entity.get(uuid=uuid)
    return EntityStruct(entity.uuid, entity.data)._asdict()


def get_all_entities() -> List[dict]:
    all_ent = Entity.select()
    return [EntityStruct(uuid=str(ent.uuid), data=ent.data)._asdict() for ent in all_ent]
