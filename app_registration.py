from datetime import datetime, timedelta
from pulumi_random import RandomPassword
from pulumi_azuread import Application, ServicePrincipal, ApplicationPassword
from dataclasses import dataclass

from .app_permissions import default_permissions, create_permission


class CompositeAppDefinition:
    title: str
    name: str
    business: str
    required_permissions: list
    local_url: str = 'http://localhost:5000'
    domain: str = 'icgplc.com'

    def __init__(self, title: str, name: str, business: str):
        self.title = title
        self.name = name
        self.business = business
        self.required_permissions = default_permissions()

    def add_permission(self, permission):
        self.required_permissions.append(permission)


class AppDefinition:
    title: str
    name: str
    business: str
    required_permissions: list
    local_url: str = 'http://localhost:5000'
    domain: str = 'icgplc.com'
    is_api: bool

    def __init__(self, title: str, name: str, business: str, is_api: bool = True):
        self.title = title
        self.name = name
        self.business = business
        self.required_permissions = default_permissions()
        self.is_api = is_api

    def add_permission(self, permission):
        self.required_permissions.append(permission)


@dataclass
class AppRegistration:
    app: Application
    sp: ServicePrincipal


_environments: dict = {
    "int": "int.",
    "uat": "uat.",
    "prod": ""
}

_api_end_points = ("", "swagger/oauth2-redirect.html")
_web_end_points = ("", "signin-oidc")


def create_composite_app(appDefinition: CompositeAppDefinition):
    api_definition = AppDefinition(title=f"{appDefinition.title} API", name=appDefinition.name, business=appDefinition.business)
    api = create_app(api_definition)

    web_definition = AppDefinition(title=f"{appDefinition.title} Web", name=appDefinition.name, business=appDefinition.business, is_api=False)
    web = create_app(web_definition)

    return {"web": web, "api": api}


def create_app(appDefinition: AppDefinition) -> AppRegistration:
    name_prefix = f"{appDefinition.name}.api" if appDefinition.is_api else appDefinition.name
    end_points = _api_end_points if appDefinition.is_api else _web_end_points

    appUrls = [f"http://{name_prefix}.{appDefinition.business}.{_environments[env]}{appDefinition.domain}" for env in _environments]
    appUrls.append(appDefinition.local_url)

    replyUrls = [f"{url}/{ep}" for url in appUrls for ep in end_points]

    app = Application(appDefinition.title,
                      available_to_other_tenants=False,
                      homepage=appUrls[2],
                      name=appDefinition.title,
                      oauth2_allow_implicit_flow=True,
                      identifier_uris=[appUrls[2]],
                      reply_urls=replyUrls,
                      oauth2_permissions=[
                          {
                              "adminConsentDescription": f"Allow the application to access {appDefinition.title} on behalf of the signed-in user.",
                              "adminConsentDisplayName": f"Access {appDefinition.title}",
                              "isEnabled": True,
                              "type": "User",
                              "userConsentDescription": f"Allow the application to access {appDefinition.title} on your behalf.",
                              "userConsentDisplayName": f"Access {appDefinition.title}",
                              "value": "user_impersonation",
                          }
                      ],
                      required_resource_accesses=appDefinition.required_permissions
                      )

    sp = ServicePrincipal(f"{appDefinition.title} - ServicePrincipal",
                          application_id=app.application_id,
                          app_role_assignment_required=False)

    return AppRegistration(app=app, sp=sp)


def create_app_secret(app: Application, purpose: str, expiry_duration_in_days=365):
    secret = RandomPassword("password", length=16, override_special="_%@", special=True)

    expiry = (datetime.utcnow() + timedelta(days=expiry_duration_in_days)).isoformat() + "Z"  # TODO: Hack
    password = ApplicationPassword("app_password",
                                   application_object_id=app.object_id,
                                   description=purpose,
                                   value=secret,
                                   end_date=expiry)

    return password
