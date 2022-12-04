from django.db import migrations, models, connection
from django.db.migrations import RunPython


def do(_, __):
    with open('./course_work/sql/create_procedures.sql') as f:
        script = f.read()
        with connection.cursor() as cursor:
            cursor.execute(script)


def undo(_, __):
    with open('./course_work/sql/drop_procedures.sql') as f:
        script = f.read()
        with connection.cursor() as cursor:
            cursor.execute(script)


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        RunPython(do, reverse_code=undo)
    ]
