def authorize():
    query_parm = {
        "client_id": "",
        "response_type": "code",
        "response_mode": "form_post",
        "scope": "openid profile phone email address",
        "redirect_uri": "{baseUrl}/api/v1/EmployeeAuth/callback-authorize-okta",
    "state": "",
    }
