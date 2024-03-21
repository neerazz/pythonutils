from tools.github.github_clinet import GitHubClient
from util.file_util import delete_files_or_directory, read_from_file, write_to_file


class GitHubPRAttributes:
    def __init__(self):
        self.delimiter = "|"
        self.repoOwner = None
        self.owner = None
        self.repo = None
        self.number = None
        self.title = None
        self.state = None
        self.merged_at = None
        self.commits = None
        self.additions = None
        self.deletions = None
        self.changed_files = None

    def __str__(self):
        return f"{self.repoOwner}{self.delimiter}{self.owner}{self.delimiter}{self.repo}{self.delimiter}" \
               f"{self.number}{self.delimiter}{self.title}{self.delimiter}{self.state}" \
               f"{self.delimiter}{self.merged_at}{self.delimiter}{self.commits}{self.delimiter}" \
               f"{self.additions}{self.delimiter}{self.deletions}{self.delimiter}{self.changed_files}"

    def __abs__(self):
        return f"{self.repoOwner}{self.delimiter}{self.owner}{self.delimiter}{self.repo}{self.delimiter}" \
               f"{self.number}{self.delimiter}{self.title}{self.delimiter}{self.state}" \
               f"{self.delimiter}{self.merged_at}{self.delimiter}{self.commits}{self.delimiter}" \
               f"{self.additions}{self.delimiter}{self.deletions}{self.delimiter}{self.changed_files}"


git = GitHubClient()


def get_pr_counts_of_repos(repos: list):
    pull_requests = []
    for repo in repos:
        prs = git.get_all_pull_requests(repo)
        for pr in prs:
            pr_summary = GitHubPRAttributes()
            pr_detail_head = pr["head"]
            pr_summary.owner = pr["user"]["login"]
            pr_summary.repoOwner = pr_detail_head["repo"]["owner"]["login"]
            pr_summary.repo = pr_detail_head["repo"]["name"]
            pr_summary.number = pr["number"]
            pr_summary.title = pr["title"]
            pr_summary.state = pr["state"]
            pr_summary.merged_at = pr["merged_at"]
            pr_full_detail = git.get_all_pull_request_details(pr_summary.repoOwner, pr_summary.repo, pr_summary.number)
            pr_summary.commits = pr_full_detail["commits"]
            pr_summary.additions = pr_full_detail["additions"]
            pr_summary.deletions = pr_full_detail["deletions"]
            pr_summary.changed_files = pr_full_detail["changed_files"]
            pull_requests.append(pr_summary)
    return pull_requests


def get_issues(repo: str):
    split = repo.split("/")
    org, repo_name = split[0], split[1]
    query_filters = {"labels": "rate-limiting"}
    issue_responses = git.get_issues(org, repo_name, query_filters)
    issue_url = ("", "")
    if issue_responses and len(issue_responses) > 0:
        return issue_responses[0]["url"], issue_responses[0]["number"]
    return issue_url


def get_all_issues():
    repos = read_from_file("file.txt")
    # repos = ["shared/xray-vulnerability-detection"]
    git_issues_file = "git_issues_file.txt"
    delete_files_or_directory(git_issues_file, ".")
    file_output = []
    for repo in repos:
        issue_link, issue_number = get_issues(repo)
        if issue_link == "":
            issue_link = create_issues(repo)
        if not issue_number == "":
            update_issues(repo, issue_number)
            file_output.append(f"{repo},{issue_link},UPDATED")
        else:
            file_output.append(f"{repo},{issue_link}")

    write_to_file(git_issues_file, file_output)


title = "AppSec Questionnaire for Istio Rate Limiting Implementation"
body = """
---

**Rate Limiting: Why is it Needed?**

Rate limiting is a technique for limiting network traffic. It sets a limit on how many requests a client can make to a server in a given amount of time. It's a crucial aspect of internet security and an incredibly useful tool for preventing a range of malicious behaviors:

1. **Denial-of-Service (DoS) attacks**: Without rate limits, your application could be vulnerable to DoS attacks, where an attacker could potentially make unlimited requests to your server, causing it to crash due to overload.

2. **Brute Force Attacks**: Rate limiting can also prevent brute force attacks, where an attacker attempts to gain access by trying many different passwords or access tokens in quick succession.

3. **Web Scraping and Data Theft**: If there are no restrictions on the number of requests, automated bots could scrape your website or API for valuable data.

4. **Resource Utilization**: Rate limiting can help ensure that your resources are not monopolized by a single or small group of users, ensuring fair access for all users.

5. **API Stability**: For applications that provide APIs, rate limiting helps to maintain the stability and reliability of the API by preventing it from being overwhelmed by too many requests.

When deciding on the appropriate policy, you should take into consideration factors such as the expected traffic patterns, the nature of your application, and the potential impact on user experience. It's important to ensure that rate limiting doesn't unnecessarily prevent legitimate users from using your application.

As a security team, applying these changes to the application's GitHub repositories would involve ensuring that the application's code implements the chosen rate limiting policy effectively. This could involve changes to the application's Kubernetes (k8) YAML file. It's also important to clearly communicate the appropriate policy. Need help in deciding one, feel free to contact us at the below slack channel.

To implement rate limiting, we will make necessary changes in the Kubernetes (k8) YAML file. If rate limiting is currently disabled, we will enable it by adding the appropriate configuration in the YAML file.

### For more details kindly go through the [link](https://docs.csnzoo.com/shared/analytic-infra-product/containers-kubernetes-at-wayfair/istio/development-resources/istio-subchart/istio-chart-v2/#rate-limiting).

---

_For questions and concerns please reach out to #appsec-rate-limiting._

**NOTE: Please respond to the questions by [filling out the form with details.](https://docs.google.com/forms/d/e/1FAIpQLScleYxWmTUUFkk5IsCNa2mVV8Z1bEMNz2AUGbSdSe_mTaxj_A/viewform?entry.1023539274={git_repo_name})**
        """


def create_issues(repo: str):
    data = {
        "title": title,
        "body": body.format(git_repo_name=repo),
        "labels": ["app-security", "rate-limiting"]
    }

    split = repo.split("/")
    org, repo_name = split[0], split[1]
    issue_response = git.create_issue(org, repo_name, data)
    if "url" in issue_response:
        return issue_response["url"]
    elif "message" in issue_response:
        return issue_response["message"]
    return str(issue_response)


def update_issues(repo: str, issue_number):
    data = {
        "title": title,
        "body": body.format(git_repo_name=repo),
        "labels": ["app-security", "rate-limiting"]
    }
    split = repo.split("/")
    org, repo_name = split[0], split[1]
    issue_response = git.update_issues(org, repo_name, issue_number, data)
    if "url" in issue_response:
        return issue_response["url"]
    elif "message" in issue_response:
        return issue_response["message"]
    return str(issue_response)


def start_issues_creation():
    repos = read_from_file("file.txt")
    # repos = ["shared/xray-vulnerability-detection"]
    git_issues_file = "git_issues_file.txt"
    delete_files_or_directory(git_issues_file, ".")
    file_output = []
    for repo in repos:
        issue_link = create_issues(repo)
        file_output.append(f"{repo},{issue_link}")

    write_to_file(git_issues_file, file_output)


if __name__ == '__main__':
    get_all_issues()
    # start_issues_creation()
    # repos = ["vulnerabilitiy-managment", "xray-vulnerability-detection"]
    # print("This will extract all the PRs of github projects " + str(repos))
    # pr_details = get_pr_counts_of_repos(repos)
    # for pr_detail in pr_details:
    #     print(pr_detail)
