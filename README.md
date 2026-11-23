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
