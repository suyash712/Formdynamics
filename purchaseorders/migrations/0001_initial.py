# Generated by Django 4.2.3 on 2023-12-19 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='apipurchaseorder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchaseorder_id', models.CharField(max_length=200)),
                ('vendor_id', models.CharField(max_length=200)),
                ('vendor_name', models.CharField(max_length=200)),
                ('company_name', models.CharField(max_length=200)),
                ('order_status', models.CharField(max_length=200)),
                ('billed_status', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=200)),
                ('color_code', models.CharField(max_length=200)),
                ('current_sub_status_id', models.CharField(max_length=200)),
                ('current_sub_status', models.CharField(max_length=200)),
                ('purchaseorder_number', models.CharField(max_length=200)),
                ('reference_number', models.CharField(max_length=200)),
                ('date', models.CharField(max_length=200)),
                ('delivery_date', models.CharField(max_length=200)),
                ('delivery_days', models.CharField(max_length=200)),
                ('due_by_days', models.CharField(max_length=200)),
                ('due_in_days', models.CharField(max_length=200)),
                ('currency_id', models.CharField(max_length=200)),
                ('currency_code', models.CharField(max_length=200)),
                ('price_precision', models.CharField(max_length=200)),
                ('total', models.IntegerField()),
                ('has_attachment', models.BooleanField()),
                ('created_time', models.CharField(max_length=200)),
                ('last_modified_time', models.CharField(max_length=200)),
                ('quantity_yet_to_receive', models.IntegerField()),
                ('quantity_marked_as_received', models.IntegerField()),
                ('receives', models.CharField(max_length=200)),
                ('client_viewed_time', models.CharField(max_length=200)),
                ('is_viewed_by_client', models.BooleanField()),
                ('branch_id', models.CharField(max_length=200)),
                ('branch_name', models.CharField(max_length=200)),
            ],
        ),
    ]
