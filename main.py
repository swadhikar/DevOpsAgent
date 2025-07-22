from build_monitoring.publisher import BuildPublisher
from build_monitoring.pollers.jenkins_poller import JenkinsPoller
from build_monitoring.observers.db_writer import DatabaseWriter
from ai_agents.jenkins_failure_agent import JenkinsFailureAgent

jenkins_url = 'http://localhost:8080/'
jenkins_user = 'swadhikar'
jenkins_token = '11f22f72a7957f823d8fbe985500944237'

# pubsub
publisher = BuildPublisher()

# register
publisher.subscribe(DatabaseWriter())
publisher.subscribe(JenkinsFailureAgent())

# poller
poller = JenkinsPoller(publisher)
poller.run_once()
