# Generated by Django 2.1.7 on 2019-04-06 21:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fpiweb', '0006_auto_20190406_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='box',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='fpiweb.Product', verbose_name='product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='prod_name',
            field=models.CharField(max_length=30, verbose_name='product Name'),
        ),
    ]