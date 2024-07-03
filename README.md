# Django OMS Service

## Overview

This project is an Order Management System (OMS) built with Django. It integrates with various services such as a Master Data service for product information, a PPL service for promotions, and handles cart and checkout operations. The project supports different types of promotions including discount, BOGO, Buy X Get Y, and point purchase promos.

## Setup

### Prerequisites

- Python 3.x
- Django
- gRPC and Protocol Buffers
- `protobuf` and `grpcio-tools` packages

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repository/oms-service.git
    cd oms-service
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Generate gRPC code from proto files:
    ```bash
    python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. oms/grpc/protos/promo.proto
    ```

5. Apply migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

7. Run the development server:
    ```bash
    python manage.py runserver
    ```
