# Generated by Django 2.2.2 on 2019-07-05 20:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fpiweb', '0017_location_locbin_locrow_loctier_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='active_location',
            field=models.ForeignKey(blank=True, help_text='The active location for when user is building a pallet (Location)', null=True, on_delete=django.db.models.deletion.SET_NULL, to='fpiweb.Location'),
        ),
    ]
