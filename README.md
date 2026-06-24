# Expense Tracker Backend | AWS, Terraform, Docker, Kubernetes & MySQL

## Project Overview

This project demonstrates deployment of a Flask-based Expense Tracker Backend with MySQL on AWS EC2 using Terraform, Docker, Docker Hub and Kubernetes.

## Features

- JWT Authentication
- User Registration & Login
- Add Expenses
- View Expenses
- MySQL Database Integration
- Docker Containerization
- Kubernetes Deployment
- AWS EC2 Hosting

## Tech Stack

- Python
- Flask
- MySQL
- SQLAlchemy
- JWT Authentication
- Docker
- Docker Hub
- Kubernetes
- AWS EC2
- Terraform
- Git & GitHub

## Architecture

```text
Internet
    │
    ▼
AWS EC2
    │
    ▼
Kubernetes Cluster
    │
    ▼
Expense Tracker Service (NodePort)
    │
    ▼
Flask Pod
    │
    ▼
MySQL Service
    │
    ▼
MySQL Pod
```

## Application URL

http://13.232.93.175:30001

## Kubernetes Components

- MySQL Deployment
- MySQL Service
- Expense Tracker Deployment
- Expense Tracker Service

## Deployment Flow

```text
Terraform
    │
    ▼
AWS EC2
    │
    ▼
Docker Build
    │
    ▼
Docker Hub
    │
    ▼
Kubernetes Deployment
    │
    ▼
Browser Access
```

## Author

Chetan Barfa
Electronics & Telecommunication Engineering Student
Vidyalankar Institute of Technology, Mumbai
