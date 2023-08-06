import re
from typing import Callable, Optional, List

from adhesive.graph.BaseTask import BaseTask


class ExecutionBaseTask:
    """
    A task implementation.
    """
    def __init__(self,
                 code: Callable,
                 *expressions: str) -> None:
        self.re_expressions = list(map(re.compile, expressions))
        self.code = code
        self.expressions = expressions

