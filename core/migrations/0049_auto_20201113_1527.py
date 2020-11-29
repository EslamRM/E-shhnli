# Generated by Django 2.2.12 on 2020-11-13 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0048_auto_20201113_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commercialorder',
            name='price',
            field=models.DecimalField(decimal_places=2, default=1, help_text='Price', max_digits=10),
        ),
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.CharField(help_text='Price', max_length=300),
        ),
    ]
