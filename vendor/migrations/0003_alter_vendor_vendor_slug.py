# Generated by Django 5.1.4 on 2024-12-26 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vendor", "0002_vendor_vendor_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vendor",
            name="vendor_slug",
            field=models.SlugField(max_length=100, unique=True),
        ),
    ]