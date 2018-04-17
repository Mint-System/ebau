import functools

import pyexcel
import pytest
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status

from camac.instance import serializers


@pytest.mark.parametrize("instance_state__name", [
    'new',
])
@pytest.mark.parametrize("role__name,instance__user,num_queries,editable", [
    ('Applicant', LazyFixture('admin_user'), 14, {'form', 'document'}),
    ('Canton', LazyFixture('user'), 14, {'document'}),
    ('Municipality', LazyFixture('user'), 14, {'document'}),
    ('Service', LazyFixture('user'), 14, {'document'}),
])
def test_instance_list(admin_client, instance, activation, num_queries,
                       django_assert_num_queries, editable):
    url = reverse('instance-list')

    included = serializers.InstanceSerializer.included_serializers
    with django_assert_num_queries(num_queries):
        response = admin_client.get(url, data={
            'include': ','.join(included.keys())
        })
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json['data']) == 1
    assert json['data'][0]['id'] == str(instance.pk)
    assert set(json['data'][0]['meta']['editable']) == set(editable)
    # included previous_instance_state and instance_state are the same
    assert len(json['included']) == len(included) - 1


@pytest.mark.parametrize("role__name,instance__user", [
    ('Applicant', LazyFixture('admin_user')),
])
def test_instance_detail(admin_client, instance):
    url = reverse('instance-detail', args=[instance.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("instance__identifier", ['00-00-000'])
@pytest.mark.parametrize("form_field__name", ['name'])
@pytest.mark.parametrize("role__name,instance__user", [
    ('Applicant', LazyFixture('admin_user')),
])
@pytest.mark.parametrize("form_field__value,search", [
    ('simpletext', 'simple'),
    (['list', 'value'], 'list'),
    ({'key': ['l-list-d', ['b-list-d']]}, 'list'),
])
def test_instance_search(admin_client, instance, form_field, search):
    url = reverse('instance-list')

    response = admin_client.get(url, {'search': search})
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert len(json['data']) == 1
    assert json['data'][0]['id'] == str(instance.pk)


@pytest.mark.parametrize("role__name,instance__user", [
    ('Applicant', LazyFixture('admin_user')),
])
def test_instance_filter_fields(admin_client, instance, form_field_factory):

    filters = {}

    for i in range(4):
        value = str(i)
        form_field_factory(name=value, value=value, instance=instance)
        filters['fields[' + value + ']'] = value

    url = reverse('instance-list')

    response = admin_client.get(url, filters)
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert len(json['data']) == 1


@pytest.mark.parametrize("instance_state__name,instance__identifier", [
    ('new', '00-00-000'),
])
@pytest.mark.parametrize("role__name,instance__user,status_code", [
    ('Applicant', LazyFixture('admin_user'), status.HTTP_400_BAD_REQUEST),
    ('Canton', LazyFixture('user'), status.HTTP_403_FORBIDDEN),
    ('Municipality', LazyFixture('user'), status.HTTP_403_FORBIDDEN),
    ('Service', LazyFixture('user'), status.HTTP_404_NOT_FOUND),
    ('Unknown', LazyFixture('user'), status.HTTP_404_NOT_FOUND),
])
def test_instance_update(admin_client, instance, location_factory,
                         form_factory, status_code):
    url = reverse('instance-detail', args=[instance.pk])

    data = {
        'data': {
            'type': 'instances',
            'id': instance.pk,
            'relationships': {
                'form': {
                    'data': {
                        'type': 'forms',
                        'id': form_factory().pk
                    }
                },
                'location': {
                    'data': {
                        'type': 'locations',
                        'id': location_factory().pk
                    }
                },
            }
        }
    }

    response = admin_client.patch(url, data=data)
    assert response.status_code == status_code


@pytest.mark.parametrize("role__name,instance__user", [
    ('Applicant', LazyFixture('admin_user')),
    ('Canton', LazyFixture('user')),
    ('Municipality', LazyFixture('user')),
    ('Service', LazyFixture('user')),
    ('Unknown', LazyFixture('user')),
])
def test_instance_destroy(admin_client, instance):
    url = reverse('instance-detail', args=[instance.pk])

    response = admin_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.parametrize("instance_state__name", [
    'new',
])
def test_instance_create(admin_client, admin_user, form,
                         instance_state):
    url = reverse('instance-list')

    data = {
        'data': {
            'type': 'instances',
            'id': None,
            'relationships': {
                'form': {
                    'data': {
                        'type': 'forms',
                        'id': form.pk
                    }
                },
            }
        }
    }

    response = admin_client.post(url, data=data)
    assert response.status_code == status.HTTP_201_CREATED

    json = response.json()

    url = reverse('instance-list')
    response = admin_client.post(url, data=json)
    assert response.status_code == status.HTTP_201_CREATED

    assert json['data']['attributes']['modification-date'] < (
        response.json()['data']['attributes']['modification-date']
    )


@pytest.mark.freeze_time('2017-7-27')
@pytest.mark.parametrize(
    "instance__user,location__communal_federal_number,instance_state__name",
    [(LazyFixture('admin_user'), '1311', 'new')]
)
@pytest.mark.parametrize("role__name,instance__location,form__name,status_code", [  # noqa: E501
    ('Applicant', LazyFixture('location'), 'baugesuch', status.HTTP_200_OK),
    ('Applicant', LazyFixture('location'), '', status.HTTP_400_BAD_REQUEST),
    ('Applicant', None, 'baugesuch', status.HTTP_400_BAD_REQUEST),
])
def test_instance_submit(admin_client, admin_user, form, form_field_factory,
                         instance, instance_state, instance_state_factory,
                         status_code):
    instance_state_factory(name='subm')
    url = reverse('instance-submit', args=[instance.pk])
    add_field = functools.partial(form_field_factory, instance=instance)

    add_field(name='kategorie-des-vorhabens', value=['Anlage(n)'])
    add_field(name='hohe-der-anlage', value=12.5, instance=instance)
    add_field(name='anlagen-mit-erheblichen-schadstoffemissionen',
              value='Nein')
    add_field(name='anlagen-mit-erheblichen-schadstoffemissionen-welche',
              value='Test')
    add_field(name='grundeigentumerschaft', value=[{'name': 'Name'}])
    add_field(
        name='gwr',
        value=[{'name': 'Name', 'wohnungen': [{'stockwerk': '1OG'}]}]
    )
    add_field(name='art-der-anlage', value=['Solaranlage', 'Antennen'])
    add_field(name='art-der-befestigten-flache', value='Lagerplatz')

    response = admin_client.post(url)
    assert response.status_code == status_code

    if status_code == status.HTTP_200_OK:
        json = response.json()
        assert json['data']['attributes']['identifier'] == '11-17-001'
        assert set(json['data']['meta']['editable']) == set()

        instance.refresh_from_db()
        assert instance.instance_state.name == 'subm'


@pytest.mark.parametrize("role__name", ['Canton'])
def test_instance_export(admin_client, user, instance_factory,
                         django_assert_num_queries):
    url = reverse('instance-export')
    instances = instance_factory.create_batch(2, user=user)

    with django_assert_num_queries(7):
        response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    book = pyexcel.get_book(
        file_content=response.content, file_type='xlsx'
    )
    # bookdict is a dict of tuples(name, content)
    sheet = book.bookdict.popitem()[1]
    assert len(sheet) == len(instances)


@pytest.mark.freeze_time('2017-7-27')
@pytest.mark.parametrize("location__communal_federal_number", [
    '1311',
])
def test_instance_generate_identifier(db, instance, instance_factory):
    instance_factory(identifier='11-17-010')
    serializer = serializers.InstanceSubmitSerializer(instance)
    identifier = serializer.generate_identifier()

    assert identifier == '11-17-011'
