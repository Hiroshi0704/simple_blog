# Generated by Django 2.2.4 on 2019-10-10 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20190930_0734'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-create_at']},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-create_at']},
        ),
    ]
