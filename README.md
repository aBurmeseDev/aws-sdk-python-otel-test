# aws-sdk-python-otel-test
This sample shows how to use OpenTelemetry Python API to instrument the following calls in AWS SDK for Python:
- `ListBuckets` call on S3 client
- `ListTables` call on DynamoDB client

This example exports spans data to `Console`. You can also export it to [Jaeger][jaegertracing]
by setting `JAEGER_ENABLED` environment variable.

## What is OpenTelemetry and How it works?

OpenTelemetry is a project maintained by the Cloud Native Computing Foundation which provides open source APIs, libraries, and agents to collect distributed traces and metrics for application monitoring.

OpenTelemetry generates telemetry data, such as metrics and traces, for requests to the application. In addition, OpenTelemetry Python provides automatic tracing for many popular Python packages. These traces record parameters used, results, exceptions, and more in span attributes as it completes the traced task. Read more about standardized attributes on the OpenTelemetry Specification [Semantic Conventions for traces](https://github.com/open-telemetry/opentelemetry-specification/tree/main/specification/trace/semantic_conventions).

[OpenTelemetry Python](https://github.com/open-telemetry/opentelemetry-python) provides entry points for configuration through its [API](https://github.com/open-telemetry/opentelemetry-python/tree/main/opentelemetry-api). This can be used to configure the [ids_generator](https://github.com/open-telemetry/opentelemetry-python/blob/65528f7534f1f5f2e8adc7520b6e696a84569c7d/opentelemetry-sdk/src/opentelemetry/sdk/trace/id_generator.py#L19) needed to support the X-Ray trace ID format. It also allows the use of a custom propagator, passed into the tracer provider, to generate and propagate the AWS X-Ray trace header.

After traces have been generated, they can be sent to a back-end service like AWS X-Ray to display the traces in a user-friendly interactive console packed with features to help you visualize and understand what happened during traced calls. Learn more about AWS X-Ray in the [developer guide](https://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html).

An easy way for a traced application to send traces to AWS X-Ray is by using the ADOT Collector. The traced application configures OpenTelemetry for Python to export traces in the OpenTelemetry Format, and subsequently directs the traces to a Docker Container running the ADOT Collector. The ADOT Collector is configured with [AWS credentials for the CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html), an AWS Region, and which trace attributes to index so that it can send the traces to the AWS X-Ray console. Read more about the [AWS X-Ray Tracing Exporter for OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/exporter/awsxrayexporter).

## Requirements

Python 3.5+ is required to use OpenTelemetry Python. Check your currently installed Python version using `python3 -V`.
For more information about supported Python versions, see the [OpenTelemetry Python package on PyPi](https://pypi.org/project/opentelemetry-api/).

## Prerequisites

Complete the following tasks:
- Install **Python** by following these steps [here](https://realpython.com/installing-python/)
- Install **pip** by following these steps [here](https://pip.pypa.io/en/stable/installation/)
- Install the following dependencies:
  - `pip install boto3`
  - `pip install opentelemetry-api`
  - `pip install opentelemetry-sdk`
  - `pip install opentelemetry-sdk-extension-aws`
  - `pip install opentelemetry-exporter-jaeger`
- If you don't have an AWS account, [create one](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/).
  - If you're an Amazon employee, see the internal wiki for creating an AWS account.
- Install the [AWS CLI](https://aws.amazon.com/cli/).
  - Verify that the AWS CLI is installed by running `aws` in a terminal window.
- Set up [AWS Shared Credential File](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html).
  - Your `~/.aws/credentials` (`%UserProfile%\.aws\credentials` on Windows) should look like the following:
    ```
    [default]
    aws_access_key_id = <ACCESS_KEY>
    aws_secret_access_key = <SECRET_ACCESS_KEY>
    ```
  - Your `~/.aws/config` (`%UserProfile%\.aws\config` on Windows) should look like the following:
    ```
    [default]
    region = us-west-2
    ```
- (Optional) Setup [Jaeger Tracing][jaeger-getting-started]: needs to be running on `localhost` port `16686`.

## Setup

The test code from this package uses `AwsInstrumentation` from [@opentelemetry/instrumentation-aws-sdk][instrumentation-aws-sdk]
to instrument listBuckets call on S3 and listTables call on DynamoDB client.

### Trace Logs and Data Metrics
<details>
<summary>console trace logs</summary>

```console
$ trace logs
{
    "name": "S3.ListBuckets",
    "context": {
        "trace_id": "0x7db042e4fe525fb8c833e18572d319b7",
        "span_id": "0x2611d37fd852d169",
        "trace_state": "[]"
    },
    "kind": "SpanKind.CLIENT",
    "parent_id": null,
    "start_time": "2022-07-26T23:11:49.728823Z",
    "end_time": "2022-07-26T23:11:49.919806Z",
    "status": {
        "status_code": "UNSET"
    },
    "attributes": {
        "rpc.system": "aws-api",
        "rpc.service": "S3",
        "rpc.method": "ListBuckets",
        "aws.region": "us-west-1",
        "aws.request_id": "8YV1ZYTFD7S7N7AZ",
        "retry_attempts": 0,
        "http.status_code": 200
    },
    "events": [],
    "links": [],
    "resource": {
        "telemetry.sdk.language": "python",
        "telemetry.sdk.name": "opentelemetry",
        "telemetry.sdk.version": "1.11.1",
        "service.name": "unknown_service"
    }
}
```
</details>

### Screenshots

<details>
<summary>Jaeger Traces when operation is called multiple times</summary>

![Jaeger Traces for AWS SDK for JavaScript](img/jaeger-traces.png?raw=true)

</details>
