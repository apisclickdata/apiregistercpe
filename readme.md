### En este caso solo se usa Docker para desplegar la API en AppRunner y no Kubernetes

### Generar las imágenes desde el docker-compose

```
docker compose -f docker-compose-aws.yaml build
```

### Vincular la cuenta de AWS con la cuenta local de Docker

```
docker login -u AWS -p $(aws ecr get-login-password --region us-east-1) 254143684691.dkr.ecr.us-east-1.amazonaws.com
```

### Para subir las imágenes locales a ECR

```
docker compose -f docker-compose-aws.yaml push
```
