from abc import abstractmethod, ABC
from db_library.db_lib import DBConnection


class BuildObserver(ABC):
    """Abstract observer"""
    @abstractmethod
    def update(self, build_data: dict) -> None:
        ...

