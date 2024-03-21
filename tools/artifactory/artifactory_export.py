from collections import OrderedDict
from typing import List

from tools.googlesheet.google_sheets_service import update_sheet_values
from util.file_util import append_to_file
from util.httpcaller import get_session

sheet_id = "1XoUXZ-aqkt2dMxl8PqA6Ey0JjwSHcRPT27wbvgt1o_U"
page_id = "Dockers!"
chunk_size = 50


class JFrogConfig:

    def get_session(self):
        session = get_session({
            "Authorization":
                "Basic c2VjdXJpdHlfYXV0b21hdGlvbjpBS0NwOGtxcWppSHVLMWhuS2hCQUZkdnR6TWNUcktGOE16MjJDamVTdTZWOGpBSk15b2FVaDZOeVJKMmF4VFd1OFhxUE1vb2Y4"})
        session.verify = False
        return session


class JFrogClient:
    artifactory_url = "https://artifactorybase.service.csnzoo.com"
    xray_url = "https://artifactorybase.service.csnzoo.com"
    config = JFrogConfig()

    def get_call(self, url: str, query_param: dict = None):
        session = self.config.get_session()
        response = session.get(url, params=query_param)
        return response.json()

    def get_artifactory_resource(self, repo, deep=1):
        url = f"{self.artifactory_url}/artifactory/api/storage/{repo}"
        return self.get_call(url, {"deep": deep})

    def get_all_docker_images(self, image_repo):
        repo_images = []
        repo_artifacts = self.get_artifactory_resource(image_repo)
        for entry in repo_artifacts["children"]:
            if entry["folder"]:
                repo_images.append(entry["uri"])
        return repo_images

    def get_image_tags(self, image_path):
        image_tags = []
        repo_artifacts = self.get_artifactory_resource(image_path)
        for entry in repo_artifacts["children"]:
            if entry["folder"]:
                image_tags.append(entry["uri"])
        return image_tags

    def get_image_layers_paths(self, image_path):
        image_layers = []
        repo_artifacts = self.get_artifactory_resource(image_path)
        for entry in repo_artifacts["children"]:
            image_layers.append(entry["uri"])
        return image_layers

    def get_image_details(self, image_path: str):
        print(f"This will extract The Docker : {image_path} details from Artifactory.")
        image_details = OrderedDict()
        manifest_response = self.get_artifactory_resource(image_path + "/manifest.json")
        image_details["repo"] = manifest_response["repo"]
        image_path = manifest_response["path"]
        image_path_split = image_path.split("/")
        image_details["image_name"] = f"{image_path_split[1]}/{image_path_split[2]}"
        image_details["image_tag"] = f"{image_path_split[3]}"
        image_details["created"] = manifest_response["created"]
        image_details["createdBy"] = manifest_response["createdBy"]
        image_details["lastModified"] = manifest_response["lastModified"]
        image_details["modifiedBy"] = manifest_response["modifiedBy"]
        manifest_json = manifest_response["downloadUri"]
        manifest_json_response = self.get_call(manifest_json)
        image_layers = list()
        total_size = manifest_json_response["config"]["size"]
        image_details["imageHash"] = manifest_json_response["config"]["digest"]
        for layer in manifest_json_response["layers"]:
            image_layers.append(layer["digest"])
            total_size += layer["size"]
        image_details["image_layers"] = image_layers
        image_details["total_size"] = total_size
        return image_details


def format_image_details(image_detail: dict):
    return "|".join([str(imageDetailedItem) for imageDetailedItem in image_detail.values()])


def get_all_wayfair_images(client: JFrogClient()):
    repo = "docker-prod-deployed_lclsnc/wayfair"
    return client.get_all_docker_images(repo)


def add_all_wayfair_docker_images_to_sheet():
    repo = "docker-prod-deployed_lclsnc/wayfair"
    add_to_sheet(client.get_all_docker_images(repo), "A:A")


def write_all_wayfair_image_details_to_file():
    wayfair_repo = "docker-prod-deployed_lclsnc/wayfair"
    artifactory_client = JFrogClient()
    images = artifactory_client.get_all_docker_images(wayfair_repo)
    for image in images:
        imageTags = artifactory_client.get_image_tags(f"{wayfair_repo}{image}")
        for imageTag in imageTags:
            try:
                image_details = artifactory_client.get_image_details(f"{wayfair_repo}{image}{imageTag}")
                append_to_file("all_wayfair_images.txt", [format_image_details(image_details)])
            except KeyError:
                print("There was an error getting image details.")


def add_to_sheet(cell_value: List[List], cell_range, initial_row=1):
    row_number = initial_row
    for i in range(0, len(cell_value), chunk_size):
        start_index = i
        end_index = i + chunk_size
        chunk_cell_value = cell_value[start_index:end_index]
        #  Converting when there is only Item in cell value.
        if chunk_cell_value and type(chunk_cell_value[0]):
            temp_chunk = cell_value[start_index:end_index]
            chunk_cell_value.clear()
            for item in temp_chunk:
                chunk_cell_value.append([item])

        insertRange = f"{page_id}{cell_range[0]}{row_number + start_index}:{cell_range[0]}{row_number + end_index}"
        body = {
            "range": insertRange,
            "majorDimension": "ROWS",
            "values": [chunk_cell_value]
        }
        update_sheet_values(sheet_id, insertRange, body)


if __name__ == '__main__':
    print('This will extract all the Docker Repos from Artifactory.')
    client = JFrogClient()
    # repo = "docker-prod-deployed_lclsnc/wayfair"
    # imagesNames = client.get_all_docker_images(repo)
    # write_to_file("docker_images.txt", imagesNames)
    # image_name = "docker-prod-deployed/wayfair/aa714q-test-app/de2acf9-main"
    # image_details = client.get_image_details(image_name)
    # print(f"Image Details of {image_name}: \n {image_details}")
    # write_to_file("Image_details.txt", [format_image_details(image_details)])
    write_all_wayfair_image_details_to_file()
