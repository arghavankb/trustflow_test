# TrustFlow

## Overview
`TrustFlow` is an automation service that minimizes manual intervention across Toman's financial operations.  
It streamlines reconciliation processes, detects anomalies, and automates the creation of financial documents—helping teams achieve greater accuracy, transparency, and efficiency.
---

## Features
- [Add a bullet list of main features here.]

---

## Project Information

| **Category**             | **Details**                                                                                                                                                                                                                                                                                                                                                             |
|--------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Programming Language** | Python 3.13                                                                                                                                                                                                                                                                                                                                                             |
| **Framework**            | Django REST                                                                                                                                                                                                                                                                                                                                                             |
| **Database**             | **Type:** PostgreSQL with Timescale extension  <br> **Persistence:** Yes                                                                                                                                                                                                                                                                                                |
| **Caching**              | **Redis** <br> **Usage:** Caching and session storage <br> **Persistence:** No                                                                                                                                                                                                                                                                                          |
| **Message Queue**        | **RabbitMQ** <br> **Usage:** Task queues and async messaging <br> **Persistence:** Yes                                                                                                                                                                                                                                                                                  |
| **External Dependencies**| **Libraries:** Django, Celery, Django REST Framework <br> **System:** `libpq-dev` <br> **Services:** AWS S3, Twilio API                                                                                                                                                                                                                                                 |
| **Entrypoints**          | **Main:** `manage.py` <br> **API:** `/api/v1/`                                                                                                                                                                                                                                                                                                                          |
| **Health Checks**        | **Readiness Probe:** `/health/ready` → `200 OK` <br> **Liveness Probe:** `/health/live` → `200 OK`                                                                                                                                                                                                                                                                      |
| **Service Types**        | **1. Django Web Server** <br> CPU: 1 core, RAM: 1 GB <br> Entrypoint: `gunicorn --config gunicorn_config.py repigma.wsgi:application` <br><br> **2. Celery Worker** <br> CPU: 1 core, RAM: 1 GB <br> Entrypoint: `gunicorn --config gunicorn_config.py repigma` <br><br> **3. Celery Beat** <br> CPU: 1 core, RAM: 1 GB <br> Entrypoint: `celery -A repigma beat -l INFO` |
| **Jobs**                 | **1. Django Migration** <br> CPU: 1 core, RAM: 1 GB <br> Entrypoint: `gunicorn --config gunicorn_config.py repigma.wsgi:application` <br><br> **2. Collect Static** <br> CPU: 1 core, RAM: 1 GB <br> Entrypoint: `python manage.py collectstatic --noinput`                                                                                                             |
| **Environment Variables**| **File:** `.env` <br> **Example Variables:** `DB_HOST`, `REDIS_HOST`, `RABBITMQ_HOST`                                                                                                                                                                                                                                                                                   |
| **Destination Address**  | **IP Address:** e.g., `192.168.1.10` <br> **NAT Required:** Yes                                                                                                                                                                                                                                                                                                         |
| **Metrics**              | **Enabled:** Yes <br> **Path:** `/metrics`                                                                                                                                                                                                                                                                                                                              |
| **Tests**                | **Enabled:** Yes <br> **1. Lint:** Flake8 <br> **2. Unit Tests with Coverage:** Django <br> **3. DB Migration Check:** Django                                                                                                                                                                                                                                           |
| **Ingress**              | **Prod:** `payrep.toman.ir` → **Published:** Yes <br> **Stage:** `payrep-staging.qcluster.org` → **Published:** Yes <br> **Dev:** `payrep-develop.qcluster.org` → **Published:** No                                                                                                                                                                                     |
| **Partner Whitelists**   | **Prod:** Enabled: Yes <br> IP Lists/Docs: [link] <br> **Stage:** Enabled: Yes, Published: Yes <br> **Dev:** Published: No                                                                                                                                                                                                                                              |

---

## Installation and Setup

### Prerequisites
- Python 3.13+
- PostgreSQL (or compatible database)
- Redis (for caching)
- RabbitMQ (for message queuing)
- [Other required dependencies]

> _Determine dependencies sensitivity and version constraints if applicable._

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://gitlab.qcluster.org/data/trustflow.git
   cd trust_flow
