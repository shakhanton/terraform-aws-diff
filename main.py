import json
import boto3
import os
from flatten_json import flatten


def get_aws_arn(service, operation, service_object, object_arn, **paginate_params):
    arns = []
    client = boto3.client(service)
    paginator = client.get_paginator(operation)
    page_iterator = paginator.paginate(**paginate_params)
    for page in page_iterator:
        for arn in page[service_object]:
            arns.append(arn[object_arn])
    return arns


def get_state_arns(state_file_dir):
    list_state_arn = []
    data = []
    with os.scandir(state_file_dir) as it:
        for entry in it:
            if entry.name.endswith('.json') and entry.is_file():
                with open(entry, 'r') as f:
                    json_txt_temp = f.read()
                json_dict = json.loads(json_txt_temp)
                data.append(json_dict)

    for json_plan in data:
        flat_json = flatten(json_plan)

        for key, value in list(flat_json.items()):
            if key.startswith('prior_state_values_'):
                del flat_json[key]

        for key, value in flat_json.items():
            if key.endswith('_arn'):
                list_state_arn.append(value)

    return list_state_arn


def compare_function(resource_type_desc, list_aws):

    resources_in_aws_only = [item for item in list_aws if item not in list_state]
    print(f"\033[1m{resource_type_desc} not created by terraform \033[0m", *resources_in_aws_only, sep="\n")


list_state = get_state_arns('plans')


list_aws_user = get_aws_arn('iam', 'list_users', 'Users', 'Arn')
list_roles = get_aws_arn('iam', 'list_roles', 'Roles', 'Arn')
list_policy = get_aws_arn('iam', 'list_policies', 'Policies', 'Arn', Scope='Local')
list_instance_profile = get_aws_arn('iam', 'list_instance_profiles', 'InstanceProfiles', 'Arn')
list_groups = get_aws_arn('iam', 'list_groups', 'Groups', 'Arn')
list_dashboards = get_aws_arn('cloudwatch', 'list_dashboards', 'DashboardEntries', 'DashboardArn')
list_topics = get_aws_arn('sns', 'list_topics', 'Topics', 'TopicArn')
list_describe_db_instances = get_aws_arn('rds', 'describe_db_instances', 'DBInstances', 'DBInstanceArn')
list_functions = get_aws_arn('lambda', 'list_functions', 'Functions', 'FunctionArn')


compare_function("IAM Users", list_aws_user)
compare_function("IAM Roles", list_roles)
compare_function("IAM Policies", list_policy)
compare_function("IAM InstanceProfile", list_instance_profile)
compare_function("IAM Groups", list_groups)
compare_function("CloudWatch dashboards", list_dashboards)
compare_function("SNS topics", list_topics)
compare_function("RDS DB Instances", list_describe_db_instances)
compare_function("IAM Lambda Functions", list_functions)
