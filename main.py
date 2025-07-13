from build_monitoring.publisher import BuildPublisher
from build_monitoring.pollers.jenkins_poller import JenkinsPoller
from build_monitoring.observers.db_writer import DatabaseWriter

jenkins_url = 'http://localhost:8080/'
jenkins_user = 'swadhikar'
jenkins_token = '11f22f72a7957f823d8fbe985500944237'

# pubsub
publisher = BuildPublisher()
db_observer = DatabaseWriter()

# register
publisher.subscribe(db_observer)

# poller
poller = JenkinsPoller(publisher)
poller.run_once()
