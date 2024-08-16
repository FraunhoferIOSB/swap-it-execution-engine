# Licensed under the MIT License.
# For details on the licensing terms, see the LICENSE file.
# SPDX-License-Identifier: MIT

# Copyright 2023-2024 (c) Fraunhofer IOSB (Author: Florian Düwel)

class ServiceInfo:

    def __init__(self, service_uuid: str, task_uuid: str, completed:bool, service_name: str):
        self.service_uuid = service_uuid
        self.task_uuid = task_uuid
        self.completed = completed
        self.service_name = service_name

class ExecutionList:

    def __init__(self):
        self.services = []

    def add_service(self, service: object):
        self.services.append(service)

    def remove_service(self):
        for i in range(len(self.services)):
            if self.services[i].completed == True:
                service_uuid = self.services[i].service_uuid
                task_uuid = self.services[i].task_uuid
                service_name = self.services[i].service_name
                del self.services[i]
                return service_uuid, task_uuid, service_name
        return None, None, None

    def set_service_to_completed(self, service_uuid: str, task_uuid: str):
        for i in range(len(self.services)):
            if (str(self.services[i].service_uuid) == str(service_uuid) and str(self.services[i].task_uuid) == str(task_uuid)):
                self.services[i].completed = True
                return True
        return False