aws s3 mb s3://${S3_BUCKET}

aws cloudformation package --template-file announcements-app.yaml \
    --s3-bucket ${S3_BUCKET} --output-template-file output_template.yaml

aws cloudformation deploy --template-file output_template.yaml \
    --stack-name ${STACK_NAME} --capabilities CAPABILITY_IAM

api_endpoint=$(aws cloudformation describe-stacks --stack-name "${STACK_NAME}" \
    --query "Stacks[].Outputs[? OutputKey == 'ApiUrl'].OutputValue" \
    --output text)

echo "Successful deployed. The API endpoint: ${api_endpoint}"