# Generated by Django 3.1.7 on 2021-03-30 04:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_app', '0005_message_item_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='item_message',
        ),
    ]
