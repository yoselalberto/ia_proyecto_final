## Tarea sobre aprendizaje autómatico supervisado

Para obtener el entorno de ejecución executa el siguiente comando:

```
docker run --rm -p 8888:8888 -e JUPYTER_ENABLE_LAB=yes -v <working_directory>:/home/jovyan/work --name <container_name> jupyter/datascience-notebook:d113a601dbb8

```  

executing `docker logs <container_name>` returns the web direction to access *jupyter_lab*, copy and paste it to a browser and you are ready.  

