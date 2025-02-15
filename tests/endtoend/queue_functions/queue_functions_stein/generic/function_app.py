import json
import logging
import typing

import azure.functions as func

app = func.FunctionApp()


@app.function_name(name="get_queue_blob")
@app.generic_trigger(arg_name="req",
                     type="httpTrigger",
                     route="get_queue_blob")
@app.generic_output_binding(arg_name="$return", type="http")
@app.generic_input_binding(
    arg_name="file",
    type="blob",
    connection="AzureWebJobsStorage",
    path="python-worker-tests/test-queue-blob.txt")
def get_queue_blob(req: func.HttpRequest, file: func.InputStream) -> str:
    return json.dumps({
        'queue': json.loads(file.read().decode('utf-8'))
    })


@app.function_name(name="get_queue_blob_message_return")
@app.generic_trigger(arg_name="req",
                     type="httpTrigger",
                     route="get_queue_blob_message_return")
@app.generic_output_binding(arg_name="$return", type="http")
@app.generic_input_binding(
    arg_name="file",
    type="blob",
    connection="AzureWebJobsStorage",
    path="python-worker-tests/test-queue-blob-message-return.txt")
def get_queue_blob_message_return(req: func.HttpRequest,
                                  file: func.InputStream) -> str:
    return file.read().decode('utf-8')


@app.function_name(name="get_queue_blob_return")
@app.generic_trigger(arg_name="req",
                     type="httpTrigger",
                     route="get_queue_blob_return")
@app.generic_output_binding(arg_name="$return", type="http")
@app.generic_input_binding(arg_name="file",
                           type="blob",
                           connection="AzureWebJobsStorage",
                           path="python-worker-tests/test-queue-blob-return"
                                ".txt")
def get_queue_blob_return(req: func.HttpRequest,
                          file: func.InputStream) -> str:
    return file.read().decode('utf-8')


@app.function_name(name="get_queue_untyped_blob_return")
@app.generic_trigger(arg_name="req",
                     type="httpTrigger",
                     route="get_queue_untyped_blob_return")
@app.generic_output_binding(arg_name="$return", type="http")
@app.generic_input_binding(
    arg_name="file",
    type="blob",
    connection="AzureWebJobsStorage",
    path="python-worker-tests/test-queue-untyped-blob-return.txt")
def get_queue_untyped_blob_return(req: func.HttpRequest,
                                  file: func.InputStream) -> str:
    return file.read().decode('utf-8')


@app.function_name(name="put_queue")
@app.generic_trigger(arg_name="req",
                     type="httpTrigger",
                     route="put_queue")
@app.generic_output_binding(arg_name="$return", type="http")
@app.generic_output_binding(
    arg_name="msg",
    type="queue",
    connection="AzureWebJobsStorage",
    queue_name="testqueue")
def put_queue(req: func.HttpRequest, msg: func.Out[str]):
    msg.set(req.get_body())

    return 'OK'


@app.function_name(name="put_queue_message_return")
@app.generic_trigger(arg_name="req",
                     type="httpTrigger",
                     route="put_queue_message_return")
@app.generic_output_binding(arg_name="resp", type="http")
@app.generic_output_binding(
    arg_name="$return",
    type="queue",
    connection="AzureWebJobsStorage",
    queue_name="testqueue-message-return")
def main(req: func.HttpRequest, resp: func.Out[str]) -> bytes:
    return func.QueueMessage(body=req.get_body())


@app.function_name(name="put_queue_multiple_out")
@app.generic_trigger(arg_name="req",
                     type="httpTrigger",
                     route="put_queue_multiple_out")
@app.generic_output_binding(arg_name="resp", type="http")
@app.generic_output_binding(
    arg_name="msg",
    type="queue",
    connection="AzureWebJobsStorage",
    queue_name="testqueue-return-multiple-outparam")
def put_queue_multiple_out(req: func.HttpRequest,
                           resp: func.Out[func.HttpResponse],
                           msg: func.Out[func.QueueMessage]) -> None:
    data = req.get_body().decode()
    msg.set(func.QueueMessage(body=data))
    resp.set(func.HttpResponse(body='HTTP response: {}'.format(data)))


@app.function_name("put_queue_return")
@app.generic_trigger(arg_name="req",
                     type="httpTrigger",
                     route="put_queue_return")
@app.generic_output_binding(arg_name="resp", type="http")
@app.generic_output_binding(
    arg_name="$return",
    type="queue",
    connection="AzureWebJobsStorage",
    queue_name="testqueue-return")
def put_queue_return(req: func.HttpRequest, resp: func.Out[str]) -> bytes:
    return req.get_body()


@app.function_name(name="put_queue_multiple_return")
@app.generic_trigger(arg_name="req",
                     type="httpTrigger",
                     route="put_queue_multiple_return")
@app.generic_output_binding(arg_name="$return", type="http")
@app.generic_output_binding(
    arg_name="msgs",
    type="queue",
    connection="AzureWebJobsStorage",
    queue_name="testqueue-return-multiple")
def put_queue_multiple_return(req: func.HttpRequest,
                              msgs: func.Out[typing.List[str]]):
    msgs.set(['one', 'two'])


@app.function_name(name="put_queue_untyped_return")
@app.generic_trigger(arg_name="req",
                     type="httpTrigger",
                     route="put_queue_untyped_return")
@app.generic_output_binding(arg_name="resp", type="http")
@app.generic_output_binding(
    arg_name="$return",
    type="queue",
    connection="AzureWebJobsStorage",
    queue_name="testqueue-untyped-return")
def put_queue_untyped_return(req: func.HttpRequest,
                             resp: func.Out[str]) -> bytes:
    return func.QueueMessage(body=req.get_body())


@app.function_name(name="queue_trigger")
@app.generic_trigger(arg_name="msg",
                     type="queueTrigger",
                     queue_name="testqueue",
                     connection="AzureWebJobsStorage")
@app.generic_output_binding(arg_name="$return",
                            type="blob",
                            connection="AzureWebJobsStorage",
                            path="python-worker-tests/test-queue-blob.txt")
def queue_trigger(msg: func.QueueMessage) -> str:
    result = json.dumps({
        'id': msg.id,
        'body': msg.get_body().decode('utf-8'),
        'expiration_time': (msg.expiration_time.isoformat()
                            if msg.expiration_time else None),
        'insertion_time': (msg.insertion_time.isoformat()
                           if msg.insertion_time else None),
        'time_next_visible': (msg.time_next_visible.isoformat()
                              if msg.time_next_visible else None),
        'pop_receipt': msg.pop_receipt,
        'dequeue_count': msg.dequeue_count
    })

    return result


@app.function_name(name="queue_trigger_message_return")
@app.generic_trigger(arg_name="msg",
                     type="queueTrigger",
                     queue_name="testqueue-message-return",
                     connection="AzureWebJobsStorage")
@app.generic_output_binding(
    arg_name="$return",
    type="blob",
    connection="AzureWebJobsStorage",
    path="python-worker-tests/test-queue-blob-message-return.txt")
def queue_trigger_message_return(msg: func.QueueMessage) -> bytes:
    return msg.get_body()


@app.function_name(name="queue_trigger_return")
@app.generic_trigger(arg_name="msg",
                     type="queueTrigger",
                     queue_name="testqueue-message-return",
                     connection="AzureWebJobsStorage")
@app.generic_output_binding(
    arg_name="$return",
    type="blob",
    connection="AzureWebJobsStorage",
    path="python-worker-tests/test-queue-blob-return.txt")
def queue_trigger_return(msg: func.QueueMessage) -> bytes:
    return msg.get_body()


@app.function_name(name="queue_trigger_return_multiple")
@app.generic_trigger(arg_name="msg",
                     type="queueTrigger",
                     queue_name="testqueue-return-multiple",
                     connection="AzureWebJobsStorage")
def queue_trigger_return_multiple(msg: func.QueueMessage) -> None:
    logging.info('trigger on message: %s', msg.get_body().decode('utf-8'))


@app.function_name(name="queue_trigger_untyped")
@app.generic_trigger(arg_name="msg",
                     type="queueTrigger",
                     queue_name="testqueue-untyped-return",
                     connection="AzureWebJobsStorage")
@app.generic_output_binding(arg_name="$return",
                            type="blob",
                            connection="AzureWebJobsStorage",
                            path="python-worker-tests/test-queue-untyped"
                                 "-blob-return.txt")
def queue_trigger_untyped(msg: str) -> str:
    return msg


@app.function_name(name="put_queue_return_multiple")
@app.generic_trigger(arg_name="req",
                     type="httpTrigger",
                     route="put_queue_return_multiple")
@app.generic_output_binding(arg_name="resp", type="http")
@app.generic_output_binding(
    arg_name="msgs",
    type="queue",
    connection="AzureWebJobsStorage",
    queue_name="testqueue-return-multiple")
def put_queue_return_multiple(req: func.HttpRequest,
                              resp: func.Out[str],
                              msgs: func.Out[typing.List[str]]):
    msgs.set(['one', 'two'])
