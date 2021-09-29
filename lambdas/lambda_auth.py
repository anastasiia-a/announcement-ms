MOCK_TOKEN = "allow"
PRINCIPAL_ID = "user"


def generate_policy_document(effect, method_arn):
    """
    The following policy statement gives the user permission to call
    method along the path of 'method_arn' resource.
    """
    if all([effect, method_arn]):
        policy_document = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": method_arn,
                }
            ],
        }
        return policy_document

    return None


def generate_auth_response(principal_id, effect, method_arn):
    policy_document = generate_policy_document(effect, method_arn)
    return {"principalId": principal_id, "policyDocument": policy_document}


def lambda_handler(event, context):
    """
    Mock token authorization.
    Allows a request if there is a MOCK_TOKEN in the header.
    """
    token = event.get("authorizationToken")
    method_arn = event.get("methodArn")

    if token == MOCK_TOKEN:
        return generate_auth_response(PRINCIPAL_ID, "Allow", method_arn)
    else:
        return generate_auth_response(PRINCIPAL_ID, "Deny", method_arn)
