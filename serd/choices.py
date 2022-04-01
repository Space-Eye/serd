REQUEST_STATE = (
    ('new','Neu'),
    ('in_progress','in Bearbeitung'),
    ('closed', 'vermittelt')
)
LANGUAGE_CHOICE = (
    ('de', 'Deutsch'),
    ('uk', 'Ukrainisch'),
    ('ru', 'Russisch'),
    ('en', 'Englisch')
)
LIVING_WITH = (
    ('single','alleine'),
    ('family','mit Familie'),
    ('friends', 'mit Freunden')
)

OFFER_STATE = (
    ('new','Neu'),
    ('contacted', 'Kontaktiert'),
    ('closed', 'Vermittelt' )
)
PRIORITY_CHOICE = (
    ('normal','Normal'),
    ('elevated','Erhöht'),
    ('high','Hoch')
)
CURRENT_ACCOMODATION = (
    ('none', 'Ich habe keinen Schlafplatz'),
    ('friends', 'Bei Freunden oder Verwandten'),
    ('hotel', 'Hotel')
)
PETS = (
    ('dog', 'Hund'),
    ('cat', 'Katze'),
    ('small', 'Kleintier')
)