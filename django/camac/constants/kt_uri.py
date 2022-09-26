KOOR_BG_SERVICE_ID = 1
KOOR_NP_SERVICE_ID = 87
KOOR_BD_SERVICE_ID = 302
KOOR_SD_SERVICE_ID = 590
KOOR_AFJ_SERVICE_ID = 546
BUNDESSTELLE_SERVICE_ID = 141

KOOR_BD_GROUP_ID = 502
KOOR_SD_GROUP_ID = 1022

CIRCULATION_STATE_RUN = 1
CIRCULATION_STATE_OK = 2
CIRCULATION_STATE_IDLE = 21
CIRCULATION_STATE_NFD = 41

ROLE_MUNICIPALITY = 6  # Sekretariat der Gemeindebaubehörde
ROLE_KOOR_BG = 3
ROLE_KOOR_BD = 1101
ROLE_KOOR_NP = 1061

SERVICE_GROUP_KOOR = 1

INTERNAL_DOCUMENTS_ATTACHMENT_SECTION_ID = 12000001
LISAG_ATTACHMENT_SECTION_ID = 12000007
KOOR_AFJ_ATTACHMENT_SECTION_ID = 12000008
MUNICIPALITY_SERVICE_ATTACHMENT_SECTION_ID = 12000003

LISAG_GROUP_ID = 283
KOOR_NP_GROUP_ID = 21
KOOR_BG_GROUP_ID = 142
KOOR_AFJ_GROUP_ID = 836
SACHBEARBEITUNG_AFJ_GROUP_ID = 102
SACHBEARBEITUNG_UND_KOORDINATION_AFJ_GROUP_ID = 42

WORKFLOW_ENTRY_RECEIVED_DECISION = 87
WORKFLOW_ENTRY_RECEIVED_PRELIMINARY_DECISION = 130000

WORKFLOW_ITEM_DOSSIER_ERFASST = 12
WORKFLOW_ITEM_FORWARD_TO_KOOR = 16

BUILDINGAUTHORITY_BUTTON_DECISION = 14
BUILDINGAUTHORITY_BUTTON_PRELIMINARY_DECISION = 15

INTENT_SLUGS = [
    "proposal-description",
    "beschreibung-zu-mbv",
    "bezeichnung",
    "vorhaben-proposal-description",
    "veranstaltung-beschrieb",
]

# Question identifiers (Chapter/Question/Item) for various information that we need
# Format: List of 3-tuples to implement fallback
CQI_FOR_PROPOSAL = [(21, 97, 1)]
CQI_FOR_PROPOSAL_DESCRIPTION = [(21, 98, 1)]
CQI_FOR_PARZELLE = [(21, 91, 1), (101, 91, 1), (102, 91, 1)]
CQI_FOR_STREET = [(21, 93, 1), (101, 93, 1), (102, 93, 1)]
CQI_FOR_APPLICANT_NAME = [(1, 23, 1)]
CQI_FOR_APPLICANT_ORGANISATION = [(1, 221, 1)]
CQI_FOR_APPLICANT_STREET = [(1, 61, 1)]
CQI_FOR_APPLICANT_ZIP_CITY = [(1, 62, 1)]
CQI_FOR_GESUCHSTELLER = [(1, 23, 1)]

FORM_BGBB = 41
FORM_BAUGESUCH = 298
FORM_VORABKLAERUNG = 299
FORM_REKLAME = 121
FORM_MELDUNG_SOLARANLAGE = 141
FORM_KANTONSGEBIET = 247
FORM_MELDUNG_VORHABEN = 290
FORM_MITBERICHT_BUNDESSTELLE = 292
FORM_ARCHIV = 293
FORM_OEREB_VERFAHREN = 296
FORM_MELDUNG_GEBAEUDETECHNIK = 297
FORM_MITBERICHT_KANTON = 300
FORM_BAUVERWALTUNG = 301
FORM_BOHRBEWILLIGUNG_WAERMEENTNAHME = 302
FORM_KONZESSION_WAERMEENTNAHME = 303

PORTAL_FORMS = [
    FORM_BAUGESUCH,
    FORM_VORABKLAERUNG,
    FORM_REKLAME,
    FORM_MELDUNG_SOLARANLAGE,
    FORM_MELDUNG_VORHABEN,
]

RESPONSIBLE_KOORS = {
    KOOR_BG_SERVICE_ID: [
        FORM_BAUGESUCH,
        FORM_VORABKLAERUNG,
        FORM_REKLAME,
        FORM_MELDUNG_SOLARANLAGE,
        FORM_MELDUNG_VORHABEN,
        FORM_MELDUNG_GEBAEUDETECHNIK,
    ],
    KOOR_NP_SERVICE_ID: [
        FORM_OEREB_VERFAHREN,
    ],
}


CALUMA_FORM_MAPPING = {
    FORM_VORABKLAERUNG: "baugesuch-vorabklaerung",
    FORM_BGBB: "bgbb",
    FORM_BAUGESUCH: "baubewilligungsverfahren",
    FORM_REKLAME: "commercial-permit",
    FORM_MELDUNG_SOLARANLAGE: "solar-announcement",
    FORM_KANTONSGEBIET: "kantonsgebiet",
    FORM_MELDUNG_VORHABEN: "project-announcement",
    FORM_ARCHIV: "archiv",
    FORM_MITBERICHT_BUNDESSTELLE: "mitbericht-bundesstelle",
    FORM_OEREB_VERFAHREN: "oereb",
    FORM_MELDUNG_GEBAEUDETECHNIK: "technische-bewilligung",
    FORM_MITBERICHT_KANTON: "mitbericht-kanton",
    FORM_BAUVERWALTUNG: "bauverwaltung",
    FORM_BOHRBEWILLIGUNG_WAERMEENTNAHME: "bohrbewilligung-waermeentnahme",
    FORM_KONZESSION_WAERMEENTNAHME: "konzession-waermeentnahme",
}

PARASHIFT_ATTACHMENT_SECTION_MAPPING = {
    "Fachstellen": 12000002,
    "Gesuchsteller": 12000000,
    "Leitbehörde": 12000004,
}
