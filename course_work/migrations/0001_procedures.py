from django.db import connection
from django.db import migrations
from django.db.migrations import RunPython


def do(_, __):
    for script_path in ['./course_work/sql/create_procedures.sql', './course_work/sql/fill_data.sql']:
        with open(script_path) as f:
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
