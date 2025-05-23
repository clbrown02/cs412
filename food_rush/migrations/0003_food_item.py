# Generated by Django 5.1.5 on 2025-04-16 06:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("food_rush", "0002_restaurant"),
    ]

    operations = [
        migrations.CreateModel(
            name="Food_item",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=5)),
                ("description", models.TextField()),
                (
                    "restaurant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="food_rush.restaurant",
                    ),
                ),
            ],
        ),
    ]
