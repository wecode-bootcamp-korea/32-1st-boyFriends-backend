# Generated by Django 4.0.4 on 2022-04-27 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_address_alter_user_age_alter_user_gender_and_more'),
        ('products', '0004_productstatus_rename_sale_product_discount_and_more'),
        ('payments', '0002_remove_order_order_number_alter_cart_count_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='id',
            new_name='order_number',
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.order'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product'),
        ),
    ]
