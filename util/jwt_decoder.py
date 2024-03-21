import jwt


def decode_token(token):
    """Decodes a JWT token.

    Args:
      token (str): The JWT token to decode.

    Returns:
      dict: The decoded JWT payload.
    """
    # Decode the token using the HS256 algorithm.
    payload = jwt.decode(token, "secret", algorithms=['HS256'])

    # Return the decoded payload.
    return payload


def main(token):
    # Decode the token.
    payload = decode_token(token)

    # Print the decoded payload.
    print(payload)


if __name__ == "__main__":
    input_token = "7nOrRdx3T/x/NgaC7UJoc6fhV0U555QquVV2wRzkoTBnjjAhofPB2wNbTNIBRK9TWdPIEgnZ0jgf+L4lEFyhLxn2eiqMbogaO/JguR7ychVRWEvkC7YNo3hHmUxcey9aEEaci90At6Hd06d+GayDppbxZUTUM7KAXblWvnoyGrb96aFyUT0Gh4rIeJIooWIQAyn1yuVIi2Czw5V+7FeHUtqW1whey5hAxoCUYQNx9QgEQYE/zOSHCJbAUyOKPqEl919P2Ql6LlI4IZF1BeqCmaeprtogjFpUFsMF0Nn5wd2EtXyTMDzADSGjxGqZXKQhcTlOvopPsin0kxx6vBHqwZ14eTJg4yFtfj5ljp8u7JO6UivSDkGi1Ogs6lpcGAdVGQrqAOZbwbZx2Ph4mqZAUVdOUT10QEjQI+07CVVpChPnUH6EQ3cUv3LHrCXVX5vr/O7eMCqG38XuJ7X9Jl6pvBZXA35wF9JSzNmfRPLyI3D6HZRFHQrpNou62TgF41bsQ4/msPLX56a2R/pMvvGcEmp07H4V0tYxdYhaaF8KWEJQxATez7CiC1OL28XHK0rE"
    main(input_token)
