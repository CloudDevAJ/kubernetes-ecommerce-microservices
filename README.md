# Kubernetes E-Commerce Microservices

Virtualization Lab — Sheridan College

## Overview

A containerized e-commerce application built with
Python Flask, PostgreSQL, Docker, and Kubernetes.

## Components

- Frontend Service
- Product Service
- Order Service
- PostgreSQL Database

## Learning Objectives

- Deploy independent microservices
- Configure Kubernetes Services and internal DNS
- Use Secrets and persistent storage
- Test independent scaling and self-healing


## Kubernetes Service Discovery

The application uses Kubernetes Services and internal DNS
to enable communication between microservices.

| Component | Internal Service Address |
|---|---|
| Product Service | product-service:5001 |
| Order Service | order-service:5002 |
| PostgreSQL | database:5432 |

All application components run in the `ecommerce` namespace.

Kubernetes DNS allows services to communicate without
depending on individual Pod IP addresses.

For example, the frontend retrieves products through
`http://product-service:5001/products`.

This makes communication more reliable when Kubernetes
replaces or scales application Pods.


## Independent Microservice Scaling

Tested manually scaling individual Kubernetes Deployments
without changing the other application components.

| Component | Initial Replicas | Final Replicas |
|---|---:|---:|
| Frontend | 2 | 5 |
| Product Service | 1 | 3 |
| Order Service | 1 | 2 |
| PostgreSQL | 1 | 1 |

Kubernetes successfully maintained the requested replica
counts while allowing different application components
to scale independently.

The shopping application remained accessible after scaling.


## Kubernetes Self-Healing

Tested Kubernetes self-healing by manually deleting
application Pods managed by Deployments.

### Frontend Recovery

- Desired replicas: 5
- Deleted one frontend Pod
- Kubernetes created a replacement Pod
- Deployment returned to 5 available replicas

### Product Service Recovery

- Desired replicas: 3
- Deleted one Product Service Pod
- Kubernetes created a replacement Pod
- Deployment returned to 3 available replicas

### Key Learning

Kubernetes Deployments use ReplicaSets to maintain
the desired number of application replicas.

When a Pod is deleted, Kubernetes automatically creates
a replacement without requiring manual intervention.


## PostgreSQL Database Persistence

Tested database persistence using a Kubernetes
PersistentVolumeClaim (PVC).

### Test Procedure

1. Created a customer order through the frontend.
2. Verified the order was stored in PostgreSQL.
3. Deleted the running PostgreSQL Pod.
4. Observed Kubernetes create a replacement Pod.
5. Verified the new Pod became Ready.
6. Retrieved the original customer order again.

### Results

- PostgreSQL Deployment recovered successfully.
- PersistentVolumeClaim remained Bound.
- Customer order remained available after Pod replacement.

### Key Learning

Kubernetes Pods are temporary, but PersistentVolumeClaims
provide storage that can survive Pod deletion and recreation.

Separating persistent data from the container lifecycle
helps protect application data during Pod replacement.
