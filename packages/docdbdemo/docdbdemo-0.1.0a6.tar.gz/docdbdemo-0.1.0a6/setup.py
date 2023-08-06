import json
import setuptools

kwargs = json.loads("""
{
    "name": "docdbdemo",
    "version": "0.1.0-alpha.6",
    "description": "DocumentDB API Example",
    "url": "https://github.com/CDK-User-Group/DocumentDBDemo",
    "long_description_content_type": "text/markdown",
    "author": "Richard Boyd<Richard@rboyd.dev>",
    "project_urls": {
        "Source": "https://github.com/CDK-User-Group/DocumentDBDemo"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "docdbdemo",
        "docdbdemo._jsii"
    ],
    "package_data": {
        "docdbdemo._jsii": [
            "doc_db_lib@0.1.0-alpha.6.jsii.tgz"
        ],
        "docdbdemo": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii~=0.15.2",
        "publication>=0.0.3",
        "aws-cdk.aws-apigateway~=1.8,>=1.8.0",
        "aws-cdk.aws-docdb~=1.8,>=1.8.0",
        "aws-cdk.aws-ec2~=1.8,>=1.8.0",
        "aws-cdk.aws-lambda~=1.8,>=1.8.0",
        "aws-cdk.aws-secretsmanager~=1.8,>=1.8.0",
        "aws-cdk.core~=1.8,>=1.8.0"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
