# ia_proyecto_final
proyecto final de la inteligencia artificial


## Usage 


```
docker build -t jupyter_datascience .  
docker run --rm -p 8888:8888 -e JUPYTER_ENABLE_LAB=yes -v ~/proyectos/posgrado/ia/ia_proyecto_final/:/home/jovyan/work --name ia jupyter_datascience
```


