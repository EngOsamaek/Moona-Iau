# Generated by Django 4.1.2 on 2023-06-04 21:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Moona', '0002_virtualorder_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='product',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='Moona.product'),
            preserve_default=False,
        ),
    ]
