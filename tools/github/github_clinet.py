import json

from tools.googlesheet.google_sheets_service import update_sheet_values
from util.httpcaller import get_session


class GitHubConfig:

    @staticmethod
    def get_session():
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'token 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'
        }
        session = get_session(headers)
        session.verify = False
        return session


class GitHubClient:
    base_url = "https://github.csnzoo.com"

    def __init__(self):
        self.config = GitHubConfig()

    def make_request(self, url):
        session = self.config.get_session()
        response = session.get(url)
        return response.json()

    def get_call(self, url: str, query_param: dict = None):
        session = self.config.get_session()
        response = session.get(url, params=query_param)
        return response.json()

    def post_call(self, url: str, data: dict = None):
        session = self.config.get_session()
        response = session.post(url, data=json.dumps(data))
        return response.json()

    def patch_call(self, url: str, data: dict = None):
        session = self.config.get_session()
        response = session.patch(url, data=json.dumps(data))
        return response.json()

    def get_All_Repos(self, org: str = "shared", page: int = 1, per_page: int = 30):
        url = f"{self.base_url}/api/v3/orgs/{org}/repos?page={page}&per_page={per_page}"
        return self.get_call(url)

    def get_all_pull_requests(self, repo: str, org: str = "shared", includeClosed: bool = True,
                              selfPROnly: bool = True):
        url = f"{self.base_url}/api/v3/repos/{org}/{repo}/pulls"
        # Create a dictionary of query parameters, and add the page number
        query_param = {"per_page": 100, "page": 1, "sort": "created", "direction": "desc"}
        if includeClosed:
            query_param['state'] = 'all'
        if selfPROnly:
            query_param['author'] = '@me'
        pull_requests = []
        while True:
            response = self.get_call(url, query_param)
            if response:
                pull_requests.extend(response)
                if len(response) < query_param['per_page']:
                    break
                else:
                    query_param['page'] += 1
            else:
                break
        return self.get_call(url, query_param)

    def get_all_pull_request_details(self, org: str, repo: str, pr_number: int):
        url = f"{self.base_url}/api/v3/repos/{org}/{repo}/pulls/{pr_number}"
        return self.get_call(url)

    def get_all_pull_request_comments(self, org: str, repo: str, pr_number: int):
        url = f"{self.base_url}/api/v3/repos/{org}/{repo}/issues/{pr_number}/comments"
        return self.get_call(url)

    def get_all_pull_request_commits(self, org: str, repo: str, pr_number: int):
        url = f"{self.base_url}/api/v3/repos/{org}/{repo}/pulls/{pr_number}/commits"
        return self.get_call(url)

    def get_all_pull_request_files(self, org: str, repo: str, pr_number: int):
        url = f"{self.base_url}/api/v3/repos/{org}/{repo}/pulls/{pr_number}/files"
        return self.get_call(url)

    def get_repo_files(self, owner: str = "shared", repo: str = None):
        url = f"{self.base_url}/api/v3/repos/{owner}/{repo}/contents"
        return self.get_call(url)

    def create_issue(self, org: str = "shared", repo: str = None, body: dict = None):
        url = f'https://github.csnzoo.com/api/v3/repos/{org}/{repo}/issues'
        return self.post_call(url, body)

    def update_issues(self, org: str = "shared", repo: str = None, issue_number=None, body: dict = None):
        url = f'https://github.csnzoo.com/api/v3/repos/{org}/{repo}/issues/{issue_number}'
        return self.patch_call(url, body)

    def get_issues(self, org, repo, query_filters):
        url = f'https://github.csnzoo.com/api/v3/repos/{org}/{repo}/issues'
        return self.get_call(url, query_filters)


class GitHubRepo:
    delimiter = "|"

    def __int__(self):
        self.id = None
        self.name = ""
        self.language = ""
        self.default_branch = ""
        self.size = ""
        self.visibility = ""
        self.gitURL = ""
        self.files = set()
        self.CVEs = set()
        self.scanned = False
        self.response_body = ""
        self.response_status = False
        self.time_in_secs = 0
        self.dependencies = ""
        self.vulnerabilities = ""
        self.createdAt = ""
        self.updatedAt = ""
        self.pushedAt = ""

    def __str__(self):
        return self.__abs__()

    def __abs__(self):
        return f"{self.name}{self.delimiter}" \
               f"{self.language}{self.delimiter}" \
               f"{self.buildTool()}{self.delimiter}" \
               f"{self.lockFile()}{self.delimiter}" \
               f"{self.default_branch}{self.delimiter}" \
               f"{self.files}{self.delimiter}" \
               f"{self.scanned}{self.delimiter}" \
               f"{self.response_body}{self.delimiter}" \
               f"{self.response_status}{self.delimiter}" \
               f"{self.time_in_secs}\n"

    def lockFile(self):
        for file_name in self.files:
            if file_name.endswith('lock') or \
                    file_name.endswith('lock.json') or \
                    file_name.endswith('lock'):
                return True
        return False

    def buildTool(self):
        if "pom.xml" in self.files:
            return "Maven"
        elif "build.gradle" in self.files or "build.sbt" in self.files:
            return "Gradle"
        elif "requirement.txt" in self.files or "requirements.txt" in self.files or \
                "requirement.lock" in self.files or "requirements.lock" in self.files or \
                "pyproject.toml" in self.files or \
                "setup.py" in self.files or "setup.cfg" in self.files:
            return "PIP"
        elif "yarn.lock" in self.files or "yarn.json" in self.files or "yarn-lock.json" in self.files:
            return "YARN"
        elif "package.json" in self.files or "package-lock.json" in self.files:
            return "NPM"
        elif "build.ps1" in self.files:
            return "PowerShell"
        elif "Package.swift" in self.files:
            return "Swift"
        elif "main.go" in self.files:
            return "GO"
        else:
            return "Other"

    def get_cell_values_for_github_metadata(self):
        return [
            str(self.id),
            str(self.name),
            str(self.default_branch),
            str(self.language),
            str(self.buildTool()),
            str(self.size),
            str(self.visibility),
            str(self.createdAt),
            str(self.updatedAt),
            str(self.pushedAt),
            str(self.gitURL),
            str(self.files),
            str(self.isK8()),
            str(self.lockFile())
        ]

    def get_cell_values_for_build_tool(self):
        return [
            str(self.name),
            str(self.language),
            str(self.buildTool()),
            str(self.lockFile()),
            str(self.default_branch),
            str(self.files)]

    def get_cell_values(self):
        return [
            str(self.name),
            str(self.language),
            str(self.buildTool()),
            str(self.lockFile()),
            str(self.default_branch),
            str(self.files),
            str(self.scanned),
            str(self.response_status),
            str(self.time_in_secs),
            str(self.dependencies)[:4000].strip(),
            str(self.vulnerabilities)[:4000].strip(),
            str(self.CVEs)[:1000].strip()]

    def isK8(self):
        for file in self.files:
            if "k8" in file.lower():
                return True
        return False


def extractFromGitHub():
    git = GitHubClient()
    file_name = "file.txt"
    file = open(file_name, "w")
    j = 2
    for i in range(1, 400):
        res = git.get_All_Repos(page=i)
        for repo in res:
            cur_repo = GitHubRepo()
            cur_repo.id = repo["id"]
            cur_repo.name = repo["name"]
            cur_repo.language = repo["language"]
            cur_repo.default_branch = repo["default_branch"]
            cur_repo.size = repo["size"]
            cur_repo.visibility = repo["visibility"]
            cur_repo.createdAt = repo["created_at"]
            cur_repo.updatedAt = repo["updated_at"]
            cur_repo.pushedAt = repo["pushed_at"]
            cur_repo.gitURL = repo["html_url"]
            cur_repo.files = set()
            cur_repo.scanned = False
            cur_repo.response_status = None
            cur_repo.response_body = None
            cur_repo.time_in_secs = None
            files = git.get_repo_files(repo=cur_repo.name)
            for entry in files:
                if "name" in entry and "size" in entry and entry["size"] > 0:
                    cur_repo.files.add(entry["name"])
            # print(cur_repo)
            # add_to_sheet(j, cur_repo)
            j += 1
            file.write(str(cur_repo))
            file.write("\n")


def add_to_sheet(row_number, cell_value: GitHubRepo):
    sheet_id = "1XoUXZ-aqkt2dMxl8PqA6Ey0JjwSHcRPT27wbvgt1o_U"
    page_id = "Github_Metadata!"
    insertRange = f"{page_id}A{row_number}:N{row_number}"
    values = cell_value.get_cell_values_for_github_metadata()
    body = {
        "range": insertRange,
        "majorDimension": "ROWS",
        "values": [values]
    }
    update_sheet_values(sheet_id, insertRange, body)


if __name__ == '__main__':
    print('This will extract all the github projects.')
    extractFromGitHub()
