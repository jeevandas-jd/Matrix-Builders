# Generated by Django 5.1.2 on 2024-10-19 10:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("skills", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="skillexchange",
            name="is_paid_service",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="skillexchange",
            name="price",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=6, null=True
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="hourly_rate",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=6, null=True
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="is_professional",
            field=models.BooleanField(default=False),
        ),
    ]
