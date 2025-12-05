import re
import requests


class HadoopCustomHandler:
    def url_handler(url: str, node_address: str, node_port: int) -> str:
        pattern = r"http://[^:]+:\d+"

        replacement = f"http://{node_address}:{node_port}"

        new_url = re.sub(pattern, replacement, url)

        return new_url

    def get_port_from_url(url: str) -> int | None:
        port = None
        pattern = r"http://[^:]+:(\d+)/"
        match = re.search(pattern, url)
        if match:
            port = int(match.group(1))
        return port

    def read_file(node_address: str, node_port: str, hdfs_path: str):
        url = f"http://{node_address}:{node_port}/webhdfs/v1{hdfs_path}?op=OPEN"

        response = requests.get(url, allow_redirects=True)

        if response.status_code == 200:
            print(response.text)
        else:
            print(f"Error: {response.status_code}, {response.text}")

    def write_file(node_address: str, node_port: str, hdfs_path: str, file_path: bytes):
        url = f"http://{node_address}:{node_port}/webhdfs/v1{hdfs_path}?op=CREATE&overwrite=true"

        response = requests.put(url, allow_redirects=False)

        if response.status_code == 307:
            redirect_url = response.headers["Location"]

            with open(file_path, "rb") as file_data:
                response = requests.put(redirect_url, data=file_data)

            if response.status_code == 201:
                print("File created successfully.")
            else:
                print(f"Error: {response.status_code}, {response.text}")
        else:
            print(f"Error: {response.status_code}, {response.text}")

    def list_dir_contents(node_address: str, node_port: str, hdfs_path: str):
        url = f"http://{node_address}:{node_port}/webhdfs/v1{hdfs_path}?op=LISTSTATUS"

        response = requests.get(url)

        if response.status_code == 200:
            directory_listing = response.json()
            for file_status in directory_listing["FileStatuses"]["FileStatus"]:
                print(f"{file_status['pathSuffix']}: {file_status['type']}")
        else:
            print(f"Error: {response.status_code}, {response.text}")
