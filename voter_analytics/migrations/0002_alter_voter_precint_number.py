# Generated by Django 5.1.5 on 2025-04-03 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("voter_analytics", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="voter",
            name="precint_number",
            field=models.TextField(),
        ),
    ]
