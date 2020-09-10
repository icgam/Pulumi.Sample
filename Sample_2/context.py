import logging
from dataclasses import dataclass, asdict
from datetime import datetime

import pulumi
from cerberus.validator import Validator
from pulumi_azure import core


EXECUTION_CONTEXT_SCHEMA = {
    'region': {'type': 'string', 'empty': False},
    'platform': {'type': 'string', 'empty': False},
    'stack': {'type': 'string', 'empty': False},
    'project': {'type': 'string', 'empty': False},
    'subscription_id': {'type': 'string', 'empty': False},
    'last_modified_on': {'type': 'datetime'},
}

AZURE_CONTEXT_SCHEMA = {
    'tenant_id': {'type': 'string', 'empty': False},
    'service_principal_id': {'type': 'string', 'empty': False},
    'subscription_id': {'type': 'string', 'empty': False}
}


@dataclass
class ExecutionContext:
    region: str
    platform: str
    stack: str
    project: str
    subscription_id: str
    last_modified_on: datetime


@dataclass
class AzureContext:
    tenant_id: str
    service_principal_id: str
    subscription_id: str


@dataclass
class Context:
    execution_context: ExecutionContext
    azure_context: AzureContext


def _get_execution_context(subscription_id) -> ExecutionContext:
    logging.basicConfig(level=logging.DEBUG)
    location = pulumi.config.get_config('azure:location')
    platform = pulumi.config.get_config('platform:name')
    project = pulumi.get_project()
    stack = pulumi.get_stack()
    context = ExecutionContext(
        location,
        platform,
        stack,
        project,
        subscription_id,
        datetime.now()
    )

    v = Validator(EXECUTION_CONTEXT_SCHEMA, require_all=True)
    if not v.validate(asdict(context)):
        raise Exception(v.errors)

    return context


def _get_azure_context() -> AzureContext:
    client_config = core.get_client_config()

    context = AzureContext(
        client_config.tenant_id,
        client_config.object_id,
        client_config.subscription_id
    )

    v = Validator(AZURE_CONTEXT_SCHEMA, require_all=True)
    if not v.validate(asdict(context)):
        raise Exception(v.errors)

    return context


def get_context() -> Context:
    primary = core.get_subscription()
    context = Context(
        execution_context=_get_execution_context(primary.id),
        azure_context=_get_azure_context())
    return context
