from pulumi import Output
from pulumi_azuread import Application


_all_permissions = {
    "graph_api_basic": {
        "resourceAppId": "00000003-0000-0000-c000-000000000000",
        "resourceAccess": [
            {
                "id": "e1fe6dd8-ba31-4d61-89e7-88639da4683d",
                "type": "Scope"
            }
        ]},
    "graph_api_extended": {
        "resourceAppId": "00000003-0000-0000-c000-000000000000",
        "resourceAccess": [
            {
                "id": "e1fe6dd8-ba31-4d61-89e7-88639da4683d",
                "type": "Scope"
            },
            {
                "id": "64a6cdd6-aab1-4aaf-94b8-3cc8405e90d0",
                "type": "Scope"
            },
            {
                "id": "7427e0e9-2fba-42fe-b0c0-848c9e6a8182",
                "type": "Scope"
            },
            {
                "id": "37f7f235-527c-4136-accd-4a02d197296e",
                "type": "Scope"
            },
            {
                "id": "14dad69e-099b-42c9-810b-d002981feec1",
                "type": "Scope"
            },
            {
                "id": "5f8c59db-677d-491f-a6b8-5f174b11ec1d",
                "type": "Scope"
            },
            {
                "id": "b340eb25-3456-403f-be2f-af7a0d370277",
                "type": "Scope"
            }
        ]
    },
    "blob_storage": {
        "resourceAppId": "e406a681-f3d4-42a8-90b6-c2b029497af1",
        "resourceAccess": [
            {
                "id": "03e0da56-190b-40ad-a80c-ea378c433f7f",
                "type": "Scope"
            }
        ]}

}


def all_permissions() -> list:
    return [_all_permissions["graph_api_extended"], _all_permissions["blob_storage"]]


def default_permissions() -> list:
    return [_all_permissions["graph_api_basic"]]


def create_permission(app: Output[Application]) -> Output:
    return Output.all(app.application_id, app.oauth2_permissions).apply(lambda args: {
        "resourceAppId": args[0],
        "resourceAccess": [
            {
                "id": args[1][0]["id"],
                "type": "Scope"
            }
        ]
    })
