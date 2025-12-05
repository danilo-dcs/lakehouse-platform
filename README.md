# Lakehouse Platform

## VM set up steps

Create the docker_volumes folder, under the $HOME dir:

```
mkdir $HOME/docker_volumes
```

Setting user permissions to the volume's folder:

```
sudo chown -R $USER:$USER $HOME/docker_volumes && sudo chmod -R 755 $HOME/docker_volumes
```

Make sure to install NGINX following the set up steps specified on the nginx folder: [link](./nginx/README.md)

## Lauching the dev infrastructure

### Environment Setup

1. Make sure to create the `.env` file in the root directory, following the `.env.example` file (also in the root directiory).

This file contains important variables for the backend api and the frontend applications.

2. Run the command below:
```
docker-compose up -d --build
```
