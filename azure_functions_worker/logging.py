# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import logging
import logging.handlers
import sys
from typing import Optional

# Logging Prefixes
CONSOLE_LOG_PREFIX = "LanguageWorkerConsoleLog"
SYSTEM_LOG_PREFIX = "azure_functions_worker"
SDK_LOG_PREFIX = "azure.functions"


logger: logging.Logger = logging.getLogger('azure_functions_worker')
error_logger: logging.Logger = (
    logging.getLogger('azure_functions_worker_errors'))

handler: Optional[logging.Handler] = None
error_handler: Optional[logging.Handler] = None


def setup(log_level, log_destination):
    # Since handler and error_handler are moved to the global scope,
    # before assigning to these handlers, we should define 'global' keyword
    global handler
    global error_handler

    if log_level == 'TRACE':
        log_level = 'DEBUG'

    formatter = logging.Formatter(f'{CONSOLE_LOG_PREFIX}'
                                  ' %(levelname)s: %(message)s')

    if log_destination is None:
        # With no explicit log destination we do split logging,
        # errors go into stderr, everything else -- to stdout.
        error_handler = logging.StreamHandler(sys.stderr)
        error_handler.setFormatter(formatter)
        error_handler.setLevel(getattr(logging, log_level))

        handler = logging.StreamHandler(sys.stdout)

    elif log_destination in ('stdout', 'stderr'):
        handler = logging.StreamHandler(getattr(sys, log_destination))

    elif log_destination == 'syslog':
        handler = logging.handlers.SysLogHandler()

    else:
        handler = logging.FileHandler(log_destination)

    if error_handler is None:
        error_handler = handler

    handler.setFormatter(formatter)
    handler.setLevel(getattr(logging, log_level))

    logger.addHandler(handler)
    logger.setLevel(getattr(logging, log_level))

    error_logger.addHandler(error_handler)
    error_logger.setLevel(getattr(logging, log_level))


def disable_console_logging() -> None:
    # We should only remove the sys.stdout stream, as error_logger is used for
    # unexpected critical error logs handling.
    if logger and handler:
        handler.flush()
        logger.removeHandler(handler)


def enable_console_logging() -> None:
    if logger and handler:
        logger.addHandler(handler)


def enable_debug_logging_recommendation():
    logging.info("To enable debug level logging, please refer to "
                 "https://aka.ms/python-enable-debug-logging")


def is_system_log_category(ctg: str) -> bool:
    """Check if the logging namespace belongs to system logs. Category starts
    with the following name will be treated as system logs.
    1. 'azure_functions_worker' (Worker Info)
    2. 'azure_functions_worker_errors' (Worker Error)
    3. 'azure.functions' (SDK)

    Expected behaviors for sytem logs and customer logs are listed below:
                  local_console  customer_app_insight  functions_kusto_table
    system_log    false          false                 true
    customer_log  true           true                  false
    """
    return ctg.startswith(SYSTEM_LOG_PREFIX) or ctg.startswith(SDK_LOG_PREFIX)
