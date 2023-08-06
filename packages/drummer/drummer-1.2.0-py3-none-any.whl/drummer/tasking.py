# -*- coding: utf-8 -*-
from drummer.foundation import Response, StatusCode

class Task:
    """Base class for tasks.

    This class is subclassed by user-defined tasks.

    Attributes:
        config: Dict with environment configuration.
        logger: Logger object.

    """

    def __init__(self, config, logger):

        self.config = config
        self.logger = logger

    def run(self, args):
        raise NotImplementedError('This method must be implemented by a real task')
