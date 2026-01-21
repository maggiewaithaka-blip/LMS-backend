from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0008_scormpackage_section"),
    ]
    operations = [
        migrations.RemoveField(
            model_name="scormpackage",
            name="extracted_path",
        ),
    ]
