# Generated by Django 3.2 on 2021-09-09 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymActivities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityObservers',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'Activity_observers',
                'managed': False,
            },
        ),
    ]