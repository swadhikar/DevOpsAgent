from build_monitoring.observers.base_observer import BuildObserver
from db_library.db_lib import DBConnection


class DatabaseWriter(BuildObserver):
    """Concrete observer"""

    def update(self, build_data: dict) -> None:
        db = DBConnection()
        db.upsert('builds', build_data)

