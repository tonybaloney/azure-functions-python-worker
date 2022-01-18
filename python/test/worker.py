import sys
import os
from azure_functions_worker import main
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter


# Azure environment variables
AZURE_WEBJOBS_SCRIPT_ROOT = "AzureWebJobsScriptRoot"


def add_script_root_to_sys_path():
    '''Append function project root to module finding sys.path'''
    functions_script_root = os.getenv(AZURE_WEBJOBS_SCRIPT_ROOT)
    if functions_script_root is not None:
        sys.path.append(functions_script_root)


if __name__ == '__main__':
    add_script_root_to_sys_path()


    trace.set_tracer_provider(TracerProvider())
    
    exporter = AzureMonitorTraceExporter.from_connection_string(
        conn_str = "InstrumentationKey=f02d8d32-cdc2-4b39-b8d3-d71206b0febe;IngestionEndpoint=https://australiaeast-1.in.applicationinsights.azure.com/" # ""# conn_str = os.environ["APPLICATIONINSIGHTS_CONNECTION_STRING"]
    )
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(exporter)
    )

    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("foo"):
        main.main()
