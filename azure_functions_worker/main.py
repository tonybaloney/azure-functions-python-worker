# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Main entrypoint."""


import argparse
import asyncio


def parse_args():
    parser = argparse.ArgumentParser(
        description='Python Azure Functions Worker')
    parser.add_argument('--host',
                        help="host address")
    parser.add_argument('--port', type=int,
                        help='id for the requests')
    parser.add_argument('--workerId', dest='worker_id',
                        help='id for the worker')
    parser.add_argument('--requestId', dest='request_id',
                        help='log destination: stdout, stderr, '
                             'syslog, or a file path')
    parser.add_argument('--log-level', type=str, default='INFO',
                        choices=['TRACE', 'INFO', 'WARNING', 'ERROR'],
                        help="log level: 'TRACE', 'INFO', 'WARNING', "
                             "or 'ERROR'")
    parser.add_argument('--log-to', type=str, default=None,
                        help='log destination: stdout, stderr, '
                             'syslog, or a file path')
    parser.add_argument('--grpcMaxMessageLength', type=int,
                        dest='grpc_max_msg_len')
    parser.add_argument('--asGrpcServer', type=bool,
                        dest='as_grpc_server', default=False)
    return parser.parse_args()


def main():
    from .utils.dependency import DependencyManager
    DependencyManager.initialize()
    DependencyManager.use_worker_dependencies()

    from . import logging
    from ._thirdparty import aio_compat
    from .logging import error_logger, logger

    args = parse_args()
    logging.setup(log_level=args.log_level, log_destination=args.log_to)

    logger.info('Starting Azure Functions Python Worker.')
    logger.info('Worker ID: %s, Request ID: %s, Host Address: %s:%s',
                args.worker_id, args.request_id, args.host, args.port)

    try:
        return aio_compat.run(start_async(
            args.host, args.port, args.worker_id,
            args.request_id, args.as_grpc_server))
    except Exception:
        error_logger.exception('unhandled error in functions worker')
        raise


async def start_async(host, port, worker_id, request_id, as_grpc_server):
    from . import dispatcher
    from .testutils import create_server

    if as_grpc_server:
        loop = asyncio.get_event_loop()
        dis = dispatcher.Dispatcher(loop, '127.0.0.1', port, 'worker_id',
                                    'request_id', 60.0)
        server = create_server(port, loop, dis)
        server.start()
        await loop.create_future()
    else:
        disp = await dispatcher.Dispatcher.connect(host=host, port=port,
                                                   worker_id=worker_id,
                                                   request_id=request_id,
                                                   connect_timeout=5.0)

        await disp.dispatch_forever()
