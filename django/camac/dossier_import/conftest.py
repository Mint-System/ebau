import pytest
from django.core.management import call_command
from django.utils.module_loading import import_string

from camac.dossier_import.tests.test_dossier_import_case import TEST_IMPORT_FILE


@pytest.fixture
def setup_workflow_fixtures(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command("loaddata", "/app/kt_schwyz/config/caluma_workflow.json")


@pytest.fixture
def setup_workflow_fixtures_for_config(django_db_setup, django_db_blocker):
    def wrapper(config):
        with django_db_blocker.unblock():
            call_command("loaddata", f"/app/{config}/config/caluma_workflow.json")
            call_command("loaddata", f"/app/{config}/config/instance.json")
            # call_command("loaddata", f"/app/{config}/config/user.json")

    return wrapper


@pytest.fixture
def initialized_dossier_importer(
    db,
    setup_workflow_fixtures_for_config,
    settings,
    service_factory,
    user_factory,
    group_factory,
    role_factory,
    form_factory,
    form_state_factory,
    instance_state_factory,
    attachment_section_factory,
):
    def wrapper(config, service_id: int, path_to_archive: str = TEST_IMPORT_FILE):
        application_settings = settings.APPLICATIONS[config]
        setup_workflow_fixtures_for_config(config)
        # form_state_factory(pk=1)
        # form_factory(
        #     pk=application_settings["DOSSIER_IMPORT"]["FORM_ID"], form_state_id=1
        # )
        service = service_factory(service_id=service_id)
        role = role_factory(pk=application_settings["DOSSIER_IMPORT"]["ROLE_ID_GROUP"])
        group_factory(service=service, role=role)
        user_factory(username=application_settings["DOSSIER_IMPORT"]["USER"])
        # for mapping in application_settings["DOSSIER_IMPORT"][
        #     "INSTANCE_STATE_MAPPING"
        # ].values():
        #     instance_state_factory(pk=mapping)
        attachment_section_factory(
            pk=application_settings["DOSSIER_IMPORT"]["ATTACHMENT_SECTION_ID"]
        )

        importer_cls = import_string(
            application_settings["DOSSIER_IMPORT"]["XLSX_IMPORTER_CLASS"]
        )
        importer = importer_cls(settings=application_settings["DOSSIER_IMPORT"])
        importer.initialize(service_id, path_to_archive)
        return importer

    return wrapper
