import boto3
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.sdk.resources import get_aggregated_resources
from opentelemetry.sdk.extension.aws.resource.ec2 import (
    AwsEc2ResourceDetector,
)
trace.set_tracer_provider(
    TracerProvider(
        resource=get_aggregated_resources(
            [
                AwsEc2ResourceDetector(),
            ]
        ),
    )
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(ConsoleSpanExporter())
)
tracer = trace.get_tracer(__name__)
with tracer.start_as_current_span("foo"):
    ec2 = boto3.client('ec2')
    ec2.region = 'us-east-2'
    response = ec2.describe_instances()
    print('Response: ', response)