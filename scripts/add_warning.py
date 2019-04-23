from apps.schema.models import Database
from scripts.check import CommentParser

from xlibs.db import DB


def run(db_list, t_list):
    db_name_list = db_list.split(',')
    if len(db_name_list) == 1 and db_name_list[0] == '':
        databases = Database.objects.filter(enable=True)
    else:
        databases = Database.objects.filter(enable=True, name__in=db_name_list)

    for database in databases:
        t_name_list = t_list.split(',')
        if len(t_name_list) == 1 and t_name_list[0] == '':
            tables = database.table_set.all()
        else:
            tables = database.table_set.filter(name__in=t_name_list)
            if not tables:
                tables = database.table_set.all()

        db = DB(database.config)
        for table in tables:

            for column in table.column_set.all():
                # skip column which is dirty
                if column.is_comment_dirty:
                    comment_enums = CommentParser.get_enums(column.comment or '')
                    try:
                        tb = getattr(db, table.name)
                    except Exception:
                        continue
                    real_enums = [str(getattr(row, column.name)) for row in tb.group_by(column.name).all()]
                    no_match_enums = (set(real_enums) - set(comment_enums))
                    print real_enums, comment_enums
                    warning = ','.join(no_match_enums)
                    column.other_enums = warning
                    column.save()



