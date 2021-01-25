FROM jupyter/datascience-notebook:7e07b801d92b

LABEL maintainer="Alberto Jaimes <yoselerratil@gmail.com>"

# update repositories
USER root
RUN  apt-get update && pip install --upgrade pip 
USER $NB_UID

# extra libraries
RUN pip install pyjanitor==0.20.10 jupyter-dash==0.3.0

# change working directory
# WORKDIR /home/jovyan/work
