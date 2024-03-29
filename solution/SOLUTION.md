This document provides a soloution for the 3 scenarios.

# Running the application in a VM

# Fixing the appliation code

# Running the application in Kubernetes

## Building a Docker image

## Starting a local cluster

In this soloution uses `minikube` as a local cluster soloution. You are allowed
to deploy it on any cluster of you choosing.

Install minikube from: https://minikube.sigs.k8s.io/docs/start/

```bash
$ minikube start
```

## Building and uplaoding the image to minikube

```bash
docker build -t sre-challenge -f solution/supporting-files/Dockerfile .
docker image save -o image.tar sre-challenge
minikube image load image.tar
```

Or, build it directlly in minikube:

```bash
minikube image build -t sre-challenge -f solution/supporting-files/Dockerfile .
```

## Deploying application

```bash
minikube> kubectl create namespace sre-challenge
minikube> kubectl create deployment sre-challenge --image sre-challenge --port 5000 --namespace sre-challenge --dry-run --output yaml > sre-deployment.yaml
```

Add `imagePullPolicy: Never` to the yaml so that it works (under `spec.template.spec.containers`)

```bash
minikube> kubectl apply -f sre-deployment.yaml
minikube> kubectl expose deployment sre-challenge --type=NodePort --namespace sre-challenge
```

### Accessing the application

```bash
minikube> kubectl port-forward deployment/sre-challenge :5000 --namespace sre-challenge

Forwarding from 127.0.0.1:61526 -> 5000
Forwarding from [::1]:61526 -> 5000
```

```bash
$ curl -vk 127.0.0.1:61526
```

Or, testing the login:

```bash
$ curl -X POST http://127.0.0.1:61526/login -d "username=admin&password=supersecret"
```