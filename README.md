# Microservices communication using RabbitMQ
Built an inventory management system that aims to efficiently manage inventory items, track stock levels, and handle orders through a microservices architecture.  
The system utilizes RabbitMQ for inter-service communication and Docker for containerisation, thus ensuring scalability, modularity, and ease of deployment.

## Technologies Used 
- Docker
- Python
- MongoDB (with persistent storage)
- RabbitMQ

## Usage 
Clone the git repository.
When running project for the first time, run this command in the directory.
```
  docker volume create mongodb_data
```
In the directory run the following commands  
```
  docker-compose build
  docker-compose up
```
then in a browser go to  
```
  localhost:8001
```
to view the Inventory Management System 
and to view the RabbitMQ Dashboard go to
```
  localhost:15672
```
where the default credentials are guest and guest
