# Dockerfile used to verify that the build command invokes the docker build
#   command with the correct context
FROM python:3.11-alpine
USER root

COPY foo.txt /home/foo.txt
