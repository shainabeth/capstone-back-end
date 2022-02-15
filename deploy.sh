#!/bin/bash

SCRIPT_DIR=`pwd`
ZIP_NAME="my-deployment-package.zip"
DEPS_PATH="./venv/lib/python3.9/site-packages"
pushd ${DEPS_PATH}
zip -r9 ${SCRIPT_DIR}/${ZIP_NAME} .
popd 

zip ${ZIP_NAME} ./lambda_function.py

S3_BUCKET="shaina-capstone-lambda-deployment"
S3_KEY="${ZIP_NAME}"
S3_URI="s3://${S3_BUCKET}/${S3_KEY}"

# Deploy to s3
aws s3 cp ${ZIP_NAME} ${S3_URI} && rm ${ZIP_NAME}
# Tell lambda to pull from s3
aws lambda update-function-code --function-name Capstone-back-end --s3-key ${S3_KEY} --s3-bucket ${S3_BUCKET} 