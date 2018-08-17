# KubernetesImagePuller
Pre-pull images to Kubernetes cluster nodes

## Installation

1. Clone this repo
2. From the `helm` directory, install the Helm chart to your Kubernetes cluster:
    ```bash
    helm install ./ --name imagepuller --set DOCKER_USER=[your docker username] --set DOCKER_PASS=[your docker password]
    ```
3. If you don't want to put your Docker credentials on the command prompt, you can create and use a values file instead.

## Usage

Create a Kubernetes Image object like the one in `example.image.yaml` for each Docker image you'd like pulled to your cluster workers. The controller will detect this, pull the image to each worker node and update `spec.nodes` on the original Image object when that node has successfully pulled the image.

## Credits

Many thanks to Karim Boumedhel for the following blog and example which were the foundation for this project:
- https://blog.openshift.com/writing-custom-controller-python/
- https://github.com/karmab/samplecontroller
