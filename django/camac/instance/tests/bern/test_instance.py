import pytest
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status

from camac.applicants.factories import ApplicantFactory
from camac.instance import serializers


@pytest.mark.parametrize(
    "instance_state__name,instance__creation_date",
    [("new", "2018-04-17T09:31:56+02:00")],
)
@pytest.mark.parametrize(
    "role__name,instance__user,editable",
    [
        ("Service", LazyFixture("user"), {"form", "document"}),
        ("Fachstelle", LazyFixture("user"), {"form", "instance", "document"}),
        ("Support", LazyFixture("user"), {"form", "instance", "document"}),
    ],
)
def test_instance_list(
    admin_client, instance, activation, group, editable, group_location_factory
):

    url = reverse("bern-instance-list")
    included = serializers.InstanceSerializer.included_serializers
    response = admin_client.get(
        url,
        data={
            "include": ",".join(included.keys()),
            "creation_date_before": "17.04.2018",
            "creation_date_after": "17.04.2018",
        },
    )

    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == 1
    assert json["data"][0]["id"] == str(instance.pk)
    assert set(json["data"][0]["meta"]["editable"]) == set(editable)
    # Included previous_instance_state and instance_state are the same
    assert len(json["included"]) == len(included) - 1


@pytest.mark.parametrize(
    "instance_state__name,instance__creation_date",
    [("new", "2018-04-17T09:31:56+02:00")],
)
@pytest.mark.parametrize(
    "role__name,instance__user,editable",
    [("Applicant", LazyFixture("admin_user"), {"form", "instance", "document"})],
)
def test_instance_list_as_applicant(
    admin_client,
    admin_user,
    instance,
    activation,
    group,
    editable,
    group_location_factory,
):

    ApplicantFactory(instance=instance, user=admin_user, invitee=admin_user)

    url = reverse("bern-instance-list")
    included = serializers.InstanceSerializer.included_serializers
    response = admin_client.get(
        url,
        data={
            "include": ",".join(included.keys()),
            "creation_date_before": "17.04.2018",
            "creation_date_after": "17.04.2018",
        },
    )

    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == 1
    assert json["data"][0]["id"] == str(instance.pk)
    assert set(json["data"][0]["meta"]["editable"]) == set(editable)
    # Included previous_instance_state and instance_state are the same
    assert len(json["included"]) == len(included) - 1


@pytest.mark.parametrize(
    "role__name,instance__user", [("Applicant", LazyFixture("admin_user"))]
)
def test_instance_detail(admin_client, admin_user, instance):
    ApplicantFactory(instance=instance, user=admin_user, invitee=admin_user)

    url = reverse("bern-instance-detail", args=[instance.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("instance__identifier", ["00-00-000"])
@pytest.mark.parametrize("form_field__name", ["name"])
@pytest.mark.parametrize(
    "role__name,instance__user", [("Applicant", LazyFixture("admin_user"))]
)
@pytest.mark.parametrize(
    "form_field__value,search",
    [
        ("simpletext", "simple"),
        (["list", "value"], "list"),
        ({"key": ["l-list-d", ["b-list-d"]]}, "list"),
    ],
)
def test_instance_search(admin_client, admin_user, instance, form_field, search):
    ApplicantFactory(instance=instance, user=admin_user, invitee=admin_user)
    url = reverse("bern-instance-list")

    response = admin_client.get(url, {"search": search})
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == 1
    assert json["data"][0]["id"] == str(instance.pk)


@pytest.mark.parametrize("instance_state__name", ["Neu"])
@pytest.mark.parametrize(
    "role__name,instance__user,status_code",
    [
        # NOTE: Problem is that queryset is limited to instances with activations...
        ("Applicant", LazyFixture("admin_user"), status.HTTP_204_NO_CONTENT),
        # TODO: I think the schwyz setup is broken. 404 is returned because of the queryset is empty
        # and not because someone is not allowed to destroy an instance. DRF returns 403 if the
        # permission has been denied.
        ("Service", LazyFixture("user"), status.HTTP_404_NOT_FOUND),
        ("Fachstelle", LazyFixture("user"), status.HTTP_404_NOT_FOUND),
        ("Support", LazyFixture("admin_user"), status.HTTP_403_FORBIDDEN),
    ],
)
def test_instance_destroy(
    admin_client, role, admin_user, instance, status_code, location_factory
):
    ApplicantFactory(instance=instance, user=admin_user, invitee=admin_user)
    url = reverse("bern-instance-detail", args=[instance.pk])
    response = admin_client.delete(url)
    assert response.status_code == status_code
