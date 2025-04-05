from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        # replace with the actual previous migration
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql="CREATE EXTENSION IF NOT EXISTS hstore;",
            reverse_sql="DROP EXTENSION IF EXISTS hstore;",
        ),
    ]
