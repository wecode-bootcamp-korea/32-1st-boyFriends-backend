# Generated by Django 4.0.4 on 2022-04-28 05:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0005_alter_ordershipment_delivery_company'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DeliveryCompany',
            new_name='Carrier',
        ),
        migrations.RenameField(
            model_name='carrier',
            old_name='company',
            new_name='carriers',
        ),
        migrations.RenameField(
            model_name='ordershipment',
            old_name='delivery_company',
            new_name='carrier',
        ),
        migrations.AlterModelTable(
            name='carrier',
            table='carriers',
        ),
    ]