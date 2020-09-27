import pymongo
from django.conf import settings
from sqlalchemy import create_engine, inspect
from sqlalchemy import MetaData
from pymongo_schema.extract import extract_pymongo_client_schema
from pymongo_schema.tosql import mongo_schema_to_mapping

from apps.schema.models import Database, Table, Column, Index


class RelationalDBSync(object):
    @staticmethod
    def save_indexes(t, indexes):
        for index in indexes:
            i, created = Index.objects.get_or_create(table=t, name=index.name)
            i.type = 'UNIQUE KEY' if index.unique else 'KEY'
            i.include_columns = ', '.join([c.name for c in index.columns])
            i.save()

    @staticmethod
    def save_primary_keys(t, primary_keys):
        for index in primary_keys:
            i, created = Index.objects.get_or_create(table=t, name=index.name)
            i.type = 'PRIMARY KEY'
            i.include_columns = index.name
            i.save()

    @staticmethod
    def save_columns(t, columns):
        for column in columns:
            default_value = column.server_default.arg if column.server_default else None
            c, created = Column.objects.get_or_create(table=t, name=column.name)
            try:
                c.data_type = str(column.type)
            except Exception:
                c.data_type = repr(column.type)
            c.is_null = column.nullable
            c.default_value = default_value
            if not c.comment and column.comment:
                c.comment = column.comment
            c.save()

    def build(self, database):
        engine = create_engine(database.config)
        m = MetaData()
        m.reflect(engine)
        if not database.charset:
            # fill database info
            database.charset = engine.dialect.encoding
            database.save()
        for table in m.sorted_tables:
            print(table.name)
            dialect = database.config.split(':')[0]
            table_info = table.dialect_options[dialect]._non_defaults
            t, created = Table.objects.get_or_create(database=database, name=table.name)
            t.engine = table_info.get('engine', '')
            t.charset = table_info.get('default charset', '')
            if not t.comment and table.comment:
                t.comment = table.comment
            t.save()
            self.save_columns(t, table.columns)
            self.save_primary_keys(t, table.primary_key.columns)
            self.save_indexes(t, table.indexes)


class MongoDBSync(object):
    def __init__(self, database):
        self.database = database
        parts1 = database.config.rsplit(':', 1)
        parts2 = parts1[1].split('/')
        self.host = parts1[0]
        self.port = int(parts2[0])
        self.db = parts2[1]

    def build(self):
        with pymongo.MongoClient(self.host, self.port) as client:
            for collection in client[self.db].list_collection_names():
                print(collection)
                schema = extract_pymongo_client_schema(client, [self.db], [collection])
                mapping = mongo_schema_to_mapping(schema)
                t, created = Table.objects.get_or_create(database=self.database, name=collection)
                for column in mapping[self.db][collection].keys():
                    if column == 'pk':
                        continue
                    c, created = Column.objects.get_or_create(table=t, name=column)
                    c.data_type = mapping[self.db][collection][column]['type']
                    c.is_null = None
                    c.default_value = None
                    c.comment = ''
                    c.save()


def init_databases():
    for instance in settings.DB_INSTANCES:
        engine = create_engine(instance)
        insp = inspect(engine)
        db_list = insp.get_schema_names()
        dbs = set(db_list) - {'information_schema', 'performance_schema', 'mysql', 'sys'}
        for db in dbs:
            config = '{}/{}?charset=utf8'.format(instance.rstrip('/'), db)
            d, created = Database.objects.get_or_create(name=db)
            d.config = config
            d.save()


def run():
    init_databases()
    databases = Database.objects.filter(enable=True)
    for database in databases:
        try:
            if database.config.startswith('mongodb'):
                MongoDBSync(database).build()
            else:
                RelationalDBSync().build(database)
        except Exception, e:
            print('ERROR: {}'.format(database.name))
            print(e)


if __name__ == '__main__':
    run()
