# Generated by Django 2.2 on 2021-03-04 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_app', '0016_delete_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(default='', upload_to='images'),
            preserve_default=False,
        ),
    ]
