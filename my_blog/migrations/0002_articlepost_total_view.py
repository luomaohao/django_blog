# Generated by Django 2.1 on 2020-01-04 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepost',
            name='total_view',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
