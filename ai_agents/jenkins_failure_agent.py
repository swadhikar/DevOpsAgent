from build_monitoring.observers.base_observer import BuildObserver
from db_library.db_lib import DBConnection
from concurrent.futures import ThreadPoolExecutor
from ai_agents.llm_helpers import analyze_log
import requests


class JenkinsFailureAgent(BuildObserver):
    def __init__(self, max_workers=3):
        self.db = DBConnection().get_client()
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def update(self, build_data: dict) -> None:
        print(f'Got status: {build_data.get("status")}')
        if build_data.get("status") != "FAILURE":
            return

        print(f"[JenkinsFailureAgent] Handling failed job: {build_data['job_name']} #{build_data['build_number']}")
        self.executor.submit(self.handle_failure, build_data)

    def handle_failure(self, build_data: dict):
        console_url = build_data.get("console_log_url")
        print(f'Console url: {console_url}')
        log_text = self.fetch_log(console_url)

        if not log_text:
            print("[Agent] Could not retrieve log.")
            return

        reason, suggestion = analyze_log(log_text, build_data)
        self.log_agent_action(build_data, reason, suggestion)

        # Optional: trigger Jenkins retry or raise a PR, etc.
        print(f"[Agent] Suggested Fix: {suggestion}")

    @staticmethod
    def fetch_log(url):
        try:
            resp = requests.get(url, auth=('jenkins', '1185acab3eabb231614e0e1e9c7e4ffae9'), timeout=10)
            return resp.text if resp.ok else None
        except Exception as e:
            print(f"[Agent] Log fetch failed: {e}")
            return None

    def log_agent_action(self, build_data, reason, suggestion):
        entry = {
            "job_name": build_data["job_name"],
            "build_number": build_data["build_number"],
            "failure_reason": reason,
            "suggestion": suggestion,
            "action_taken": "analyzed",
        }
        self.db.table("agent_actions").insert(entry).execute()


if __name__ == '__main__':
    log = JenkinsFailureAgent.fetch_log('http://localhost:8080/job/ShellScriptExecutor/164/consoleText')
    print(log)