# Generated by Django 2.1.8 on 2019-12-13 00:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0003_auto_20191213_0045'),
        ('courses', '0002_auto_20191211_0011'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_org',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='organizations.CourseOrg', verbose_name='课程机构'),
        ),
    ]
