from datetime import date, datetime
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core import mail
from .models import Hotel
from .utils.db import get_departing_stays, get_persons, get_requests, get_stays
import logging
logger = logging.getLogger('default')

def yesno(boolean):
    if boolean:
        return _("Ja")
    else:
        return _("Nein")

REQUEST_CONFIRMATION_SUBJECT = _("Wohnungsgesuch mit der Nummer {id} erfolgreich eingetragen")
OFFER_CONFIRMATION_SUBJECT = _("Wohnungsangebot mit der Nummer {id} erfolgreich eingetragen")
OFFER_CONFIRMATION_TEXT = _("""Guten Tag,
Ihr Wohnungsangebot wurde mit folgenden Daten erfolgreich in die Space-Eye Datenbank aufgenommen:
{table}
Sollten sich Änderungen ergeben, teilen Sie uns diese bitte unter 'kontakt@space-eye.org' mit
und geben dabei die Nr {id} an.
""")
REQUEST_CONFIRMATION_TEXT = _("""Guten Tag,
Ihr Wohnungsgesuch wurde mit folgenden Daten erfolgreich in die Space-Eye Datenbank aufgenommen:
{table}
Sollten sich Änderungen ergeben, teilen Sie uns diese bitte unter 'kontakt@space-eye.org' mit
und geben dabei die Nr {id} an.
""")

def create_offer_table_string(offer):
    string = _("""Vorname:\t{given_name}
Nachname:\t{last_name}
PLZ:\t{plz}
Ort:\t{city}
""").format(given_name=offer.given_name, last_name=offer.last_name, plz=offer.plz, city=offer.city)
    if offer.street:
        string += _("Straße:\t{street}").format(street=offer.street)
    string +=_("""Telefon:\t{phone}
E-Mail:\t{mail}
Sprachen:\t{language}
Anzahl Personen:\t{total_number}
Davon Kinder:\t{children_number}
Kostenfreie Unterkunft:\t{for_free}
""").format(phone=offer.phone, mail=offer.mail, language=offer.get_language_display(), total_number=offer.total_number,
            children_number=offer.children_number, for_free=yesno(offer.for_free))

    if not offer.for_free:
        string += _("Miete:\t{cost}\n").format(cost=offer.cost)
    string += _("""Spontan Verfügbar:\t{spontan}
Verfügbar ab:\t{available_from}
Nur vorrübergehend verfügbar:\t{limited_availability}
""").format(spontan=yesno(offer.spontan), available_from = offer.available_from, limited_availability=yesno(offer.limited_availability))
    
    if offer.limited_availability:
        string += _("Verfügbar bis:\t{available_until}\n").format(available_until=offer.available_until)
    string += _("""Mit ÖPNV erreichbar:\t{public_transport}
Zahl der Zimmer:\t{rooms}
Eigenständige Wohnung:\t{seperate_appartment}
""").format(public_transport=yesno(offer.public_transport), rooms=offer.rooms, seperate_appartment=yesno(offer.seperate_appartment))
    if not offer.seperate_appartment:
        string += _("Meine Wohnsituation:\t{living_with}\n").format(living_with=offer.get_living_with_display())
    string += _("""Erlaubte Haustiere:\t{pets}
Kommentar:\t{comment}""").format(pets=offer.get_pets_display(), comment=offer.comment)
    return string

def create_request_table_string(request):
    string = _("""Vorname:\t{given_name}
Nachname:\t{last_name}
Telefon:\t{phone}
Erwachsene:\t{adults}
Kinder:\t{children}
Beschreibung:\t{who}
Gruppe teilbar:\t{split}
Aktuelle Unterkunft:\t{current_housing}
""").format(given_name=request.given_name, last_name=request.last_name, phone=request.phone,
            adults=request.adults, children=request.children, split=yesno(request.split),
            who=request.who, current_housing=request.get_current_housing_display())
    if request.representative:
        string+=_("""Stellvertreter:in :\t{representative}
Stellvertreter:in Telefon:\t{repr_phone}
Stellvertreter:in E-Mail:\t{repr_mail}
""").format(representative=request.representative, repr_phone=request.repr_phone,
            repr_mail=request.repr_mail)
    string += _("""Ankunftsdatum:\t{arrival_date}
Haustiere:\t{pets}
Anzahl Haustiere\t{pet_number}
Auto vorhanden\t{car}
Sprachen:\t{languages}
Impfung:\t{vaccination}
Barrierefrei:\t{accessability_needs}
""").format(arrival_date=request.arrival_date,
            pets=request.get_pets_display(), pet_number=request.pet_number,
            car=yesno(request.car), languages=request.get_languages_display(),
            vaccination=yesno(request.vaccination), accessability_needs=yesno(request.accessability_needs)
)
    return string
class Mailer:
    def send_offer_confirmation_mail(self, offer):
        subject = OFFER_CONFIRMATION_SUBJECT.format(id=offer.number)
        text = OFFER_CONFIRMATION_TEXT.format(id=offer.number, table=create_offer_table_string(offer))
        logger.debug("connecting to mail server")
        try:
            with mail.get_connection() as connection:
                logger.debug("Sending offer confirmation mail to %s, for offer %s", offer.mail, offer.number)
                try:
                    mail.EmailMessage(subject, text, settings.EMAIL_HOST_USER, [offer.mail]).send()
                    logger.debug("Success")
                except Exception as e:
                    logger.error("Sending failed with %s", str(e))
        except Exception as e:
            logger.error("Connecting to mail server failed with %s", str(e))

    def send_request_confirmation_mail(self, request):
        subject = REQUEST_CONFIRMATION_SUBJECT.format(id=request.number)
        text = REQUEST_CONFIRMATION_TEXT.format(id=request.number, table=create_request_table_string(request))
        logger.debug("connecting to mail server")
        try:
            with mail.get_connection() as connection:
                logger.debug("Sending request confirmation mail to %s for request %s", request.mail, request.number)
                try:
                    mail.EmailMessage(subject, text, settings.EMAIL_HOST_USER, [request.mail]).send()
                except Exception as e:
                    logger.error("Sending mail failed with %s", str(e))
        except Exception as e:
            logger.error("Connecting to mail server failed with %s", str(e))

    def send_departure_mail(self, data, today, total, address):
        logger.debug("Creating departure mail text departure mail to %s ", address)
        text = """Hallo,
Space-Eye hat laut Datenbank gerade {persons} Personen im Dream Inn untergebracht.
""".format(persons=total)

        
        
        text += "Davon reisen heute ({day}) {persons} Personen aus den Zimmern {rooms} ab.\n".format(
                day = date.today(), persons=today[0], rooms =" ".join(today[1]))
        if data:            
            for day in data.keys():
                text+="am {day} reisen nach derzeitigem Stand {persons} Personen aus den Zimmern {rooms} ab.\n".format(day = day, persons=data[day][0], rooms =" ".join(data[day][1]))
        text += "Herzliche Grüße,\nTeam Space-Eye"
        logger.debug("connecting to mail server")
        try:
            with mail.get_connection() as connection:
                logger.debug("Sending departure mail")
                try:
                    mail.EmailMessage("Vorraussichtliche Abreisen", text, settings.EMAIL_HOST_USER, [address]).send()
                    logger.debug("Success")
                except Exception as e:
                    logger.error("Sending failed with %s", str(e))
        except Exception as e:
            logger.error("Connecting to mail server failed with %s", str(e))
        

