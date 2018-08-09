from sqlalchemy import create_engine
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


def run():
    databases = Database.objects.all()
    for database in databases:
        build(database)


if __name__ == '__main__':
    run()
