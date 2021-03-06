# Generated by Django 3.2.12 on 2022-06-06 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('serd', '0022_auto_20220529_2239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='offer_filter',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='serd.offerfilter'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='request_filter',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='serd.requestfilter'),
        ),
        migrations.AlterField(
            model_name='requestfilter',
            name='current_housing',
            field=models.CharField(blank=True, choices=[('none', 'Ich habe keinen Schlafplatz'), ('friends', 'Bei Freunden oder Verwandten'), ('shelter', 'Staatliche Notunterkunft'), ('hotel', 'Im Hotel')], default='', max_length=64, verbose_name='Aktuelle Unterbringung'),
            preserve_default=False,
        ),
    ]
