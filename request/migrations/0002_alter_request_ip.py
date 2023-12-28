from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("request", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="request",
            name="ip",
            field=models.GenericIPAddressField(verbose_name="ip address"),
        ),
    ]
