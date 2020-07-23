from pulumi import Output
from pulumi_azuread import Application


_all_permissions = {
    "graph_api": {
        "resourceAppId": "00000003-0000-0000-c000-000000000000",
        "resourceAccess": [
            {
                "id": "e1fe6dd8-ba31-4d61-89e7-88639da4683d",
                "type": "Scope"
            }
        ]},
    'blob_storage': {
        "resourceAppId": "e406a681-f3d4-42a8-90b6-c2b029497af1",
        "resourceAccess": [
            {
                "id": "03e0da56-190b-40ad-a80c-ea378c433f7f",
                "type": "Scope"
            }
        ]}

}


def all_permissions() -> dict:
    return _all_permissions


def default_permissions() -> list:
    return [_all_permissions["graph_api"]]


def create_permission(app: Output[Application]):
    # permission = app.oauth2_permissions[0].apply(lambda x: {"id": x["id"], "value": x["value"]})
    permission = app.oauth2_permissions[0]

    return {
        "resourceAppId": app.application_id,
        "resourceAccess": [
            {
                "id": permission["id"],
                "type": "Scope"
            }
        ]
    }
