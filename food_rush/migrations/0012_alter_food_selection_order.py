# Generated by Django 4.2.20 on 2025-04-25 02:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('food_rush', '0011_alter_customer_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food_selection',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='selections', to='food_rush.order'),
        ),
    ]
