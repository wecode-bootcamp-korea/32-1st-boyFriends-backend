# Generated by Django 4.0.4 on 2022-05-03 08:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_image_category'),
        ('payments', '0007_cart_check_box'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='option',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='products.size'),
        ),
    ]
