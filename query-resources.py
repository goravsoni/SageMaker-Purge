import boto3
from collections import defaultdict
# Create a SageMaker client
sagemaker_client = boto3.client('sagemaker')
def count_resources(resource_type, key, status_key):
    active_statuses = ['InService', 'InProgress']
    active_count = defaultdict(int)
    inactive_count = defaultdict(int)
    paginator = sagemaker_client.get_paginator(resource_type)
    for page in paginator.paginate():
        for resource in page[key]:
            status = resource.get(status_key, 'Unknown')
            if status in active_statuses:
                active_count[status] += 1
            else:
                inactive_count[status] += 1
    return active_count, inactive_count
def list_notebook_instances_and_domains():
    # List Notebook Instances
    notebook_instances = sagemaker_client.list_notebook_instances()
    print("\nNotebook Instances:")
    for instance in notebook_instances.get('NotebookInstances', []):
        status = instance['NotebookInstanceStatus']
        dot = '🟢' if status == 'InService' else '🔴'
        print(f"{dot} Instance Name: {instance['NotebookInstanceName']}, Status: {status}")
    # List Domains
    domains = sagemaker_client.list_domains()
    print("\nDomains and User Profiles:")
    for domain in domains.get('Domains', []):
        status = domain['Status']
        dot = '🟢' if status == 'InService' else '🔴'
        print(f"{dot} Domain ID: {domain['DomainId']}, Status: {status}")
        # List User Profiles in each domain
        user_profiles = sagemaker_client.list_user_profiles(DomainIdEquals=domain['DomainId'])
        for profile in user_profiles.get('UserProfiles', []):
            print(f"  User Profile: {profile['UserProfileName']}")
            # List Apps in each user profile
            apps = sagemaker_client.list_apps(DomainIdEquals=domain['DomainId'], UserProfileNameEquals=profile['UserProfileName'])
            for app in apps.get('Apps', []):
                app_status = app['Status']
                dot = '🟢' if app_status == 'InService' else '🔴'
                print(f"    {dot} App Type: {app['AppType']}, Status: {app_status}")
# Mappings for function calls, their respective result keys, and status keys
resource_mappings = {
    'list_training_jobs': ('TrainingJobSummaries', 'TrainingJobStatus'),
    'list_models': ('Models', None),  # Models don't have a status
    'list_endpoints': ('Endpoints', 'EndpointStatus'),
    'list_hyper_parameter_tuning_jobs': ('HyperParameterTuningJobSummaries', 'HyperParameterTuningJobStatus'),
    'list_transform_jobs': ('TransformJobSummaries', 'TransformJobStatus'),
    'list_processing_jobs': ('ProcessingJobSummaries', 'ProcessingJobStatus'),
    'list_compilation_jobs': ('CompilationJobSummaries', 'CompilationJobStatus'),
}
# Iterate over all the resource types and count them
for resource_type, (key, status_key) in resource_mappings.items():
    print(f"\nCounting {resource_type}:")
    active, inactive = count_resources(resource_type, key, status_key)
    for status, count in active.items():
        print(f"🟢 Status: {status}, Count: {count}")
    for status, count in inactive.items():
        print(f"🔴 Status: {status}, Count: {count}")
# List Notebook Instances and Domains
list_notebook_instances_and_domains()