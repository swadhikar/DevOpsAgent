import requests
from build_monitoring.publisher import BuildPublisher


class JenkinsPoller:
    def __init__(self, publisher: BuildPublisher):
        self.base_url = "http://localhost:8080"
        self.auth = ('jenkins', '1185acab3eabb231614e0e1e9c7e4ffae9')
        self.publisher = publisher

    def get_all_jobs(self):
        url = f"{self.base_url}/api/json?tree=jobs[name,url]"
        response = requests.get(url, auth=self.auth)
        if response.status_code != 200:
            print("[JenkinsPoller:get_all_jobs] Failed to get job list")
            print(response.text)
            return []

        job_names = [job['name'] for job in response.json()['jobs'] if 'multi' not in job['name']]
        print(f'[JenkinsPoller:get_all_jobs] Got response\n{job_names} {type(job_names)}')
        return job_names

    def fetch_latest_build(self, job_name: str) -> dict | None:
        url = f"{self.base_url}/job/{job_name}/lastBuild/api/json"
        print(f'{url=}')
        response = requests.get(url, auth=self.auth)
        if response.status_code != 200:
            print(f"[JenkinsPoller:fetch_latest_build] Failed to fetch build for job: {job_name}")
            return None

        build_info = response.json()

        # skip in-progress builds
        status = build_info.get("result")  # may be None
        if not status:  # status = None → IN_PROGRESS
            print(f"[JenkinsPoller:fetch_latest_build] Skipping {job_name} #{build_info['number']} — still running")
            return None

        build_data = {
            "job_name": job_name,
            "build_number": build_info["number"],
            "status": build_info.get("result"),
            "duration_ms": build_info.get("duration"),
            "timestamp": build_info.get("timestamp"),
            "triggered_by": build_info.get("actions", [{}])[0].get("causes", [{}])[0].get("userName", "SCM/Auto"),
            "parameters": {
                "params": build_info.get("actions", [{}])[1].get("parameters", [])
            },
            "branch": "main",
            "url": build_info.get("url"),
            "console_log_url": f"{self.base_url}/job/{job_name}/{build_info['number']}/consoleText"
        }
        return build_data

    def run_once(self):
        for job_name in self.get_all_jobs():
            build_data = self.fetch_latest_build(job_name)
            if build_data:
                self.publisher.notify(build_data)
