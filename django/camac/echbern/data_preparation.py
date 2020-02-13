from caluma.caluma_form.models import Answer, Document, DynamicOption, Option

from .utils import xml_encode_newlines

# Dicts with all questions we need from caluma. Questions under the "top" key, are
# directly accessible. Other keys refer to tableQuestions with their corresponding
# sub-questions. The second tuple element is an example value and also used for tests.
slugs_baugesuch = {
    "top": [
        ("anzahl-abstellplaetze-fur-motorfahrzeuge", 23),
        ("baukosten-in-chf", 232323),
        ("bemerkungen", " Foo bar "),
        ("beschreibung-bauvorhaben", "Beschreibung\nMehr Beschreibung"),
        ("dauer-in-monaten", 23),
        ("effektive-geschosszahl", 23),
        ("gemeinde", "2"),
        ("geplanter-baustart", "2019-09-15"),
        ("gwr-egid", "23"),
        ("nr", "23"),
        ("nutzungsart", ["nutzungsart-wohnen"]),
        ("nutzungszone", "Testnutzungszone"),
        ("ort-grundstueck", "Burgdorf"),
        ("ort-parzelle", "Burgdorf"),
        ("sammelschutzraum", "sammelschutzraum-ja"),
        ("strasse-flurname", "Teststrasse"),
    ],
    "beschreibung-der-prozessart-tabelle": [
        [("prozessart", "prozessart-fliesslawine")]
    ],
    "parzelle": [
        [
            ("e-grid-nr", "23"),
            ("lagekoordinaten-nord", "1070500.000"),
            ("lagekoordinaten-ost", "2480034.0"),
            ("parzellennummer", "1586"),
        ],
        [
            ("e-grid-nr", "24"),
            ("lagekoordinaten-nord", "1070600.000"),
            ("lagekoordinaten-ost", "2480035.0"),
            ("parzellennummer", "1587"),
        ],
    ],
    "personalien-gesuchstellerin": [
        [
            ("name-gesuchstellerin", "Smith"),
            ("nummer-gesuchstellerin", "23"),
            ("ort-gesuchstellerin", "Burgdorf"),
            ("plz-gesuchstellerin", 2323),
            ("strasse-gesuchstellerin", "Teststrasse"),
            ("vorname-gesuchstellerin", "Winston"),
        ]
    ],
}

slugs_vorabklaerung_einfach = {
    "top": [
        ("anfrage-zur-vorabklaerung", "lorem ipsum"),
        ("e-grid-nr", "23"),
        ("gemeinde", "2"),
        ("gwr-egid", "23"),
        ("lagekoordinaten-nord-einfache-vorabklaerung", "1070500.000"),
        ("lagekoordinaten-ost-einfache-vorabklaerung", "2480034.0"),
        ("name-gesuchstellerin-vorabklaerung", "Smith"),
        ("nummer-gesuchstellerin", "23"),
        ("ort-gesuchstellerin", "Burgdorf"),
        ("parzellennummer", "23"),
        ("plz-gesuchstellerin", 2323),
        ("strasse-gesuchstellerin", "Teststrasse"),
        ("vorname-gesuchstellerin-vorabklaerung", "Winston"),
    ]
}


class DocumentParser:
    simple_questions = ["integer", "float", "text", "textarea", "date"]

    def __init__(self, document: Document):
        self.document = document
        self.slugs_table = slugs_baugesuch
        if document.form.slug == "vorabklaerung-einfach":
            self.slugs_table = slugs_vorabklaerung_einfach

        # main slugs are all questions under the "top" key combined with all the other keys
        main_slugs = [slug for slug, _ in self.slugs_table["top"]] + [
            key for key in self.slugs_table if not key == "top"
        ]
        self.answers = {"ech-subject": document.form.name["de"]}
        self.answers.update(self.parse_answers(self.document, main_slugs))

    def handle_string_values(self, value):
        value = self.strip_whitespace(value)
        value = xml_encode_newlines(value)
        return value

    @staticmethod
    def strip_whitespace(value):
        if isinstance(value, str):
            return value.strip(" ")
        return value

    def _get_option_label(self, slug):
        option = Option.objects.get(pk=slug)
        return self.handle_string_values(option.label["de"])

    def _choice(self, answer, document):
        return self._get_option_label(answer.value)

    def _multiple_choice(self, answer, document):
        return [self._get_option_label(slug) for slug in answer.value]

    def _get_dynamic_option_label(self, slug, document, question):
        option = DynamicOption.objects.filter(
            slug=slug, document=document, question=question
        ).first()
        return self.handle_string_values(option.label["de"])

    def _dynamic_choice(self, answer, document):
        return self._get_dynamic_option_label(answer.value, document, answer.question)

    def _dynamic_multiple_choice(self, answer, document):  # pragma: no cover
        return [
            self._get_dynamic_option_label(slug, document, answer.question)
            for slug in answer.value
        ]

    def _table(self, answer, document):
        rows = []
        # the relevant question slugs for this subform
        slugs = [slug for slug, _ in self.slugs_table[answer.question.slug][0]]

        for row_doc in answer.documents.all():
            rows.append(self.parse_answers(row_doc, slugs))
        return rows

    def parse_answers(self, document, slugs):
        caluma_answers = Answer.objects.filter(
            document=document, question__slug__in=slugs
        )

        answers = {}

        for answer in caluma_answers:
            question_type_name = answer.question.type

            if question_type_name in self.simple_questions:
                answers[answer.question.slug] = self.handle_string_values(answer.value)
                continue

            answers[answer.question.slug] = getattr(self, f"_{question_type_name}")(
                answer, document
            )

        return answers


def get_document(instance_id):
    document = Document.objects.get(
        **{"form__meta__is-main-form": True, "meta__camac-instance-id": instance_id}
    )
    dp = DocumentParser(document)
    return dp.answers
