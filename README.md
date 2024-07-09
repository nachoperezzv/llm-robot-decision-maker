# Aplicación de LLM en sistemas robóticos mediante simulador web

En este repositorio se presenta un simulador y una API que permite ejecutar un entorno en el que se prueba como un robot puede actuar y generar estrategias para conseguir objetivos en un entorno desconocido. 

## Simulador

Para llevar a cabo estos experimentos de la forma más sencilla posible se crea una web que permite controlar y visualizar las decisiones del robot así como la selección del entorno. Esto se puede ver dentro de la carpeta [simulador](./simulator/). Dentro encontrará un [README.md](./simulator/README.md) con las intrucciones para iniciar el simulador. Antes de iniciar es mejor que primero despliegue la API. 

## API

Para desplegar la API puede leer el [README.md](./api/README.md). La carpeta [api](./api/) contiene el código en python para desplegar un servicio RESTFUL con FastAPI que permite hacer uso de un LLM para probar el simulador. 

