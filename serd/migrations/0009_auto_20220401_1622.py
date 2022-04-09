# Generated by Django 2.2.24 on 2022-04-01 16:22

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('serd', '0008_auto_20220401_1620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='pets',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('dog', 'Hund'), ('cat', 'Katze'), ('small', 'Kleintier')], max_length=13),
        ),
    ]