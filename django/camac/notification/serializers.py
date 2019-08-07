import itertools
from collections import namedtuple
from datetime import date, timedelta
from html import escape
from logging import getLogger

import inflection
import jinja2
import requests
from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header
from rest_framework_json_api import serializers

from camac.core.models import Activation
from camac.instance.mixins import InstanceEditableMixin
from camac.instance.models import Instance
from camac.user.models import Service

from ..core import models as core_models
from . import models

request_logger = getLogger("django.request")


class NoticeMergeSerializer(serializers.Serializer):
    service = serializers.StringRelatedField(source="activation.service")
    notice_type = serializers.StringRelatedField()
    content = serializers.CharField()


class ActivationMergeSerializer(serializers.Serializer):
    deadline_date = serializers.DateTimeField(format=settings.MERGE_DATE_FORMAT)
    start_date = serializers.DateTimeField(format=settings.MERGE_DATE_FORMAT)
    end_date = serializers.DateTimeField(format=settings.MERGE_DATE_FORMAT)
    circulation_state = serializers.StringRelatedField()
    service = serializers.StringRelatedField()
    reason = serializers.CharField()
    circulation_answer = serializers.StringRelatedField()
    notices = NoticeMergeSerializer(many=True)


class BillingEntryMergeSerializer(serializers.Serializer):
    amount = serializers.FloatField()
    service = serializers.StringRelatedField()
    created = serializers.DateTimeField(format=settings.MERGE_DATE_FORMAT)
    account = serializers.SerializerMethodField()
    account_number = serializers.SerializerMethodField()

    def get_account(self, billing_entry):
        billing_account = billing_entry.billing_account
        return "{0} / {1}".format(billing_account.department, billing_account.name)

    def get_account_number(self, billing_entry):
        return billing_entry.billing_account.account_number


class InstanceMergeSerializer(InstanceEditableMixin, serializers.Serializer):
    """Converts instance into a dict to be used with template merging."""

    # TODO: document.Template and notification.NotificationTemplate should
    # be moved to its own app template including this serializer.

    location = serializers.StringRelatedField()
    identifier = serializers.CharField()
    activations = ActivationMergeSerializer(many=True)
    billing_entries = BillingEntryMergeSerializer(many=True)
    answer_period_date = serializers.SerializerMethodField()
    publication_date = serializers.SerializerMethodField()
    instance_id = serializers.IntegerField()
    public_dossier_link = serializers.SerializerMethodField()
    internal_dossier_link = serializers.SerializerMethodField()
    active_municipality_name = serializers.SerializerMethodField()
    leitbehoerde_name = serializers.SerializerMethodField(
        method_name="get_active_municipality_name"
    )
    form_name = serializers.SerializerMethodField(method_name="get_form_name")

    def __init__(self, instance, *args, escape=False, **kwargs):
        self.escape = escape
        instance.activations = Activation.objects.filter(circulation__instance=instance)
        super().__init__(instance, *args, **kwargs)

    def _escape(self, data):
        result = data
        if isinstance(data, str):
            result = escape(data)
        elif isinstance(data, list):
            result = [self._escape(value) for value in data]
        elif isinstance(data, dict):
            result = {key: self._escape(value) for key, value in data.items()}

        return result

    def get_answer_period_date(self, instace):
        answer_period_date = date.today() + timedelta(days=settings.MERGE_ANSWER_PERIOD)
        return answer_period_date.strftime(settings.MERGE_DATE_FORMAT)

    def get_publication_date(self, instance):
        publication_entry = instance.publication_entries.first()

        return (
            publication_entry
            and publication_entry.publication_date.strftime(settings.MERGE_DATE_FORMAT)
            or ""
        )

    def get_active_municipality_name(self, instance):
        instance_service = core_models.InstanceService.objects.filter(
            instance=instance, active=1
        ).first()
        if not instance_service:
            return "-"
        return instance_service.service.name

    def get_form_name(self, instance):
        if settings.APPLICATION["FORM_BACKEND"] == "camac-ng":
            return instance.form.get_name()
        try:
            caluma_resp = requests.post(
                settings.CALUMA_URL,
                json={
                    "query": """,
                        query {
                          allDocuments(metaValue: [{ key: "camac-instance-id", value: $instance_id}]) {
                            edges {
                              node {
                                id
                                form {
                                  name
                                  meta
                                }
                              }
                            }
                          }
                        }
                    """,
                    "variables": {"instance_id": instance.pk},
                },
                headers={
                    "Authorization": get_authorization_header(self.context["request"])
                },
            )
            documents = caluma_resp.json()["data"]["allDocuments"]["edges"]
            form_names = [
                doc["node"]["form"]["name"]
                for doc in documents
                if doc["node"]["form"]["meta"]["is-main-form"] is True
            ]
            return form_names[0]
        except (KeyError, IndexError):  # pragma: no cover
            request_logger.error(
                "get_form_name(): Caluma did not respond with a valid response"
            )
            return "-"

    def get_internal_dossier_link(self, instance):
        return self._get_dossier_link(instance, "INTERNAL")

    def get_public_dossier_link(self, instance):
        return self._get_dossier_link(instance, "PUBLIC")

    def _get_dossier_link(self, instance, mode):
        template = settings.INSTANCE_URL_TEMPLATE[mode]

        path = self._str_replace_cb("{base_url}", self._make_base_url, template)
        path = path.replace("{instance_id}", str(instance.pk))

        return path

    def _make_base_url(self):
        try:
            rq = self.context["request"]._request
            return f"{rq.scheme}://{rq.get_host()}"
        except KeyError:
            request_logger.error("get_dossier_link(): Cannot get base URL from request")
            return "??"

    def _str_replace_cb(self, pattern, callback, string):
        """str.replace(), but with a callback.

        This is here so we can do "lazy" string replacing, so the replacement
        value only needs to be calculated if really needed.
        """
        if pattern not in string:
            return string
        value = callback()
        return string.replace(pattern, value)

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        for field in instance.fields.all():
            name = inflection.underscore("field-" + field.name)
            ret[name] = field.value

        if self.escape:
            ret = self._escape(ret)

        return ret


class IssueMergeSerializer(serializers.Serializer):
    deadline_date = serializers.DateField()
    text = serializers.CharField()

    def to_representation(self, issue):
        ret = super().to_representation(issue)

        # include instance merge fields
        ret.update(InstanceMergeSerializer(issue.instance, context=self.context).data)

        return ret


class NotificationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NotificationTemplate
        fields = ("purpose", "subject", "body")


class NotificationTemplateMergeSerializer(
    InstanceEditableMixin, serializers.Serializer
):
    instance_editable_permission = None
    """
    No specific permission needed to send notificaion
    """

    instance = serializers.ResourceRelatedField(queryset=Instance.objects.all())
    notification_template = serializers.ResourceRelatedField(
        queryset=models.NotificationTemplate.objects.all()
    )
    subject = serializers.CharField(required=False)
    body = serializers.CharField(required=False)

    def _merge(self, value, instance):
        try:
            value_template = jinja2.Template(value)
            data = InstanceMergeSerializer(instance, context=self.context).data

            # some cantons use uppercase placeholders. be as compatible as possible
            data.update({k.upper(): v for k, v in data.items()})
            return value_template.render(data)
        except jinja2.TemplateError as e:
            raise exceptions.ValidationError(str(e))

    def validate(self, data):
        notification_template = data["notification_template"]
        instance = data["instance"]

        subj_prefix = settings.EMAIL_PREFIX_SUBJECT
        body_prefix = settings.EMAIL_PREFIX_BODY

        data["subject"] = subj_prefix + self._merge(
            data.get("subject", notification_template.get_trans_attr("subject")),
            instance,
        )
        data["body"] = body_prefix + self._merge(
            data.get("body", notification_template.get_trans_attr("body")), instance
        )
        data["pk"] = "{0}-{1}".format(notification_template.pk, instance.pk)

        return data

    def create(self, validated_data):
        NotificationTemplateMerge = namedtuple(
            "NotificationTemplateMerge", validated_data.keys()
        )
        obj = NotificationTemplateMerge(**validated_data)

        return obj

    class Meta:
        resource_name = "notification-template-merges"


class NotificationTemplateSendmailSerializer(NotificationTemplateMergeSerializer):
    recipient_types = serializers.MultipleChoiceField(
        choices=(
            "applicant",
            "municipality",
            "service",
            "leitbehoerde",
            "construction_control",
        )
    )

    def _get_recipients_applicant(self, instance):
        return [instance.user.email]

    def _get_recipients_leitbehoerde(self, instance):  # pragma: no cover
        instance_service = core_models.InstanceService.objects.filter(
            instance=instance, service__service_group__name="municipality", active=1
        ).first()
        if not instance_service:
            return []
        return [instance_service.service.email]

    def _get_recipients_municipality(self, instance):
        return [instance.group.service.email]

    def _get_recipients_service(self, instance):
        services = Service.objects.filter(
            pk__in=instance.circulations.values("activations__service")
        )

        return [service.email for service in services]

    def _get_recipients_construction_control(self, instance):
        return core_models.InstanceService.objects.filter(
            instance=instance,
            service__service_group__name="construction-control",
            active=1,
        ).values_list("service__email", flat=True)

    def create(self, validated_data):
        instance = validated_data["instance"]
        recipients = itertools.chain(
            *[
                getattr(self, "_get_recipients_%s" % recipient_type)(instance)
                for recipient_type in validated_data["recipient_types"]
            ]
        )

        email = EmailMessage(
            subject=validated_data["subject"],
            body=validated_data["body"],
            bcc=set(recipients),
        )

        return email.send()

    class Meta:
        resource_name = "notification-template-sendmails"
