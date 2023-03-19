FROM python:3.11-alpine
USER root

# Install packages
RUN apk add --no-cache \
		doxygen \
		git

# Install python packages required for testing
RUN python3 -m pip install \
	coverage \
	pytest \
	pytest-cov

ENV DEV_CONTAINER=1
ENV GH_CONTAINER=1
