# fotoalpes-microservices-examples - main

## Descripción de los servicios


#### Usuarios

- Crear un nuevo usuario
- Listar todos los usuarios
- Consultar un usuario específico

#### Productos

- Crear un nuevo producto
- Modificar un producto
- Listar todos los productos
- Consultar un producto específico

#### Ordenes

- Crear una nueva orden
- Listar todas las órdenes
- Consultar una orden específica


#### Comunicación asíncrona

Cada servicio deberia tener una copia de la estructura de la BD de los demás servicios por lo que se debe actualizar la información en cada BD cuando se hace una actualización en alguno de los servicios. Por lo anterior, cada servicio usa la cola de mensajería para notificar a los demás los cambios realizados en su respectiva BD o para actualizar la BD con los cambios realizados por los otros servicios. 

###### Notificar cambios


###### Actualizar cambios

#### API Gateway
