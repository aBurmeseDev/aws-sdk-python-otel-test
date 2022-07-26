from opentelemetry import propagate, trace
from opentelemetry.instrumentation.botocore import BotocoreInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
import boto3

span_processor = BatchSpanProcessor(ConsoleSpanExporter())
trace.set_tracer_provider(
    TracerProvider(
        active_span_processor=span_processor,
        # resource=get_aggregated_resources(
        #     [
        #         AwsEc2ResourceDetector(),
        #     ]
        # ),
    )
)

# Instrument Packages

BotocoreInstrumentor().instrument()

