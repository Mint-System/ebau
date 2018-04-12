from django.conf import settings
from django.utils.translation import gettext as _
from django_clamd.validators import validate_file_infection
from rest_framework import exceptions
from rest_framework.compat import unicode_to_repr
from rest_framework_json_api import serializers

from camac.instance.mixins import InstanceEditableMixin
from camac.relations import FormDataResourceRelatedField
from camac.user.relations import GroupFormDataResourceRelatedField
from camac.user.serializers import CurrentGroupDefault

from . import models


class AttachmentSectionSerializer(serializers.ModelSerializer):
    mode = serializers.SerializerMethodField()

    def get_mode(self, instance):
        request = self.context['request']
        return instance.get_mode(request.group)

    class Meta:
        model = models.AttachmentSection
        meta_fields = (
            'mode',
        )
        fields = (
            'name',
        )


class AttachmentSectionDefault(object):
    """First availbale attachment section of current group."""

    def set_context(self, serializer_field):
        self.group = serializer_field.context['request'].group

    def __call__(self):
        return models.AttachmentSection.objects.filter_group(
            self.group).first()

    def __repr__(self):
        return unicode_to_repr('%s()' % self.__class__.__name__)


class AttachmentSerializer(InstanceEditableMixin,
                           serializers.ModelSerializer):
    serializer_related_field = FormDataResourceRelatedField

    user = FormDataResourceRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    group = GroupFormDataResourceRelatedField(default=CurrentGroupDefault())
    attachment_section = FormDataResourceRelatedField(
        queryset=models.AttachmentSection.objects.all(),
        default=AttachmentSectionDefault()
    )

    def validate_attachment_section(self, attachment_section):
        mode = attachment_section.get_mode(self.context['request'].group)
        if mode not in [models.WRITE_PERMISSION, models.ADMIN_PERMISSION]:
            raise exceptions.ValidationError(
                _('Not sufficent permissions to add file to '
                  'section %(section)s.') % {
                    'section': attachment_section.name
                }
            )

        return attachment_section

    def validate_path(self, path):
        if path.content_type not in settings.ALLOWED_DOCUMENT_MIMETYPES:
            raise exceptions.ParseError(
                _('%(mime_type)s is not a valid mime type for attachment.') % {
                    'mime_type': path.content_type
                }
            )

        validate_file_infection(path)

        return path

    def validate(self, data):
        path = data['path']
        data['size'] = path.size
        data['mime_type'] = path.content_type
        data['name'] = path.name
        return data

    included_serializers = {
        'user': 'camac.user.serializers.UserSerializer',
        'instance': 'camac.instance.serializers.InstanceSerializer',
        'attachment_section': AttachmentSectionSerializer,
    }

    class Meta:
        model = models.Attachment
        fields = (
            'attachment_section',
            'date',
            'digital_signature',
            'instance',
            'is_confidential',
            'is_parcel_picture',
            'mime_type',
            'name',
            'path',
            'size',
            'user',
            'group',
        )
        read_only_fields = (
            'date',
            'mime_type',
            'name',
            'size',
            'user',
        )


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Template
        fields = (
            'name',
        )
