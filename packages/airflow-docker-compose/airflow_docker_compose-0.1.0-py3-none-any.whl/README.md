# airflow-docker-compose
[![CircleCI](https://circleci.com/gh/airflowdocker/airflow-docker-compose.svg?style=svg)](https://circleci.com/gh/airflowdocker/airflow-docker-compose) [![codecov](https://codecov.io/gh/airflowdocker/airflow-docker-compose/branch/master/graph/badge.svg)](https://codecov.io/gh/airflowdocker/airflow-docker-compose)

## Description
A reasonably light wrapper around `docker-compose` to make it simple to start a local
airflow instance in docker.

## Configuration

The following operator defaults can be set under the `airflowdocker` namespace:

* force_pull (boolean true/false)
* auto_remove (boolean true/false)
* network_mode

For example, to set `force_pull` to False by default set the following environment variable like so:

```bash
export AIRFLOW__AIRFLOWDOCKER__FORCE_PULL=false

```
