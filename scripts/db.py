from sqlalchemy import create_engine
from sqlalchemy import MetaData

from apps.schema.models import Database, Table, Column, Index


def run():
    engine = create_engine('mysql://***REMOVED***:3306/huizhaofang')
    m = MetaData()
    m.reflect(engine)
    for table in m.tables.values():
        print dir(table)
        print table.name
        print table.comment
        for column in table.c:
            print(column.name)
            print(column.comment)
        break


if __name__ == '__main__':
    run()
