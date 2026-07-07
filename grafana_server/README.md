# Automated Monitoring Stack Deployment using Jenkins, Docker, Prometheus, and Grafana


## Project Introduction

This project automates the deployment of a monitoring solution using Jenkins CI/CD. The monitoring stack consists of Prometheus for collecting metrics and Grafana for visualization. The entire application is containerized using Docker Compose, and Jenkins automatically deploys the latest configuration from GitLab whenever changes are made.

## The Problem Statement

In many organizations, monitoring servers are deployed manually, which is time-consuming and error-prone. I wanted to automate the deployment so that whenever I update the configuration in GitLab, Jenkins automatically validates and deploys the monitoring stack.

```
cd existing_repo
git remote add origin http://192.168.1.122/root/grafana_server.git
git branch -M main
git push -uf origin main
```

## Architecture

```
Developer
      │
      │ Git Push
      ▼
 GitLab Repository
      │
      ▼
 Jenkins Pipeline
      │
      ├───────────── Checkout Code
      │
      ├───────────── Validate Docker Compose
      │
      ├───────────── Deploy Containers
      │
      ▼
 Docker Compose
      │
      ├────────────── Prometheus
      │
      └────────────── Grafana
                         │
                         ▼
                  Dashboards
                         │
                         ▼
                 Monitor Linux Server
```

## Tool

**GitLab**
I stored all project files inside GitLab.

Contents:
docker-compose.yml
prometheus.yml
Jenkinsfile
README.md

Purpose:
* Version control
* Collaboration
* Source code repository 

**Jenkins**
I used Jenkins to automate deployment.

Pipeline stages:
```
Checkout

↓

Build

↓

Validate

↓

Deploy
```

**Docker Compose**

Instead of running

```
docker run
docker run
docker run
```

I can define everything inside.
```
docker-compose.yml
```

Benefits:
* Easy deployment
* Infrastructure as Code
* One command deployment

**Grafana Container**
image:
grafana/grafana-oss

Purpose:
Dashboard Visualization

Volume:
grafana-data

Purpose:
Dashboard persistence
Without volume
All dashboards disappear after restart.

**Prometheus Container**
image:
prom/prometheus

Purpose:
Collect metrics

Volume:
./prometheus.yml
Mounting configuration inside container

Another volume:
prometheus-data
Stores TSDB database.

**Data Flow**
```
Linux Server

↓

Node Exporter

↓

Prometheus

↓

Grafana

↓

Dashboard
```

**CI/CD Flow**
```
Git Push

↓

GitLab

↓

Jenkins Trigger

↓

Checkout

↓

Validate

↓

Deploy

↓

Prometheus

↓

Grafana Updated
```

***

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!). Thanks to [makeareadme.com](https://www.makeareadme.com/) for this template.

