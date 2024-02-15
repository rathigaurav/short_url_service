# FastAPI Docker Compose Configuration
This repository contains a Docker Compose configuration (`docker-compose.yml`) for running a FastAPI application along with MongoDB and Redis as dependencies.

## Prerequisites
Before running the application, ensure that you have Docker and Docker Compose installed on your machine.
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)


## Getting Started
Follow these steps to set up and run the FastAPI application:
1. **Clone the Repository:**
    ```
    git clone <repository-url>
    cd <repository-directory>
    ```
2. **Build and Run the Docker Containers:**
    ```
    docker-compose up --build
    ```
3. **Access Swagger API Docs:**
    Once the containers are running, access the FastAPI Swagger documentation by visiting [http://localhost:8000/docs]in your web browser. This will help you understand the api structure.

4. **For executing test cases:**
    I have added unit and e2e test cases
    1. brew install python
    2. pip3 install -r requirements.txt
    3. pytest -v tests/

## Additional Information
1. The FastAPI application is exposed on port 8000.
2. MongoDB is running in a docker container and is exposed on port 27018
3. Redis is running in a docker container asn is exposed on port 6378
4. Swagger API documentation is accessible at [http://localhost:8000/docs].

## Shutting Down the Containers
To stop and remove the containers, use the following command:
```
docker-compose down
```


## Design choices
1. MongoDB
    MongoDB is a NoSQL database that provides a flexible schema, allowing us to store data in a JSON-like format. This flexibility is beneficial for handling various data structures associated with URLs, such as long URLs, short URLs, and metadata.
    MongoDB scales horizontally, making it suitable for managing large datasets. This scalability can be crucial when dealing with a high volume of short URLs and their associated data.

2. Redis
    Redis is an in-memory data store, which means it can quickly retrieve data from memory rather than disk, resulting in faster read access. For a short URL service, where quick access to frequently used data is essential, Redis can significantly improve performance.

3. FastAPI:
    FastAPI is built on top of Starlette and Pydantic, leveraging asynchronous programming with Python's async and await syntax. This results in high-performance APIs with low latency, making it suitable for handling a large number of requests concurrently. My prior experince with FastApi helped me in faster development.

4. Logging:
    For logging I have used a log file: /logs/api.log where you can see the api logs.

5. Monitoring
    I haven't built for monitoring and alerting as it was optional. However if the app is deployed on AWS we can leverage AWS cloud watch for logging and Datadog for monitoring requirements.

    
