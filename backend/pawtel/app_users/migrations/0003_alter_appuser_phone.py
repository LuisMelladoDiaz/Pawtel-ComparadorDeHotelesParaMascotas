

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_users", "0002_termsacceptance"),
    ]

    operations = [
        migrations.AlterField(
            model_name="appuser",
            name="phone",
            field=models.CharField(
                max_length=13,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="El número de teléfono debe ser del formato: +34XXXXXXXXX",
                        regex="^\\+34\\d{9}$",
                    )
                ],
            ),
        ),
    ]
