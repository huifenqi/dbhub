from django.conf import settings
from sqlalchemy import create_engine, inspect
from sqlalchemy import MetaData

from apps.schema.models import Database, Table, Column, Index


def build(database):
    engine = create_engine(database.config)
    m = MetaData()
    m.reflect(engine)
    # fill database info
    if not database.charset:
        database.charset = engine.dialect.encoding
        database.save()
    for table in m.sorted_tables:
        print 'table: {}'.format(table.name)
        dialect = database.config.split(':')[0]
        table_info = table.dialect_options[dialect]._non_defaults
        t, created = Table.objects.get_or_create(database=database, name=table.name)
        t.engine = table_info.get('engine', '')
        t.charset = table_info.get('default charset', '')
        if not t.comment and table.comment:
            t.comment = table.comment
        t.save()
        for column in table.columns:
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
        for index in table.primary_key.columns:
            i, created = Index.objects.get_or_create(table=t, name=index.name)
            i.type = 'PRIMARY KEY'
            i.include_columns = index.name
            i.save()
        for index in table.indexes:
            i, created = Index.objects.get_or_create(table=t, name=index.name)
            i.type = 'UNIQUE KEY' if index.unique else 'KEY'
            i.include_columns = ', '.join([c.name for c in index.columns])
            i.save()


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
        build(database)


if __name__ == '__main__':
    run()
