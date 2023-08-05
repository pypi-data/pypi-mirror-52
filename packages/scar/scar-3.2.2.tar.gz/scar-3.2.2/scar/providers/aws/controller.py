# Copyright (C) GRyCAP - I3M - UPV
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Module with classes and methods used to manage the AWS tools."""

import os
from typing import Dict
from scar.cmdtemplate import Commands
from scar.providers.aws.apigateway import APIGateway
from scar.providers.aws.batchfunction import Batch
from scar.providers.aws.cloudwatchlogs import CloudWatchLogs
from scar.providers.aws.iam import IAM
from scar.providers.aws.lambdafunction import Lambda
from scar.providers.aws.properties import AwsProperties, ScarProperties
from scar.providers.aws.resourcegroups import ResourceGroups
from scar.providers.aws.s3 import S3
from scar.providers.aws.validators import AWSValidator
from scar.providers.aws.properties import ApiGatewayProperties
import scar.exceptions as excp
import scar.logger as logger
import scar.providers.aws.response as response_parser
from scar.utils import lazy_property, StrUtils, FileUtils

_ACCOUNT_ID_REGEX = r'\d{12}'


def _get_storage_provider_id(storage_provider: str, env_vars: Dict) -> str:
    """Searches the storage provider id in the environment variables:
        get_provider_id(S3, {'STORAGE_AUTH_S3_USER_41807' : 'scar'})
        returns -> 41807"""
    res = ""
    for env_key in env_vars.keys():
        if env_key.startswith(f'STORAGE_AUTH_{storage_provider}'):
            res = env_key.split('_', 4)[-1]
            break
    return res


class AWS(Commands):
    """AWS controller.
    Used to manage all the AWS calls and functionalities."""

    @lazy_property
    def aws_lambda(self):
        """It's called 'aws_lambda' because 'lambda'
        it's a restricted word in python."""
        aws_lambda = Lambda(self.aws_properties,
                            self.scar_properties.supervisor_version)
        return aws_lambda

    @lazy_property
    def batch(self):
        batch = Batch(self.aws_properties,
                      self.scar_properties.supervisor_version)
        return batch

    @lazy_property
    def cloudwatch_logs(self):
        cloudwatch_logs = CloudWatchLogs(self.aws_properties)
        return cloudwatch_logs

    @lazy_property
    def api_gateway(self):
        api_gateway = APIGateway(self.aws_properties)
        return api_gateway

    @lazy_property
    def aws_s3(self):
        aws_s3 = S3(self.aws_properties)
        return aws_s3

    @lazy_property
    def resource_groups(self):
        resource_groups = ResourceGroups(self.aws_properties)
        return resource_groups

    @lazy_property
    def iam(self):
        iam = IAM(self.aws_properties)
        return iam

    @excp.exception(logger)
    def init(self):
        if self.aws_lambda.find_function():
            raise excp.FunctionExistsError(function_name=self.aws_properties.lambdaf.name)
        # We have to create the gateway before creating the function
        self._create_api_gateway()
        self._create_lambda_function()
        self._create_log_group()
        self._create_s3_buckets()
        # The api_gateway permissions are added after the function is created
        self._add_api_gateway_permissions()
        self._create_batch_environment()
        self._preheat_function()

    @excp.exception(logger)
    def invoke(self):
        self._update_local_function_properties()
        response = self.aws_lambda.call_http_endpoint()
        response_parser.parse_http_response(response,
                                            self.aws_properties.lambdaf.name,
                                            self.aws_properties.lambdaf.asynchronous,
                                            self.aws_properties.output,
                                            getattr(self.scar_properties, "output_file", ""))

    @excp.exception(logger)
    def run(self):
        if hasattr(self.aws_properties, "s3") and hasattr(self.aws_properties.s3, "input_bucket"):
            self._process_input_bucket_calls()
        else:
            if self.aws_lambda.is_asynchronous():
                self.aws_lambda.set_asynchronous_call_parameters()
            self.aws_lambda.launch_lambda_instance()

    @excp.exception(logger)
    def update(self):
        if hasattr(self.aws_properties.lambdaf, "all") and self.aws_properties.lambdaf.all:
            self._update_all_functions(self._get_all_functions())
        else:
            self.aws_lambda.update_function_configuration()

    @excp.exception(logger)
    def ls(self):
        if hasattr(self.aws_properties, "s3"):
            file_list = self.aws_s3.get_bucket_file_list()
            for file_info in file_list:
                print(file_info)
        else:
            lambda_functions = self._get_all_functions()
            response_parser.parse_ls_response(lambda_functions,
                                              self.aws_properties.output)

    @excp.exception(logger)
    def rm(self):
        if hasattr(self.aws_properties.lambdaf, "all") and self.aws_properties.lambdaf.all:
            self._delete_all_resources()
        else:
            function_info = self.aws_lambda.get_function_info(self.aws_properties.lambdaf.name)
            self._delete_resources(function_info)

    @excp.exception(logger)
    def log(self):
        aws_log = self.cloudwatch_logs.get_aws_log()
        batch_logs = self._get_batch_logs()
        aws_log += batch_logs if batch_logs else ""
        print(aws_log)

    @excp.exception(logger)
    def put(self):
        self.upload_file_or_folder_to_s3()

    @excp.exception(logger)
    def get(self):
        self.download_file_or_folder_from_s3()

    @AWSValidator.validate()
    @excp.exception(logger)
    def parse_arguments(self, **kwargs):
        self.raw_kwargs = kwargs
        self.aws_properties = AwsProperties(kwargs.get('aws', {}))
        self.scar_properties = ScarProperties(kwargs.get('scar', {}))
        self.add_extra_aws_properties()

    def add_extra_aws_properties(self):
        self._add_tags()
        self._add_output()
        self._add_account_id()
        self._add_config_file_path()

    def _add_tags(self):
        self.aws_properties.tags = {"createdby": "scar", "owner": self.iam.get_user_name_or_id()}

    def _add_output(self):
        self.aws_properties.output = response_parser.OutputType.PLAIN_TEXT
        if hasattr(self.scar_properties, "json") and self.scar_properties.json:
            self.aws_properties.output = response_parser.OutputType.JSON
        # Override json ouput if both of them are defined
        if hasattr(self.scar_properties, "verbose") and self.scar_properties.verbose:
            self.aws_properties.output = response_parser.OutputType.VERBOSE
        if hasattr(self.scar_properties, "output_file") and self.scar_properties.output_file:
            self.aws_properties.output = response_parser.OutputType.BINARY
            self.aws_properties.output_file = self.scar_properties.output_file

    def _add_account_id(self):
        self.aws_properties.account_id = StrUtils.find_expression(self.aws_properties.iam.role,
                                                                  _ACCOUNT_ID_REGEX)

    def _add_config_file_path(self):
        if hasattr(self.scar_properties, "conf_file") and self.scar_properties.conf_file:
            self.aws_properties.config_path = os.path.dirname(self.scar_properties.conf_file)

    def _get_all_functions(self):
        arn_list = self.resource_groups.get_resource_arn_list(self.iam.get_user_name_or_id())
        return self.aws_lambda.get_all_functions(arn_list)

    def _get_batch_logs(self) -> str:
        logs = ""
        if hasattr(self.aws_properties.cloudwatch, "request_id") and \
        self.batch.exist_job(self.aws_properties.cloudwatch.request_id):
            batch_jobs = self.batch.describe_jobs(self.aws_properties.cloudwatch.request_id)
            logs = self.cloudwatch_logs.get_batch_job_log(batch_jobs["jobs"])
        return logs

    @excp.exception(logger)
    def _create_lambda_function(self):
        response = self.aws_lambda.create_function()
        acc_key = self.aws_lambda.client.get_access_key()
        response_parser.parse_lambda_function_creation_response(response,
                                                                self.aws_properties.lambdaf.name,
                                                                acc_key,
                                                                self.aws_properties.output)

    @excp.exception(logger)
    def _create_log_group(self):
        response = self.cloudwatch_logs.create_log_group()
        response_parser.parse_log_group_creation_response(response,
                                                          self.cloudwatch_logs.get_log_group_name(),
                                                          self.aws_properties.output)

    @excp.exception(logger)
    def _create_s3_buckets(self):
        if hasattr(self.aws_properties, "s3"):
            if hasattr(self.aws_properties.s3, "input_bucket"):
                self.aws_s3.create_input_bucket(create_input_folder=True)
                self.aws_lambda.link_function_and_input_bucket()
                self.aws_s3.set_input_bucket_notification()
            if hasattr(self.aws_properties.s3, "output_bucket"):
                self.aws_s3.create_output_bucket()

    def _create_api_gateway(self):
        if hasattr(self.aws_properties, "api_gateway"):
            self.api_gateway.create_api_gateway()

    def _add_api_gateway_permissions(self):
        if hasattr(self.aws_properties, "api_gateway"):
            self.aws_lambda.add_invocation_permission_from_api_gateway()

    def _create_batch_environment(self):
        if self.aws_properties.execution_mode == "batch" or \
        self.aws_properties.execution_mode == "lambda-batch":
            self.batch.create_batch_environment()

    def _preheat_function(self):
        # If preheat is activated, the function is launched at the init step
        if hasattr(self.scar_properties, "preheat"):
            self.aws_lambda.preheat_function()

    def _process_input_bucket_calls(self):
        s3_file_list = self.aws_s3.get_bucket_file_list()
        logger.info(f"Files found: '{s3_file_list}'")
        # First do a request response invocation to prepare the lambda environment
        if s3_file_list:
            s3_event = self.aws_s3.get_s3_event(s3_file_list.pop(0))
            self.aws_lambda.launch_request_response_event(s3_event)
        # If the list has more elements, invoke functions asynchronously
        if s3_file_list:
            s3_event_list = self.aws_s3.get_s3_event_list(s3_file_list)
            self.aws_lambda.process_asynchronous_lambda_invocations(s3_event_list)

    def upload_file_or_folder_to_s3(self):
        path_to_upload = self.scar_properties.path
        self.aws_s3.create_input_bucket()
        files = [path_to_upload]
        if os.path.isdir(path_to_upload):
            files = FileUtils.get_all_files_in_directory(path_to_upload)
        for file_path in files:
            self.aws_s3.upload_file(folder_name=self.aws_properties.s3.input_folder,
                                    file_path=file_path)

    def _get_download_file_path(self, file_key=None):
        file_path = file_key
        if hasattr(self.scar_properties, "path") and self.scar_properties.path:
            file_path = FileUtils.join_paths(self.scar_properties.path, file_path)
        return file_path

    def download_file_or_folder_from_s3(self):
        bucket_name = self.aws_properties.s3.input_bucket
        s3_file_list = self.aws_s3.get_bucket_file_list()
        for s3_file in s3_file_list:
            # Avoid download s3 'folders'
            if not s3_file.endswith('/'):
                file_path = self._get_download_file_path(file_key=s3_file)
                # make sure the path folders are created
                dir_path = os.path.dirname(file_path)
                if dir_path and not os.path.isdir(dir_path):
                    os.makedirs(dir_path, exist_ok=True)
                self.aws_s3.download_file(bucket_name, s3_file, file_path)

    def _update_all_functions(self, lambda_functions):
        for function_info in lambda_functions:
            self.aws_lambda.update_function_configuration(function_info)

    def _update_local_function_properties(self, function_info):
        self._reset_aws_properties()
        """Update the defined properties with the AWS information."""
        if function_info:
            self.aws_properties.lambdaf.update_properties(**function_info)
        if 'API_GATEWAY_ID' in self.aws_properties.lambdaf.environment['Variables']:
            api_gtw_id = self.aws_properties.lambdaf.environment['Variables'].get('API_GATEWAY_ID',
                                                                                  "")
            if hasattr(self.aws_properties, 'api_gateway'):
                self.aws_properties.api_gateway.id = api_gtw_id
            else:
                self.aws_properties.api_gateway = ApiGatewayProperties({'id' : api_gtw_id})

#############################################################################
###                   Methods to delete AWS resources                     ###
#############################################################################

    def _delete_all_resources(self):
        for function_info in self._get_all_functions():
            self._delete_resources(function_info)

    def _delete_resources(self, function_info):
        function_name = function_info['FunctionName']
        if not self.aws_lambda.find_function(function_name):
            raise excp.FunctionNotFoundError(function_name=function_name)
        # Delete associated api
        self._delete_api_gateway(function_info['Environment']['Variables'])
        # Delete associated log
        self._delete_logs(function_name)
        # Delete associated notifications
        self._delete_bucket_notifications(function_info['FunctionArn'],
                                          function_info['Environment']['Variables'])
        # Delete function
        self._delete_lambda_function(function_name)
        # Delete resources batch
        self._delete_batch_resources(function_name)

    def _delete_api_gateway(self, function_env_vars):
        api_gateway_id = function_env_vars.get('API_GATEWAY_ID')
        if api_gateway_id:
            response = self.api_gateway.delete_api_gateway(api_gateway_id)
            response_parser.parse_delete_api_response(response, api_gateway_id,
                                                      self.aws_properties.output)

    def _delete_logs(self, function_name):
        log_group_name = self.cloudwatch_logs.get_log_group_name(function_name)
        response = self.cloudwatch_logs.delete_log_group(log_group_name)
        response_parser.parse_delete_log_response(response,
                                                  log_group_name,
                                                  self.aws_properties.output)

    def _delete_bucket_notifications(self, function_arn, function_env_vars):
        s3_provider_id = _get_storage_provider_id('S3', function_env_vars)
        input_bucket_id = f'STORAGE_PATH_INPUT_{s3_provider_id}' if s3_provider_id else ''
        if input_bucket_id in function_env_vars:
            input_path = function_env_vars[input_bucket_id]
            input_bucket_name = input_path.split("/", 1)[0]
            self.aws_s3.delete_bucket_notification(input_bucket_name, function_arn)

    def _delete_lambda_function(self, function_name):
        response = self.aws_lambda.delete_function(function_name)
        response_parser.parse_delete_function_response(response, function_name,
                                                       self.aws_properties.output)

    def _delete_batch_resources(self, function_name):
        if self.batch.exist_compute_environments(function_name):
            self.batch.delete_compute_environment(function_name)
