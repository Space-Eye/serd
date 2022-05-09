# Generated by Django 4.0.4 on 2022-05-09 16:21

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('serd', '0019_alter_offer_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='housingrequest',
            name='languages',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('de', 'Deutsch'), ('uk', 'Ukrainisch'), ('ru', 'Russisch'), ('en', 'Englisch')], max_length=11, null=True, verbose_name='Sprachkenntnisse'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='language',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('de', 'Deutsch'), ('uk', 'Ukrainisch'), ('ru', 'Russisch'), ('en', 'Englisch')], default=['de'], max_length=11, null=True, verbose_name='Welche Sprachen sprechen Sie?'),
        ),
    ]
