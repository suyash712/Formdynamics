# Generated by Django 4.2.3 on 2024-01-10 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='salesorder1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salesorder_id', models.CharField(max_length=200)),
                ('zcrm_potential_id', models.CharField(max_length=200)),
            ],
        ),
    ]