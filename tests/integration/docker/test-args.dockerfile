# Dockerfile used to verify that the build command passes in the correct args
FROM python:3.11-alpine
USER root

ARG FOO
ARG BAR

ENV FOO=$FOO
ENV BAR=$BAR
