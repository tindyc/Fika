# Generated by Django 4.0.4 on 2022-05-23 04:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_remove_eventpost_country_remove_eventpost_county_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventpost',
            old_name='author',
            new_name='user',
        ),
    ]
