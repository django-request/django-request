from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("request", "0005_alter_request_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="request",
            name="method",
            field=models.CharField(default="GET", max_length=7, verbose_name="method"),
        ),
    ]
