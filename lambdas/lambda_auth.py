def generate_policy_document(effect, method_arn):
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
    token = event.get("authorizationToken")
    method_arn = event.get("methodArn")
    http_method = event.get("httpMethod")

    if token == "allow" or http_method == "GET":
        return generate_auth_response("user", "Allow", method_arn)
    else:
        return generate_auth_response("user", "Deny", method_arn)
