# Generated by Django 2.1.7 on 2019-04-20 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fpiweb', '0011_auto_20190415_0430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='box',
            name='exp_month_end',
            field=models.IntegerField(blank=True, help_text='Optional ending month range of when the product expires, if filled.', null=True, verbose_name='Expiration End Month (Optional)'),
        ),
    ]