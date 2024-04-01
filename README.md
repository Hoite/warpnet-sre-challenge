# Warpnet SRE-challenge
> Author: Hoite Prins, hj.prins@alfa-college.nl

This document provides a solution for the 3 scenarios.

1. Running the application in a VM
2. Fix the application code
3. Running the application in Kubernetes

# 0. Preparation

## Create a secret key:

```bash
python3 solution/supporting-files/genkey.py
```
> Add the generated secret key to app.py on "CHANGEME!".

## Generate db
```bash
cd app/
touch sre-challenge.db
python3
>>> from app import db
>>> db.create_all()
```

## Optional; check database
```bash
cd app/
sqlite3 sre-challenge.db
sqlite> .tables # You should see a table "user"
sqlite> .exit
```

## Run application locally
You can use to following command to start the application:

```bash
cd app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app application run
```

# 1. Running the application in a VM (Vagrant)

Built for:
- Mac OS
- ARM64
- VMware Fusion

```bash
vagrant up
```
Open a browser and go to http://192.168.13.37:5000

# 2. Fixing the application code
## Problems
1. Secret Key
    - Static (did not fix, generated new one instead)
    - Is default static key from Flask documentation (fixed)
2. Passwords (fixed)
    - Plain-text
    - Logged to console
3. Authenticate() function (fixed)
    - vars in query (fixed)
    - SQL-injectable (fixed)
4. Sessions (fixed)
    - Unsafe secret key
5. Error handling (fixed)
    - No error handling
    - No error messages to interface (just a 401)
6. Rate-limiting on login (not fixed)
    - No protection against brute-force
7. TLS (not fixed)
    - No built-in TLS (fixed in deployment)
8. db in git (Because challenge && completion still here)
    - Contains plain-text password (fixed)

- Created register page

## Wants
I ran out of time, i was planning:
- A script that initializes the SECRET_KEY and database creation
- Sessions with JWT
- Logic / page to create accounts from admin-interface instead of registering (assuming intranet now)
- More time to implement all this ^ ;)

# 3. Running the application in Kubernetes

## Starting a local cluster

This solution uses `minikube` as a local cluster solution. It should run in any cluster type.

Install minikube from: https://minikube.sigs.k8s.io/docs/start/

```bash
$ minikube start
```

## Building a Docker image
### Building and uploading the image to minikube

```bash
eval $(minikube docker-env)
docker build -t sre-challenge -f solution/supporting-files/Dockerfile .
docker image save -o image.tar sre-challenge
minikube image load image.tar
```

### Alternative solution
Or, build it directly in minikube:

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
> :5000 forwards a random port to 5000, in this example it chose 61526, change accordingly to your situation.

```bash
$ curl -vk 127.0.0.1:61526
```

Or, testing the login:

```bash
$ curl -X POST http://127.0.0.1:61526/login -d "username=admin&password=supersecret"
```