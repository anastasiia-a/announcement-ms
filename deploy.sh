virtualvenv venv && source venv/bin/activate
pip install -r requirements.txt
cp -rp venv/lib/python*/site-packages/ lambdas/

aws s3 mb s3://${S3_BUCKET}

aws cloudformation package --template-file announcements-app.yaml \
    --s3-bucket ${S3_BUCKET} --output-template-file output_template.yaml

aws cloudformation deploy --template-file output_template.yaml \
    --stack-name ${STACK_NAME} --capabilities CAPABILITY_IAM

api_endpoint=$(aws cloudformation describe-stacks --stack-name "${STACK_NAME}" \
    --query "Stacks[].Outputs[? OutputKey == 'ApiURL'].OutputValue" \
    --output text)

signup_url=$(aws cloudformation describe-stacks --stack-name "${STACK_NAME}" \
    --query "Stacks[].Outputs[? OutputKey == 'CognitoSignUpURL'].OutputValue" \
    --output text)

login_url=$(aws cloudformation describe-stacks --stack-name "${STACK_NAME}" \
    --query "Stacks[].Outputs[? OutputKey == 'CognitoLoginUpURL'].OutputValue" \
    --output text)

echo "Application successfully deployed. The API endpoint: ${api_endpoint}"
echo "URL for Cognito Sign Up: ${signup_url}"
echo "URL for Cognito Log In: ${login_url}"