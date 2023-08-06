from kubernetes import client, config

from . import exceptions


class Client:
    def __init__(self, context=None):
        config.load_kube_config(context=context)
        self.v1 = client.CoreV1Api()

    def get_pod(self, namespace: str, labels: dict):
        resp = self.v1.list_namespaced_pod(namespace, label_selector=labels)
        if not len(resp.items):
            raise exceptions.PodNotFoundError(labels)
