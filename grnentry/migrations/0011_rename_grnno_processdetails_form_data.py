# Generated by Django 4.2.3 on 2024-04-12 16:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grnentry', '0010_rename_form_data_processdetails_grnno'),
    ]

    operations = [
        migrations.RenameField(
            model_name='processdetails',
            old_name='GRNNO',
            new_name='form_data',
        ),
    ]