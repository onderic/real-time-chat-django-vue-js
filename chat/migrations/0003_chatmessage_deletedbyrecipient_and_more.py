# Generated by Django 4.2.2 on 2023-06-20 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_alter_chatmessage_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='deletedByRecipient',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='deletedBySender',
            field=models.BooleanField(default=False),
        ),
    ]
