# Generated by Django 4.2.3 on 2024-04-23 19:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grnentry', '0022_inventory'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grnentry1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grnentry_GRNNO', models.CharField(max_length=200)),
                ('grnentry_MATERIALDESCRIPTION', models.TextField(max_length=200)),
                ('grnentry_MATERIALGRADE', models.CharField(choices=[('EN8', 'EN8'), ('EN9', 'EN9'), ('EN24', 'EN24'), ('EN1A', 'EN1A'), ('ALU T6 6082', 'ALU T6 6082'), ('ALU T6 5082', 'ALU T6 5082'), ('SS 316', 'SS 316'), ('SS 304', 'SS 304'), ('MS', 'MS')], max_length=20)),
                ('grnentry_QUANTITYTYPE', models.CharField(choices=[('KG', 'KG'), ('NO', "NO'S")], max_length=200)),
                ('grnentry_NOQUANTITY', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('grnentry_DATETIME', models.DateTimeField(auto_now_add=True, max_length=200)),
                ('grnentry_STOREOWNER', models.CharField(choices=[('YOGESH_PALKAR', 'YOGESH PALKAR'), ('PRANAV_PATIL', 'PRANAV PATIL'), ('SHUBHAM_BHALERAO', 'SHUBHAM BHALERAO')], max_length=200)),
                ('grnentry_ORDERTYPE', models.CharField(choices=[('WITH_MATERIAL', 'With Material'), ('JOB_WORK', 'Job Work')], max_length=200)),
                ('grnentry_PONO', models.CharField(max_length=200)),
                ('grnentry_CHALLANNO', models.CharField(max_length=200)),
                ('grnentry_COMMENTS', models.TextField(max_length=200)),
                ('grnentry_SONO', models.CharField(max_length=200)),
                ('grnentry_PARTNAME', models.CharField(max_length=200)),
                ('grnentry_DRAWINGNO', models.CharField(max_length=200)),
                ('grnentry_EXPTIME', models.DateTimeField(max_length=200)),
            ],
        ),
    ]
