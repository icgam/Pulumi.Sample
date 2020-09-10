from datetime import datetime, timedelta
from enum import Enum
from typing import Dict
from pulumi_random import RandomPassword
from pulumi_azuread import Application, ServicePrincipal, ApplicationPassword
from dataclasses import dataclass
from context import Context
from app_permissions import create_permission
from app_owners import app_owners
from app_claims import default_claims

DEFAULT_DOMAIN = 'domain.com'


class AppType(Enum):
    API = 1
    WEB = 2
    APP = 3


@dataclass
class CompositeAppDefinition:
    title: str
    name: str
    business: str
    required_permissions: list
    optional_claims: dict
    local_api_port: int
    local_web_port: int
    domain: str = DEFAULT_DOMAIN

    def add_permissions(self, permissions: list):
        for permission in permissions:
            self.required_permissions.append(permission)

    def add_claims(self, claims: dict):
        for (k, v) in claims.items():
            self.optional_claims[k] = v


@dataclass
class AppDefinition:
    title: str
    name: str
    business: str
    required_permissions: list
    optional_claims: dict
    local_url: str
    app_type: AppType
    domain: str = DEFAULT_DOMAIN

    def add_permissions(self, permissions: list):
        for permission in permissions:
            self.required_permissions.append(permission)

    def add_claims(self, claims: dict):
        for (k, v) in claims.items():
            self.optional_claims[k] = v


@dataclass
class AppRegistration:
    app: Application
    sp: ServicePrincipal


class AppDefinitionBuilder:

    @staticmethod
    def build(title: str, name: str, business: str, local_url: str, app_type: AppType, domain: str = DEFAULT_DOMAIN):
        definition = AppDefinition(title=title,
                                   name=name,
                                   business=business,
                                   local_url=local_url,
                                   app_type=app_type,
                                   domain=domain,
                                   required_permissions=[],
                                   optional_claims=default_claims())
        return definition

    @staticmethod
    def build_composite(title: str, name: str, business: str, local_api_port: int = 5000, local_web_port: int = 4200, domain: str = DEFAULT_DOMAIN):
        definition = CompositeAppDefinition(title=title,
                                            name=name,
                                            business=business,
                                            local_api_port=local_api_port,
                                            local_web_port=local_web_port,
                                            domain=domain,
                                            required_permissions=[],
                                            optional_claims=default_claims())
        return definition


class AppBuilder:
    _environments: Dict[str, str] = {
        "int": "int.",
        "uat": "uat.",
        "prod": ""
    }

    _api_end_points = ("", "swagger/oauth2-redirect.html")
    _web_end_points = ("", "signin-oidc")

    @staticmethod
    def create_app(app_definition: AppDefinition, context: Context) -> AppRegistration:
        app_builder = AppBuilder()
        return app_builder._create_app(app_definition, context)

    @staticmethod
    def create_composite_app(app_definition: CompositeAppDefinition, context: Context) -> Dict[str, AppRegistration]:
        app_builder = AppBuilder()
        api_definition = AppDefinitionBuilder.build(title=f"{app_definition.title} API",
                                                    name=app_definition.name,
                                                    business=app_definition.business,
                                                    local_url=f"http://localhost:{app_definition.local_api_port}",
                                                    domain=app_definition.domain,
                                                    app_type=AppType.API)
        api_definition.add_permissions(app_definition.required_permissions)
        api = app_builder._create_app(api_definition, context)

        web_definition = AppDefinitionBuilder.build(title=f"{app_definition.title} Web",
                                                    name=app_definition.name,
                                                    business=app_definition.business,
                                                    local_url=f"http://localhost:{app_definition.local_web_port}",
                                                    domain=app_definition.domain,
                                                    app_type=AppType.WEB)

        permission = create_permission(api.app)
        web_definition.add_permissions([permission])
        web_definition.add_permissions(app_definition.required_permissions)
        web = app_builder._create_app(web_definition, context)

        return {"web": web, "api": api}

    @staticmethod
    def create_app_secret(app: Application, purpose: str, expiry_duration_in_days=365):
        secret = RandomPassword("password", length=16, override_special="_%@", special=True)

        expiry = (datetime.utcnow() + timedelta(days=expiry_duration_in_days)).isoformat() + "Z"  # TODO: Hack
        password = ApplicationPassword("app_password",
                                       application_object_id=app.object_id,
                                       description=purpose,
                                       value=secret.result,
                                       end_date=expiry)

        return password

    def _create_app(self, app_definition: AppDefinition, context: Context) -> AppRegistration:
        name_prefix = f"{app_definition.name}.api" if app_definition.app_type == AppType.API else app_definition.name
        end_points = self._api_end_points if app_definition.app_type == AppType.API else self._web_end_points

        env = self._environments.get(context.execution_context.stack)
        app_urls = []

        if env is None:
            env = context.execution_context.stack + "."
            app_urls.append(app_definition.local_url)

        identifier_url = f"https://{name_prefix}.{app_definition.business}.{env}{app_definition.domain}"
        app_urls.append(identifier_url)

        reply_urls = [f"{url}/{ep}" for url in app_urls for ep in end_points]

        app = Application(f"{app_definition.title}-{context.execution_context.stack}",
                          available_to_other_tenants=False,
                          group_membership_claims="SecurityGroup",
                          homepage=identifier_url,
                          name=f"{app_definition.title}-{context.execution_context.stack}",
                          oauth2_allow_implicit_flow=True,
                          identifier_uris=[identifier_url],
                          reply_urls=reply_urls,
                          oauth2_permissions=[
                              {
                                  "adminConsentDescription": f"Allow the application to access {app_definition.title} on behalf of the signed-in user.",
                                  "adminConsentDisplayName": f"Access {app_definition.title}",
                                  "isEnabled": True,
                                  "type": "User",
                                  "userConsentDescription": f"Allow the application to access {app_definition.title} on your behalf.",
                                  "userConsentDisplayName": f"Access {app_definition.title}",
                                  "value": "user_impersonation",
                              }
                          ],
                          required_resource_accesses=app_definition.required_permissions,
                          optional_claims=app_definition.optional_claims
                          )

        sp = ServicePrincipal(f"{app_definition.title}-{context.execution_context.stack} - ServicePrincipal",
                              application_id=app.application_id,
                              app_role_assignment_required=False)

        return AppRegistration(app=app, sp=sp)
