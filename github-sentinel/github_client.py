from typing import List, Dict
import requests
import datetime

class GithubClient:
    def __init__(self, token: str):
        self.token = token
        self.headers = {
            'Authorization': f'token {self.token}',
        }

    def fetch_updates(self, repo: str) -> Dict:
        # 获取特定 repo 的更新 (commits, issues, pull requests)
        updates = {
            'commits': self.fetch_commits(repo),
            'issues': self.fetch_issues(repo),
            'pull_requests': self.fetch_pull_requests(repo)
        }
        return updates

    def fetch_commits(self, repo: str) -> List[Dict]:
        url = f'https://api.github.com/repos/{repo}/commits'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def fetch_issues(self, repo: str) -> List[Dict]:
        url = f'https://api.github.com/repos/{repo}/issues'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def fetch_pull_requests(self, repo: str) -> List[Dict]:
        url = f'https://api.github.com/repos/{repo}/pulls'
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def export_daily_progress(self, repo: str) -> str:
       date_str = datetime.datetime.now().strftime('%Y-%m-%d')
       issues = self.fetch_issues(repo)
       pull_requests = self.fetch_pull_requests(repo)
       filename = f'daily-progress/{repo.replace("/", "-")}-{date_str}.md'

       with open(filename, 'w') as f:
           f.write(f"# {repo} Daily Progress - {date_str}\n\n")
           f.write('## Commits\n\n')

           f.write("## Issues\n")
           for issue in issues:
               f.write(f"- {issue['title']}: #{issue['number']}\n")

           f.write("\n## Pull Requests\n")
           for pull_request in pull_requests:
               f.write(f'- {pull_request["title"]}: #{pull_request["number"]}\n')

       print(f"Daily progress exported to {filename}")
       return filename
