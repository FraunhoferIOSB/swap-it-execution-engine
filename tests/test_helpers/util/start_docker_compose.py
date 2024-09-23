# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)

from python_on_whales import docker, DockerClient
import threading
class DockerComposeEnvironment:
    def __init__(self, services):
        self.services = services
        self.container_names = []
        self.thread = None
        self.docker = None

    def start_docker_compose(self):
        self.docker = DockerClient(compose_files=["./tests/test_helpers/util/docker-compose.yaml"])
        self.docker.ps(all=True, filters={"name": self.container_names})
        print("self.container_names", self.container_names)
        print("docker.container", self.docker.container)
        print("docker.context", self.docker.context)
        print("docker.image", self.docker.image)
        self.docker.compose.up(services=self.services, pull="missing")

    def run_docker_compose(self):
        self.thread = threading.Thread(target=self.start_docker_compose)
        self.thread.start()

    def stop_docker_compose(self):
        self.docker.compose.down(self.services)
        #docker.stop(self.container_names)
        #self.docker.kill(self.docker.container)
        #self.thread._stop()