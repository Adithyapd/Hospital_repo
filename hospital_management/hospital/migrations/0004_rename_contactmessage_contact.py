# Generated by Django 5.0.1 on 2024-05-24 04:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0003_contactmessage'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ContactMessage',
            new_name='Contact',
        ),
    ]
