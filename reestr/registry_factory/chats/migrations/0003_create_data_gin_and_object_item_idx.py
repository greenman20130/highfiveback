import django.contrib.postgres.indexes
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0002_alter_object_item'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='Chat'.lower(),
            index=django.contrib.postgres.indexes.GinIndex(fields=['data'], name='chats_data_gin'),
        ),
        migrations.AddIndex(
            model_name='Chat'.lower(),
            index=models.Index(fields=['object_item'], name='chats_object_item_idx'),
        ),
    ]
