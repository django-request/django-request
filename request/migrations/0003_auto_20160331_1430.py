from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0002_alter_request_ip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='time', db_index=True),
        ),
    ]
