# Generated by Django 2.2.1 on 2019-06-10 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fpiweb', '0014_auto_20190523_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='box',
            name='print_box_number_label',
            field=models.BooleanField(default=False, help_text='Whether or not box number label needs printed', verbose_name='Print Box Number Label'),
        ),
    ]
