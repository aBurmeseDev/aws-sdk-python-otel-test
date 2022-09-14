from opentelemetry import trace
from opentelemetry.instrumentation.botocore import BotocoreInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource


# create a JaegerExporter
jaeger_exporter = JaegerExporter(
    # configure agent
    agent_host_name='localhost',
    agent_port=6831,
    # optional: configure also collector
    # collector_endpoint='http://localhost:14268/api/traces?format=jaeger.thrift',
    # username=xxxx, # optional
    # password=xxxx, # optional
    # max_tag_value_length=None # optional
)

# 
span_processor = BatchSpanProcessor(jaeger_exporter)
trace.set_tracer_provider(
    TracerProvider(
        active_span_processor = span_processor,
        # resource = get_aggregated_resources(
        #     [
        #         AwsEc2ResourceDetector(),
        #     ]
        # ),
         resource=Resource.create({
            "service.name": "pythonOtelSDK",
            "service.instance.id": "instance-12",
        }),
    )
)

# Instrument Packages

BotocoreInstrumentor().instrument()
