# Redis Cluster with Automatic Failover Demo

This project demonstrates how to set up a high-availability Redis Cluster using Docker Compose. It includes a six-node Redis cluster (3 masters, 3 replicas) and two simple client applications (Python and PHP) that can gracefully handle master node failures.

When a master node goes down, the Redis cluster automatically promotes one of its replicas to become the new master, and the client applications reconnect and continue their work with minimal interruption.

## ✨ Features

- **6-Node Redis Cluster**: Configured for high availability with 3 master nodes and 3 replica nodes.
- **Automatic Failover**: If a master node fails, a replica is automatically promoted.
- **Containerized Clients**: Simple Python and PHP applications are also containerized, demonstrating how clients connect and handle failover within a Docker network.
- **One-Command Setup**: The entire environment (Redis cluster + clients) is orchestrated with a single `docker-compose` command.
- **Easy to Test**: Simple instructions to simulate a node failure and observe the system's resilience.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## 🚀 Quick Start

1.  **Clone the Repository or Set Up Files**

    Ensure you have the project files with the following structure:

    ```
    .
    ├── docker-compose.yml
    ├── php-app
    │   ├── composer.json
    │   ├── Dockerfile
    │   └── index.php
    └── python-app
        ├── app.py
        ├── Dockerfile
        └── requirements.txt
    ```

2.  **Build and Start the Environment**

    From the root directory of the project, run the following command. This will build the application images and start all 8 containers (6 Redis nodes, 1 Python app, 1 PHP app) in the background.

    ```bash
    docker-compose up --build -d
    ```

3.  **Initialize the Redis Cluster**

    Wait a few seconds for the Redis containers to start, then execute the `redis-cli` command inside one of the containers to form the cluster.

    ```bash
    docker exec -it redis-1 redis-cli --cluster create redis-1:6379 redis-2:6379 redis-3:6379 redis-4:6379 redis-5:6379 redis-6:6379 --cluster-replicas 1
    ```

    You will see a plan for the cluster configuration. Type `yes` and press `Enter` to approve it.

4.  **View Application Logs**

    The client applications will start after a short delay (to allow the cluster to initialize). You can watch their output with this command:

    ```bash
    docker-compose logs -f python-app php-app
    ```

    You should see both apps successfully connect to the cluster and begin writing and reading keys.

## ⚙️ Testing Automatic Failover

1.  **Identify a Master Node**

    You can see the status of all nodes and identify the masters by running:
    ```bash
    docker exec -it redis-1 redis-cli cluster nodes | grep master
    ```

2.  **Stop a Master Container**

    Let's assume `redis-1` is a master. Stop its container to simulate a failure:
    ```bash
    docker stop redis-1
    ```

3.  **Observe the Recovery**

    Watch the application logs (`docker-compose logs -f python-app php-app`). You will see a brief connection error, after which the clients will automatically reconnect and resume their operations. The Redis cluster handles the failover by promoting a replica, and the client libraries adapt to the new cluster topology.

4.  **Verify the New Master**

    After about 15-20 seconds, check the cluster status again. You will see that one of the replicas has been promoted to `master`.
    ```bash
    docker exec -it redis-2 redis-cli cluster nodes
    ```

## 📁 Project Structure
```
.
├── docker-compose.yml        # Orchestrates all services (Redis nodes and client apps).
├── php-app/
│   ├── composer.json         # Defines the PHP dependency (predis/predis).
│   ├── Dockerfile            # Instructions to build the PHP application container.
│   └── index.php             # PHP script that connects to the cluster and handles failover.
└── python-app/
    ├── app.py                # Python script that connects to the cluster and handles failover.
    ├── Dockerfile            # Instructions to build the Python application container.
    └── requirements.txt      # Defines the Python dependency (redis).
```

## 🧹 Cleanup

To stop and remove all the containers, networks, and volumes created by this project, run the following command from the project's root directory:

```bash
docker-compose down -v
