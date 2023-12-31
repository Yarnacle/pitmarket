# Generated by Django 4.0.4 on 2022-06-03 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='page',
            old_name='bodytext',
            new_name='content',
        ),
        migrations.RemoveField(
            model_name='page',
            name='update_date',
        ),
        migrations.AlterField(
            model_name='page',
            name='permalink',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
