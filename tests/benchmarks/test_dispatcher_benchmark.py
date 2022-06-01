# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from azure_functions_worker import testutils


def test_invoke_function_benchmark(aio_benchmark, event_loop):
    async def invoke_function():
        with testutils.start_webhost(testutils.TESTS_ROOT) as host:
            await host.load_function('return_http')
            
            for _ in range(1000):
                event_loop.create_task(worker._handle__invocation_request(message))
    
    aio_benchmark(invoke_function)

