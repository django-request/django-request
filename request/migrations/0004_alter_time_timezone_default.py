import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("request", "0003_auto_20160331_1430"),
    ]

    operations = [
        migrations.AlterField(
            model_name="request",
            name="time",
            field=models.DateTimeField(
                db_index=True, default=django.utils.timezone.now, verbose_name="time"
            ),
        ),
    ]
