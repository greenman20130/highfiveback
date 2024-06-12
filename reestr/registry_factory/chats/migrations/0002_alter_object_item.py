from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='Chat'.lower(),
            name='object_item',
            field=models.UUIDField(default=None, null=True),
        ),
    ]
