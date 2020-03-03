# Generated by Django 2.2.9 on 2020-02-11 01:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fpiweb', '0025_restore_pallet_box_number_tweak_activity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='box',
            name='location',
            field=models.ForeignKey(blank=True, help_text='Location of box', null=True, on_delete=django.db.models.deletion.SET_NULL, to='fpiweb.Location'),
        ),
        migrations.AlterField(
            model_name='palletbox',
            name='box',
            field=models.ForeignKey(blank=True, help_text='Internal record identifier for a box.', null=True, on_delete=django.db.models.deletion.PROTECT, to='fpiweb.Box'),
        ),
        migrations.AlterField(
            model_name='palletbox',
            name='box_number',
            field=models.CharField(blank=True, help_text='Number printed in the label on the box.', max_length=8, null=True, verbose_name='Visible Box Number'),
        ),
        migrations.AlterField(
            model_name='palletbox',
            name='exp_year',
            field=models.IntegerField(blank=True, help_text='Year the product expires, if filled.', null=True, verbose_name='Year Product Expires'),
        ),
        migrations.AlterField(
            model_name='palletbox',
            name='pallet',
            field=models.ForeignKey(help_text='Internal record identifier for a pallet.', on_delete=django.db.models.deletion.PROTECT, related_name='boxes', to='fpiweb.Pallet'),
        ),
        migrations.AlterField(
            model_name='palletbox',
            name='product',
            field=models.ForeignKey(blank=True, help_text='Product contained in this box, if filled.', null=True, on_delete=django.db.models.deletion.PROTECT, to='fpiweb.Product', verbose_name='product'),
        ),
    ]
