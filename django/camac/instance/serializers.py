from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework import exceptions
from rest_framework_json_api import serializers

from camac.user.models import Location
from camac.user.serializers import CurrentGroupDefault

from . import models


class NewInstanceStateDefault(object):
    def __call__(self):
        # TODO: change to new instance state
        return models.InstanceState.objects.first()


class InstanceStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InstanceState
        fields = (
            'name',
        )


class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Form
        fields = (
            'name',
            'description',
        )


class InstanceSerializer(serializers.ModelSerializer):
    group = serializers.ResourceRelatedField(
        read_only=True, default=CurrentGroupDefault()
    )

    user = serializers.ResourceRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    location = serializers.ResourceRelatedField(
        queryset=Location.objects.all(), required=True
    )

    creation_date = serializers.DateTimeField(
        read_only=True, default=timezone.now
    )

    modification_date = serializers.DateTimeField(default=timezone.now)

    instance_state = serializers.ResourceRelatedField(
        read_only=True, default=NewInstanceStateDefault()
    )

    previous_instance_state = serializers.ResourceRelatedField(
        read_only=True, default=NewInstanceStateDefault()
    )

    included_serializers = {
        'location': 'camac.user.serializers.LocationSerializer',
        'user': 'camac.user.serializers.UserSerializer',
        'group': 'camac.user.serializers.GroupSerializer',
        'form': FormSerializer,
        'instance_state': InstanceStateSerializer,
        'previous_instance_state': InstanceStateSerializer,
    }

    def validate_modification_date(self, value):
        return timezone.now()

    class Meta:
        model = models.Instance
        fields = (
            'instance_state',
            'identifier',
            'location',
            'form',
            'user',
            'group',
            'creation_date',
            'modification_date',
            'previous_instance_state'
        )
        read_only_fields = (
            'identifier',
        )


class FormFieldSerializer(serializers.ModelSerializer):

    def validate_instance(self, value):
        request = self.context['request']

        if request.user != value.user:
            raise exceptions.ValidationError(
                _('Instance does not belong to requesting user.')
            )

        return value

    included_serializers = {
        'instance': InstanceSerializer,
    }

    class Meta:
        model = models.FormField
        fields = (
            'name',
            'value',
            'instance'
        )
