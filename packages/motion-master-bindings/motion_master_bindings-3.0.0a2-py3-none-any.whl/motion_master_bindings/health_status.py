"""
Health Status : Motion Master Bindings

Provides a code and description of the health of the motion-master connectivity.
"""

import enum

class HealthCode(enum.Enum):
    """
    The type of health status.
    """
    OKAY = 1

    # ERROR stars with 100
    ERROR_MESSAGE_RECEIVED_WATCHDOG = 101
    ERROR_MESSAGE_SENT_WATCHDOG = 102
    

class HealthStatus():
    """
    Provides a code, the reporting element, and a message.
    """
    def __init__(self, code, report_from,  message):
        self.code = code
        self.report_from = report_from
        self.message = message

