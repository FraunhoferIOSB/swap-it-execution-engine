from python_on_whales import docker
import threading
class DockerComposeEnvironment:
    def __init__(self, services):
        self.services = services
    def start_docker_compose(self):
        docker.compose.up(self.services)
    def run_docker_compose(self):
        x = threading.Thread(target=self.start_docker_compose)
        x.start()
    def stop_docker_compose(self):
        docker.compose.down(self.services)