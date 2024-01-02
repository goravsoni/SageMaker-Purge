import boto3
# Create a SageMaker client
sagemaker_client = boto3.client('sagemaker')
def list_sagemaker_resources(resource_type):
    paginator = sagemaker_client.get_paginator(resource_type)
    for page in paginator.paginate():
        for resource in page[resource_mappings[resource_type]]:
            print(resource)
# Mappings for function calls and their respective result keys
resource_mappings = {
    'list_training_jobs': 'TrainingJobSummaries',
    'list_models': 'Models',
    'list_endpoints': 'Endpoints',
    'list_notebook_instances': 'NotebookInstances',
    'list_hyper_parameter_tuning_jobs': 'HyperParameterTuningJobSummaries',
    'list_transform_jobs': 'TransformJobSummaries',
    'list_processing_jobs': 'ProcessingJobSummaries',
    'list_compilation_jobs': 'CompilationJobSummaries',
}
# Iterate over all the resource types and list them
for resource_type in resource_mappings.keys():
    print(f"\nListing {resource_type}:")
    list_sagemaker_resources(resource_type)