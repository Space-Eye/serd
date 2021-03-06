# Generated by Django 4.0.4 on 2022-04-20 15:10

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields
import serd.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('number', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, verbose_name='Name')),
                ('address', models.TextField(verbose_name='Adresse')),
                ('state', models.CharField(choices=[('aktive', 'Aktiv'), ('open', 'offen'), ('full', 'Keine Kapazitäten')], max_length=64, verbose_name='Status')),
                ('food', models.CharField(blank=True, choices=[('breakfast', 'Frühstück'), ('inclusive', 'Inklusive'), ('space-eye', 'Durch Space-Eye')], max_length=64, verbose_name='Verpflegung')),
                ('cost', models.CharField(max_length=128, verbose_name='Kosten')),
                ('beds_adults', models.PositiveSmallIntegerField(validators=[serd.validators.validate_not_negative], verbose_name='Betten Erwachsene')),
                ('beds_children', models.PositiveSmallIntegerField(validators=[serd.validators.validate_not_negative], verbose_name='Betten Kinder')),
                ('adults_free', models.IntegerField(blank=True, null=True, verbose_name='NICHTS EINTRAGEN, TECHNISCHES FELD, KOMMT BALD WEG')),
                ('children_free', models.IntegerField(blank=True, null=True, verbose_name='NICHTS EINTRAGEN, TECHNISCHES FELD, KOMMT BALD WEG')),
                ('info', models.TextField(blank=True, verbose_name='Info')),
                ('responsible', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='responsible_for_hotel', to=settings.AUTH_USER_MODEL, verbose_name='Zuständig Meldung')),
                ('team_gesamt', models.ManyToManyField(related_name='tem_for_hotel', to=settings.AUTH_USER_MODEL, verbose_name='Team gesamt')),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('number', models.AutoField(primary_key=True, serialize=False)),
                ('last_name', models.CharField(blank=True, max_length=128, validators=[serd.validators.validate_not_empty], verbose_name='Nachname')),
                ('given_name', models.CharField(blank=True, max_length=128, verbose_name='Vorname')),
                ('plz', models.CharField(blank=True, max_length=5, validators=[serd.validators.validate_plz], verbose_name='Postleitzahl')),
                ('total_number', models.PositiveSmallIntegerField(blank=True, validators=[serd.validators.validate_not_negative], verbose_name='Anzahl der Personen, die in dieser Wohnung eine Unterkunft finden können.')),
                ('children_number', models.PositiveSmallIntegerField(blank=True, validators=[serd.validators.validate_not_negative], verbose_name='Anzahl der zuvor genannten Plätze, die nur für Kinder unter 12 geeignet sind.')),
                ('street', models.CharField(blank=True, max_length=256, verbose_name='Straße, Hausnummer (optional)')),
                ('city', models.CharField(blank=True, max_length=256, verbose_name='Ort')),
                ('language', multiselectfield.db.fields.MultiSelectField(choices=[('de', 'Deutsch'), ('uk', 'Ukrainisch'), ('ru', 'Russisch'), ('en', 'Englisch')], max_length=11, verbose_name='Welche Sprachen sprechen Sie?')),
                ('additional_languages', models.CharField(blank=True, max_length=64, verbose_name='Weitere Sprachen')),
                ('for_free', models.BooleanField(verbose_name='Ich stelle die Unterkunft mindestens vorübergehend kostenlos zur Verfügung.')),
                ('cost', models.PositiveSmallIntegerField(null=True, validators=[serd.validators.validate_not_negative])),
                ('spontan', models.BooleanField(help_text='innerhalb eines Tages', verbose_name='spontanes zur Verfügung stellen ist möglich')),
                ('available_from', models.DateField(verbose_name='Ab wann steht die Unterkunft zur Verfügung?')),
                ('limited_availability', models.BooleanField(verbose_name='Die Unterkunft wird nur zeitlich begrenzt zur Verfügung gestellt.')),
                ('available_until', models.DateField(null=True)),
                ('accessability', models.BooleanField(verbose_name='Ist die Unterkunft barrierefrei?')),
                ('public_transport', models.BooleanField(verbose_name='Ist die Unterkunft mit öffentlichen Verkehrsmitteln erreichbar? ')),
                ('rooms', models.SmallIntegerField(blank=True, verbose_name='Anzahl der zur Verfügung gestellten Zimmer')),
                ('seperate_appartment', models.BooleanField(verbose_name='Unterkunft erfolgt in einer separaten Wohnung.')),
                ('living_with', models.CharField(blank=True, choices=[('single', 'alleine'), ('family', 'mit Familie'), ('friends', 'mit Freunden')], max_length=64, verbose_name='Bei Unterbringung in der eigenen Wohnung: Ich wohne')),
                ('pets', multiselectfield.db.fields.MultiSelectField(choices=[('dog', 'Hund'), ('cat', 'Katze'), ('small', 'Kleintier'), ('none', 'Keine')], max_length=18, verbose_name='Folgende Haustiere sind erlaubt.')),
                ('state', models.CharField(choices=[('new', 'Neu'), ('contacted', 'Kontaktiert'), ('request_contact', 'Kontakt zu Gast'), ('arrived', 'Gast ist Angekommen'), ('stale', 'Nicht mehr verfügbar'), ('free', 'Unterkunft wieder Verfügbar'), ('reserved', 'Reserviert'), ('no', 'Nicht Tragbar')], default='new', max_length=64, verbose_name='Status')),
                ('phone', models.CharField(blank=True, max_length=128, validators=[serd.validators.validate_phone], verbose_name='Telefonnummer')),
                ('mail', models.CharField(blank=True, max_length=128, validators=[django.core.validators.EmailValidator()], verbose_name='E-mail')),
                ('comment', models.CharField(blank=True, max_length=250)),
                ('private_comment', models.CharField(blank=True, default='', max_length=512)),
                ('by_municipality', models.BooleanField(default=False, verbose_name='Von Stadt Vermittelt')),
                ('covid', models.BooleanField(default=False, verbose_name='Eine COVID-19-Impfung ist zwingend notwendig.')),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='HousingRequest',
            fields=[
                ('number', models.AutoField(primary_key=True, serialize=False)),
                ('last_name', models.CharField(blank=True, max_length=128, verbose_name='Nachname')),
                ('given_name', models.CharField(blank=True, max_length=128, verbose_name='Vorname')),
                ('name_slug', models.CharField(blank=True, default='', max_length=256)),
                ('phone', models.CharField(blank=True, max_length=50, validators=[serd.validators.validate_phone], verbose_name='Telefonnummer')),
                ('mail', models.CharField(blank=True, max_length=256, validators=[django.core.validators.EmailValidator()], verbose_name='E-Mail-Adresse')),
                ('representative', models.CharField(blank=True, help_text='falls zutreffend', max_length=256, verbose_name='Name einer stellvertretenden Person')),
                ('repr_phone', models.CharField(blank=True, max_length=256, validators=[serd.validators.validate_phone], verbose_name='Telefonnummer der stellvertretenden Person')),
                ('repr_mail', models.CharField(blank=True, max_length=256, validators=[django.core.validators.EmailValidator()], verbose_name='E-Mail-Adresse der stellvertretenden Person')),
                ('adults', models.PositiveSmallIntegerField(blank=True, validators=[serd.validators.validate_not_negative], verbose_name='Anzahl der Erwachsenen und Kindern ab 12 Jahren')),
                ('children', models.PositiveSmallIntegerField(blank=True, validators=[serd.validators.validate_not_negative], verbose_name='Anzahl der Kinder unter 12')),
                ('who', models.CharField(blank=True, max_length=256)),
                ('split', models.BooleanField(help_text='notfalls kann eine Unterbringung in zwei Unterkünften erfolgen', verbose_name='Ab fünf Personen: Gruppe darf geteilt werden')),
                ('current_housing', models.CharField(blank=True, choices=[('none', 'Ich habe keinen Schlafplatz'), ('friends', 'Bei Freunden oder Verwandten'), ('shelter', 'Staatliche Notunterkunft'), ('hotel', 'Im Hotel')], max_length=128, verbose_name='Wo sind Sie aktuell untergebracht?')),
                ('arrival_date', models.DateField(null=True, verbose_name='Wann kommen Sie in Regensburg an oder seit wann sind Sie da?')),
                ('arrival_location', models.CharField(blank=True, help_text='zum Beispiel Regensburg Hauptbahnhof', max_length=256, verbose_name='Wo in Regensburg kommen Sie an?')),
                ('pets', multiselectfield.db.fields.MultiSelectField(choices=[('dog', 'Hund'), ('cat', 'Katze'), ('small', 'Kleintier'), ('none', 'Keine')], max_length=18, null=True, verbose_name='Welche Haustiere haben Sie?')),
                ('pet_number', models.PositiveSmallIntegerField(blank=True, null=True, validators=[serd.validators.validate_not_negative], verbose_name='Wie viele Haustiere haben Sie?')),
                ('car', models.BooleanField(verbose_name='Haben Sie ein Auto?')),
                ('languages', multiselectfield.db.fields.MultiSelectField(choices=[('de', 'Deutsch'), ('uk', 'Ukrainisch'), ('ru', 'Russisch'), ('en', 'Englisch')], max_length=11, null=True, verbose_name='Sprachkenntnisse')),
                ('additional_languages', models.CharField(blank=True, max_length=64, verbose_name='Weitere Sprachen')),
                ('vaccination', models.BooleanField(verbose_name='Sind alle Personen in Ihrer Gruppe vollständig gegen COVID-19 geimpft?')),
                ('accessability_needs', models.BooleanField(verbose_name='Wird eine barrierefreie Wohnung benötigt?')),
                ('can_pay', models.BooleanField(help_text='Keine Voraussetzung für die Vermittlung einer privaten Notunterkunft', verbose_name='Können Sie für Ihre Unterkunft zahlen?')),
                ('priority', models.CharField(blank=True, choices=[('normal', 'Normal'), ('elevated', 'Erhöht'), ('high', 'Hoch')], max_length=64, verbose_name='Priorität')),
                ('state', models.CharField(choices=[('new', 'Neu'), ('contacted', 'Kontaktiert'), ('stale', 'nicht mehr aktuell'), ('housing_contact', 'Kontakt mit Unterkunft'), ('arrived', 'In Unterkunft angekommen'), ('no', 'Nicht vermittelbar')], default='new', max_length=64, verbose_name='Status')),
                ('private_comment', models.CharField(blank=True, default='', max_length=512, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('case_handler', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Sachbearbeiter:in')),
                ('hotel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='requests', to='serd.hotel', verbose_name='Hotel')),
                ('placed_at', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='serd.offer', verbose_name='Vermitttelt an')),
            ],
        ),
        migrations.CreateModel(
            name='AnsprechpartnerHotel',
            fields=[
                ('number', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('tel', models.CharField(blank=True, max_length=128, validators=[serd.validators.validate_phone], verbose_name='Telefonnummer')),
                ('mail', models.CharField(blank=True, max_length=128, validators=[django.core.validators.EmailValidator()], verbose_name='E-mail')),
                ('hotel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ansprechpartner', to='serd.hotel')),
            ],
        ),
    ]
