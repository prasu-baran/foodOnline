import uuid
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def populate_referral_codes(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    for user in User.objects.all():
        code = str(uuid.uuid4())[:8].upper()
        while User.objects.filter(referral_code=code).exists():
            code = str(uuid.uuid4())[:8].upper()
        user.referral_code = code
        user.save(update_fields=['referral_code'])


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_remove_userprofile_address_line_1_and_more"),
    ]

    operations = [
        # First add the field without unique constraint and allow blank
        migrations.AddField(
            model_name="user",
            name="referral_code",
            field=models.CharField(blank=True, max_length=20, default=''),
        ),
        # Populate unique codes for existing users
        migrations.RunPython(populate_referral_codes, migrations.RunPython.noop),
        # Now add the unique constraint
        migrations.AlterField(
            model_name="user",
            name="referral_code",
            field=models.CharField(blank=True, max_length=20, unique=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="loyalty_points",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name="UserAddress",
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
                ("label", models.CharField(default="Home", max_length=30)),
                ("address", models.CharField(max_length=250)),
                ("country", models.CharField(blank=True, max_length=30)),
                ("state", models.CharField(blank=True, max_length=30)),
                ("city", models.CharField(blank=True, max_length=50)),
                ("pincode", models.CharField(blank=True, max_length=10)),
                ("is_default", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="addresses",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "User Addresses",
            },
        ),
    ]
