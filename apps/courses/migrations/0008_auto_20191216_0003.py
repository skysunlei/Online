# Generated by Django 2.1.8 on 2019-12-16 00:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_auto_20191216_0002'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coursetag',
            old_name='name',
            new_name='tag',
        ),
    ]
