# Generated by Django 2.2.12 on 2020-09-17 14:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0013_auto_20200803_1338'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo_url', models.URLField(blank=True)),
                ('title', models.CharField(max_length=300)),
                ('price', models.CharField(max_length=300)),
                ('url', models.URLField()),
                ('img_url', models.URLField(blank=True, default='default.png')),
                ('category', models.CharField(max_length=300)),
                ('color', models.CharField(default='N/A', max_length=300)),
                ('size', models.CharField(default='N/A', max_length=300)),
                ('Qty', models.IntegerField(default=1)),
                ('statue', models.CharField(max_length=300)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
