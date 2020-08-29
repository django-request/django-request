from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0004_alter_time_timezone_default'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]
