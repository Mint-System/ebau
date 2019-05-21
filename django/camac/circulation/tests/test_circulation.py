import pytest
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status

from camac.circulation import serializers
from camac.markers import only_schwyz

# module-level skip if we're not testing Schwyz variant
pytestmark = only_schwyz


@pytest.mark.parametrize(
    "role__name,instance__user,num_queries",
    [
        ("Applicant", LazyFixture("admin_user"), 5),
        ("Kanton", LazyFixture("user"), 5),
        ("Gemeinde", LazyFixture("user"), 5),
        ("Fachstelle", LazyFixture("user"), 5),
    ],
)
def test_circulation_list(
    admin_client,
    instance_state,
    circulation,
    activation,
    num_queries,
    django_assert_num_queries,
):
    url = reverse("circulation-list")

    included = serializers.CirculationSerializer.included_serializers
    with django_assert_num_queries(num_queries):
        response = admin_client.get(
            url,
            data={
                "instance_state": instance_state.pk,
                "include": ",".join(included.keys()),
            },
        )
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == 1
    assert json["data"][0]["id"] == str(circulation.pk)
    assert len(json["included"]) == len(included)


@pytest.mark.parametrize(
    "role__name,instance__user", [("Applicant", LazyFixture("admin_user"))]
)
def test_circulation_detail(admin_client, circulation):
    url = reverse("circulation-detail", args=[circulation.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
