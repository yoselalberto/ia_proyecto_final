FROM jupyter/datascience-notebook:d113a601dbb8

LABEL maintainer="Alberto Jaimes <yoselerratil@gmail.com>"

# update repositories
USER root
RUN  apt-get update
RUN  pip install --upgrade pip 

USER $NB_UID

# extra libraries
RUN pip install pyjanitor==0.20.10

