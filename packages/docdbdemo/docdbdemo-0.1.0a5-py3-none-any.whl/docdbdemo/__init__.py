import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_apigateway
import aws_cdk.aws_docdb
import aws_cdk.aws_ec2
import aws_cdk.aws_lambda
import aws_cdk.aws_secretsmanager
import aws_cdk.core
__jsii_assembly__ = jsii.JSIIAssembly.load("@richardhboyd/doc_db_lib", "0.1.0-alpha.5", __name__, "doc_db_lib@0.1.0-alpha.5.jsii.tgz")
class DocDbLib(aws_cdk.core.Construct, metaclass=jsii.JSIIMeta, jsii_type="@richardhboyd/doc_db_lib.DocDbLib"):
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, vpc: typing.Optional[aws_cdk.aws_ec2.Vpc]=None) -> None:
        """
        :param scope: -
        :param id: -
        :param props: -
        :param vpc: The visibility timeout to be configured on the SQS Queue, in seconds. Default: Duration.seconds(300)
        """
        props = DocDbLibProps(vpc=vpc)

        jsii.create(DocDbLib, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="queueArn")
    def queue_arn(self) -> str:
        """
        return
        :return: the ARN of the SQS queue
        """
        return jsii.get(self, "queueArn")


@jsii.data_type(jsii_type="@richardhboyd/doc_db_lib.DocDbLibProps", jsii_struct_bases=[], name_mapping={'vpc': 'vpc'})
class DocDbLibProps():
    def __init__(self, *, vpc: typing.Optional[aws_cdk.aws_ec2.Vpc]=None):
        """
        :param vpc: The visibility timeout to be configured on the SQS Queue, in seconds. Default: Duration.seconds(300)
        """
        self._values = {
        }
        if vpc is not None: self._values["vpc"] = vpc

    @property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.Vpc]:
        """The visibility timeout to be configured on the SQS Queue, in seconds.

        default
        :default: Duration.seconds(300)
        """
        return self._values.get('vpc')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'DocDbLibProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = ["DocDbLib", "DocDbLibProps", "__jsii_assembly__"]

publication.publish()
