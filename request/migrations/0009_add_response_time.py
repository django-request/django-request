from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0008_alter_request_response_choices'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='response_time',
            field=models.FloatField(null=True, verbose_name='response_time'),
        ),
    ]
