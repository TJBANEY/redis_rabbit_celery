# Generated by Django 2.0.2 on 2018-03-10 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wikipedia', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wikipediapage',
            name='scanned',
        ),
        migrations.AddField(
            model_name='wikipediapage',
            name='scanned_status',
            field=models.CharField(choices=[('I', 'Idle'), ('P', 'In Progress'), ('S', 'Scanned')], default='I', max_length=20),
        ),
    ]