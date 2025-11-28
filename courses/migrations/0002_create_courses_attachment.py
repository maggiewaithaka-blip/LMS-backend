from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE TABLE IF NOT EXISTS courses_attachment (
                id BIGSERIAL PRIMARY KEY,
                assignment_id BIGINT REFERENCES courses_assignment(id) ON DELETE CASCADE,
                quiz_id BIGINT REFERENCES courses_quiz(id) ON DELETE CASCADE,
                resource_id BIGINT REFERENCES courses_resource(id) ON DELETE CASCADE,
                type VARCHAR(50) NOT NULL DEFAULT 'file',
                file VARCHAR(1000),
                url VARCHAR(2000),
                text TEXT
            );
            """,
            reverse_sql="DROP TABLE IF EXISTS courses_attachment;"
        ),
    ]
