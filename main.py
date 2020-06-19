import json
import boto3
from flatten_json import flatten

client = boto3.client('iam')

list_user = []
list_roles = []
list_policy = []
list_InstanceProfile = []
list_groups = []
list_dashboards = []
list_Topics = []
list_describe_db_instances = []
list_functions = []
list_aws_arn = []

paginator = client.get_paginator('list_users')
for response in paginator.paginate():

    for aws_arn in response['Users']:
        list_user.append(aws_arn['Arn'])
    user = response.get('Users')


roles = client.list_roles()
Role_list = roles['Roles']
for key in Role_list:
    list_roles.append(key['Arn'])

paginator = client.get_paginator('list_policies')
for response in paginator.paginate(Scope='Local'):

    for aws_arn in response['Policies']:
        list_policy.append(aws_arn['Arn'])

paginator = client.get_paginator('list_instance_profiles')
for response in paginator.paginate():

    for aws_arn in response['InstanceProfiles']:
        list_InstanceProfile.append(aws_arn['Arn'])

paginator = client.get_paginator('list_groups')
for response in paginator.paginate():

    for aws_arn in response['Groups']:
        list_groups.append(aws_arn['Arn'])

client = boto3.client('cloudwatch')

paginator = client.get_paginator('list_dashboards')
for response in paginator.paginate():

    for aws_arn in response['DashboardEntries']:
        list_dashboards.append(aws_arn['DashboardArn'])

client = boto3.client('sns')

paginator = client.get_paginator('list_topics')
for response in paginator.paginate():

    for aws_arn in response['Topics']:
        list_Topics.append(aws_arn['TopicArn'])

client = boto3.client('rds')

paginator = client.get_paginator('describe_db_instances')
for response in paginator.paginate():

    for aws_arn in response['DBInstances']:
        list_describe_db_instances.append(aws_arn['DBInstanceArn'])

client = boto3.client('lambda')

paginator = client.get_paginator('list_functions')
for response in paginator.paginate():

    for aws_arn in response['Functions']:
        list_functions.append(aws_arn['FunctionArn'])

with open('plan.json') as f:
  data = json.load(f)

flat_json = flatten(data)

# ARN's from state
for key, value in flat_json.items():   # iter on both keys and values
        if key.endswith('_arn'):
                list_aws_arn.append(value)


iam_users = [item for item in list_user if item not in list_aws_arn]
print("IAM users not under terraform")
print(iam_users)

iam_roles = [item for item in list_roles if item not in list_aws_arn]
print("IAM Roles not under terraform")
print(iam_roles)

iam_policy = [item for item in list_policy if item not in list_aws_arn]
print("IAM Policies not under terraform")
print(iam_policy)

iam_InstanceProfile = [item for item in list_InstanceProfile if item not in list_aws_arn]
print("IAM InstanceProfile not under terraform")
print(iam_InstanceProfile)

iam_groups = [item for item in list_groups if item not in list_aws_arn]
print("IAM InstanceProfile not under terraform")
print(iam_groups)

cloudwatch_dashboards = [item for item in list_dashboards if item not in list_aws_arn]
print("Cloudwatch dashboards not under terraform")
print(cloudwatch_dashboards)

sns_topics = [item for item in list_Topics if item not in list_aws_arn]
print("SNS topics not under terraform")
print(sns_topics)

rds_db_instances = [item for item in list_describe_db_instances if item not in list_aws_arn]
print("RDS DB Instances not under terraform")
print(rds_db_instances)

lambda_functions = [item for item in list_functions if item not in list_aws_arn]
print("IAM Lambda Functions not under terraform")
print(lambda_functions)
