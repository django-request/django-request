from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0006_alter_request_method_default'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='is_ajax',
            field=models.BooleanField(
                default=False,
                help_text='Whether this request was used via JavaScript.',
                verbose_name='is ajax',
            ),
        ),
    ]
