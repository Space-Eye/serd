# Generated by Django 4.0.4 on 2022-04-27 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('serd', '0011_remove_ansprechpartnerhotel_hotel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='state',
            field=models.CharField(choices=[('aktive', 'Aktiv'), ('open', 'offen'), ('full', 'Keine Kapazitäten'), ('passive', 'Passiv')], max_length=64, verbose_name='Status'),
        ),
    ]
