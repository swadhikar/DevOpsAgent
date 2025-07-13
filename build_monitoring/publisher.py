from build_monitoring.observers.base_observer import BuildObserver


class BuildPublisher:
    def __init__(self):
        self.observers = []

    def subscribe(self, observer: BuildObserver) -> None:
        self.observers.append(observer)

    def unsubscribe(self, observer: BuildObserver) -> None:
        self.observers.remove(observer)

    def notify(self, build_data: dict) -> None:
        for observer in self.observers:
            observer.update(build_data)
