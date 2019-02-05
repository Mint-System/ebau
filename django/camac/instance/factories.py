from datetime import timedelta
from random import randrange

import pytz
from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from camac.user.factories import (
    GroupFactory,
    LocationFactory,
    ServiceFactory,
    UserFactory,
)

from . import models


class FormStateFactory(DjangoModelFactory):
    name = Faker("name")

    class Meta:
        model = models.FormState


class FormFactory(DjangoModelFactory):
    name = Faker("name")
    description = Faker("text")
    form_state = SubFactory(FormStateFactory)

    class Meta:
        model = models.Form


class InstanceStateFactory(DjangoModelFactory):
    name = Faker("name")
    sort = 0

    class Meta:
        model = models.InstanceState


class InstanceFactory(DjangoModelFactory):
    identifier = None
    instance_state = SubFactory(InstanceStateFactory)
    previous_instance_state = SubFactory(InstanceStateFactory)
    form = SubFactory(FormFactory)
    user = SubFactory(UserFactory)
    group = SubFactory(GroupFactory)
    location = SubFactory(LocationFactory)
    creation_date = Faker("past_datetime", tzinfo=pytz.UTC)
    modification_date = Faker("past_datetime", tzinfo=pytz.UTC)

    class Meta:
        model = models.Instance


class FormFieldFactory(DjangoModelFactory):
    instance = SubFactory(InstanceFactory)
    name = Faker("name")
    value = Faker("name")

    class Meta:
        model = models.FormField


class InstanceResponsibilityFactory(DjangoModelFactory):
    service = SubFactory(ServiceFactory)
    user = SubFactory(UserFactory)
    instance = SubFactory(InstanceFactory)

    class Meta:
        model = models.InstanceResponsibility


class JournalEntryFactory(DjangoModelFactory):
    instance = SubFactory(InstanceFactory)
    user = SubFactory(UserFactory)
    group = SubFactory(GroupFactory)
    service = SubFactory(ServiceFactory)
    creation_date = Faker("past_datetime", tzinfo=pytz.UTC)
    modification_date = Faker("past_datetime", tzinfo=pytz.UTC)
    text = Faker("text")
    duration = timedelta(0)

    class Meta:
        model = models.JournalEntry


class IssueFactory(DjangoModelFactory):
    instance = SubFactory(InstanceFactory)
    user = SubFactory(UserFactory)
    group = SubFactory(GroupFactory)
    service = SubFactory(ServiceFactory)
    deadline_date = Faker("future_date")
    text = Faker("text")
    state = models.Issue.STATE_OPEN

    class Meta:
        model = models.Issue


class IssueTemplateFactory(DjangoModelFactory):
    instance = SubFactory(InstanceFactory)
    user = SubFactory(UserFactory)
    group = SubFactory(GroupFactory)
    service = SubFactory(ServiceFactory)
    deadline = randrange(1, 10)
    text = Faker("text")

    class Meta:
        model = models.IssueTemplate


class IssueTemplateSetFactory(DjangoModelFactory):
    instance = SubFactory(InstanceFactory)
    group = SubFactory(GroupFactory)
    service = SubFactory(ServiceFactory)
    name = Faker("sentence")

    class Meta:
        model = models.IssueTemplateSet


class IssueTemplateSetIssueTemplateFactory(DjangoModelFactory):
    issue_template = SubFactory(IssueTemplateFactory)
    issue_template_set = SubFactory(IssueTemplateSetFactory)

    class Meta:
        model = models.IssueTemplateSetIssueTemplate
