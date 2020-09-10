_users = {
}

_owners = {
    "int": [
    ],
    "uat": [
    ],
    "prod": [
    ]
}


def app_owners(env: str):
    owners = _owners.get(env)
    if owners is None:
        owners = _owners.get("int")
    return owners
