# Abstract Interface

from abc import ABC, abstractmethod
from typing import Tuple, Optional


class BaseDetector(ABC):
    @abstractmethod
    def get_active_window(self) -> Tuple[Optional[str], Optional[str]]:
        pass