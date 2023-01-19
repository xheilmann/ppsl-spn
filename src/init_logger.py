import sys
import logging
import time


def init_logger(logging_level=18):
    """
    Initializes the  logger, and adds 3 cutsom levels:
    - DEBUG_SPN_COMMUNICATION(15): Shows all received and send messages and their header
    - DEBUG_SPN(16): -
    - INFO_SPN(18): Shows start and fine of exercises


    :param logging_level: the used logging level to be showed. All messages greater or equal to the level will be shown.
    """

    logging.addLevelName(15, "DEBUG_SPN_COMMUNICATION")

    def debug_spn_communication(self, message, *args, **kws):
        if self.isEnabledFor(15):
            # Yes, logger takes its '*args' as 'args'.
            self._log(15, message, args, **kws)

    logging.addLevelName(16, "DEBUG_SPN")

    def debug_spn(self, message, *args, **kws):
        if self.isEnabledFor(16):
            # Yes, logger takes its '*args' as 'args'.
            self._log(16, message, args, **kws)

    logging.addLevelName(18, "INFO_SPN")

    def info_spn(self, message, *args, **kws):
        if self.isEnabledFor(18):
            # Yes, logger takes its '*args' as 'args'.
            self._log(18, message, args, **kws)

    logging.basicConfig(level=18)

    logging.Logger.debug_spn = debug_spn
    logging.Logger.info_spn = info_spn
    logging.Logger.debug_spn_communication = debug_spn_communication

    logging.getLogger().setLevel(logging_level)
