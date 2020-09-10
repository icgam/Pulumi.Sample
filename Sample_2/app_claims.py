
def optional_claims() -> dict:
    return {
        "idToken": [
            {
                "name": "upn",
                "source": None,
                "essential": False,
                "additionalProperties": []
            },
            {
                "name": "family_name",
                "source": None,
                "essential": False,
                "additionalProperties": []
            },
            {
                "name": "email",
                "source": None,
                "essential": False,
                "additionalProperties": []
            },
            {
                "name": "given_name",
                "source": None,
                "essential": False,
                "additionalProperties": []
            },
            {
                "name": "groups",
                "source": None,
                "essential": False,
                "additionalProperties": [
                    "sam_account_name",
                    "emit_as_roles"
                ]
            }
        ],
        "accessToken": [
            {
                "name": "groups",
                "source": None,
                "essential": False,
                "additionalProperties": [
                    "sam_account_name",
                    "emit_as_roles"
                ]
            }
        ]
    }


def default_claims() -> dict:
    return {
        "idToken": [
            {
                "name": "upn",
                "source": None,
                "essential": False,
                "additionalProperties": []
            },
            {
                "name": "email",
                "source": None,
                "essential": False,
                "additionalProperties": []
            }
        ],
        "accessToken": [
        ]
    }
