from google.cloud import resource_manager
from google.oauth2 import service_account

# Path to your service account key file
key_path = "/Users/nb336n/Documents/secrets/inst-vulnerability-mnt-svc-prod.json"

# Authenticate using the service account key file
credentials = service_account.Credentials.from_service_account_file(key_path)

# Create a Resource Manager client with the specified credentials
client = resource_manager.Client(credentials=credentials)


def list_folders(parent_id=""):
    """Lists all folders under the given parent."""
    folders = []
    for folder in client.list_folders(parent=parent_id):
        folders.append(folder)
    return folders


def list_projects(parent_id=""):
    """Lists all projects under the given parent."""
    projects = []
    for project in client.list_projects(parent=parent_id):
        projects.append(project)
    return projects


def print_all_folders_subfolders_and_projects(parent_id=""):
    """Prints a list of all folders, sub-folders, and projects in the organization."""
    folders = list_folders(parent_id=parent_id)
    for folder in folders:
        print(f"Folder: {folder.display_name} ({folder.name})")
        subfolders = list_folders(parent_id=folder.name)
        for subfolder in subfolders:
            print(f"Subfolder: {subfolder.display_name} ({subfolder.name})")
        projects = list_projects(parent_id=folder.name)
        for project in projects:
            print(f"Project: {project.project_id} ({project.name})")


if __name__ == "__main__":
    gcp_wayfair_project = "gcp.wayfair.com/825417849120"
    wayfair_project = "wayfair.com/831632755848"
    print_all_folders_subfolders_and_projects(wayfair_project)
