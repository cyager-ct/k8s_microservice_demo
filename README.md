# Building a Flask Microservice on Kubernetes and Amazon EKS

Kubernetes is a popular container orchestration platform that allows containerized applications to run on clusters of virtual or physical machines.  In the cloud development world, this ability to manage containers across compute resources makes it extremely popular, and well-suited for a microservice architecture.  In this blog, I'm going to show you how to run a Dockerized Flask API on local Kubernetes resources using the Kubernetes mocking application minikube, and then how to transition those resources to AWS Elastic Kubernetes Service (EKS).  

## Requirements
* minikube - `brew install minikube`
* kubectl - `curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/amd64/kubectl"`
* Docker - install from [their website](https://docs.docker.com/desktop/mac/install/)

## Terminology
First, a little terminology to be familiar with.  

* Nodes:  Nodes are the machines that are running tasks that Kubernetes has assigned to them.  
* Pods:  Pods are groups of containers that are deployed to nodes.  All containers on a pod share some underlying resources.
* Service:  The service resource sits between the pods and the network.  It routes requests to the correct pod.

## Running service locally on minikube

1.  Start minikube - this will spin up a docker container running minikube, which is a local Kubernetes environment.  It will also configure kubectl to use the minikube cluster and default namespace.
    ```
    minikube start
    ```
    To view a web-based dashboard, run 
    ```
    minikube dashboard
    ```
2.  Configure your terminal to use the minikube docker env for the current session
    ```
    eval $(minikube -p minikube docker-env)
    ```

3.  Build docker container for flask app
    ```
    docker build . --tag flask-docker-demo-app
    ```

    To run Run flask app docker container locally on port 5000
    ```
    sudo docker run --name flask-docker-demo-app -p 5000:5000 flask-docker-demo-app
    ```
    If you stop the container, restart it by running
    ```
    docker start -a flask-docker-demo-app
    ```

4.  To run this service in kubernetes, we need two resources:  a service and a deployment.  These are defined in k8s/service.yaml and k8s/deployment.yaml respectively, although they could also be defined in one file.  The deployment tells kubernetes how to create pods running our containerized application.  The service defines how we can interact with our deployment through the network.  

    The deployment file tells kubernetes to create 3 pods (`spec.replicas`), and applies a template to each.  This template includes some metadata and a spec, which in turn defines what containers to run on the pod.  In this case, we want the docker container for our flask application that we just defined.  We also set `imagePullPolicy: Never` to ensure that our pod uses the local container image, instead of trying to pull one down from Dockerhub.  We then expose port 5000, so we can reach it through our service.

    The `service.yaml` file instructs kubernetes to create a service of type `LoadBalancer`, while exposing port 5000 to the network.  This port is then routed to port 5000 on the pods, which is the one we exposed in `deployment.yaml`.  

5.  To create a local IP for your service running on minikube, run 
    ```
    minikube service flask-service
    ```

## Running service on EKS
1.  Create an ECR repository to store docker image.  
    * The console will list push commands to enable you to push the docker image from your command line

2.  Create an EKS cluster to run kubernetes resources
3.  When that's done building, run 
    ```
    aws eks update-kubeconfig --name [cluster name]
    ```
    This will configure kubectl to work with EKS cluster.

4.  Create a role through IAM.  The role must have the following permission policies:
    * AmazonEKSWorkerNodePolicy
    * AmazonEC2ContainerRegistryReadOnly
    * AmazonEKS_CNI_Policy

5.  Create a node group.  Node groups provision compute resources to run the kubernetes cluster.  Assign the node group the role just created to allow it to provision resources.

4.  Once kubectl is connected to EKS cluster, run 
    ```
    kubectl apply -f service.yaml
    kubectl apply -f deployment.yaml
    ```
    The EKS cluster will then spin up the requested kubernetes resources and divide them among the nodes in the node group.  In this case, `service.yaml` will manifest as a Classic Load Balancer, and our pods will be divvied up among EC2 instances as nodes.

If everything goes according to plan, you should be able to reach your service running on the standard HTTP port 80 over the internet.  Navigate to the EC2 console, and click on Load Balancers on the column on the left.  Open the details view for the load balancer, and find the DNS name.  Copy this into the address bar of your browser and load the page, and you should see our welcome message!
