from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("attendance", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="student",
            name="face_image",
        ),
    ]
