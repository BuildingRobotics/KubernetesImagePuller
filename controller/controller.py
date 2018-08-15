import docker
import logging
import os
from kubernetes import client, config, watch

DOMAIN = "developers.comfyapp.com"

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)

    # Get Kubernetes client
    if 'KUBERNETES_PORT' in os.environ:
        config.load_incluster_config()
    else:
        config.load_kube_config()
    configuration = client.Configuration()
    configuration.assert_hostname = False
    api_client = client.api_client.ApiClient(configuration=configuration)
    crds = client.CustomObjectsApi(api_client)

    # Get Kubernetes node name
    node_name = os.environ.get('IMAGEPULLER_NODE_NAME')

    # Get Docker client
    docker_client = docker.from_env()

    logging.info('Waiting for Image CRD to come up...')
    while True:
        stream = watch.Watch().stream(crds.list_cluster_custom_object,
                                      DOMAIN, 'v1', 'images')
        for event in stream:
            try:
                if event['type'] != 'ADDED':
                    continue
                # TODO: Check if this node's status includes SchedulingDisabled
                # and if so, continue
                obj = event['object']
                name = obj['metadata']['name']
                image = obj.get('spec', {}).get('image')
                if not image:
                    logging.info('Ignoring %s; spec.image not found', name)
                    continue
                logging.info('Pulling image %s', image)
                docker_client.images.pull(image)
                # TODO: Update object with this node's name
            except Exception as e:
                logging.error(e, exc_info=True)
