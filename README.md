# Warpnet SRE Challenge

Welcome to the Site Reliability Engineering (SRE) challenge, where your SRE skills will be put to the test. You'll deploy an application in both a traditional and Kubernetes environment, showcasing your ability to orchestrate complex systems. From defining Kubernetes manifests to fixing bugs and ensuring good observability, this challenge mirrors real-world scenarios encountered by our SREs. Whether you're a seasoned professional or a newcomer eager to explore complex cloud environments, this challenge offers platform to demonstrate your expertise.

## Instructions

```bash
git clone https://github.com/Hoite/warpnet-sre-challenge
cd warpnet-sre-challenge/app
```

1. Create a secret key:

```bash
python3 solution/supporting-files/genkey.py
```
> Add the generated secret key to app.py on "CHANGEME!".

You can use to following command to start the application:

```bash
cd app
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask --app application run
```

Test the application by opening [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

