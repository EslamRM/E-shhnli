# Generated by Django 2.2.12 on 2020-11-20 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0051_calculator_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='statue',
            field=models.CharField(choices=[('Reviewing', 'Reviewing'), ('Reviewed', 'Reviewed'), ('Charging', 'Charging')], default='Pending', help_text='Statue', max_length=300),
        ),
    ]
