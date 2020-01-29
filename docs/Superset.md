# Apache Superset
## Overview
* [History and Anatomy](https://www.datacouncil.ai/hubfs/DataEngConf/Data%20Council/Slides%20SF%2019/The%20history%20and%20anatomy%20of%20Apache%20Superset.pdf)

## Installations
### Docker
* [Superset with Docker](https://github.com/apache/incubator-superset/blob/fce49680d75d84c9c9267ccba5688bc7f4673e66/docker/README.md)
* [Running Apache Superset in a Docker](https://medium.com/faun/docker-image-of-apache-superset-400cf4855b9)
* Docker and external services:
  * https://stackoverflow.com/questions/49148920/how-to-connect-external-service-from-docker-service
  * https://stackoverflow.com/questions/43762537/connect-docker-compose-to-external-database
  * https://github.com/docker/compose/issues/1110
  * https://github.com/docker/compose/issues/2478
  * https://docs.docker.com/compose/extends/
  * https://nickjanetakis.com/blog/docker-tip-65-get-your-docker-hosts-ip-address-from-in-a-container
  * 
* Steps:
  *  Install Docker on Mac
  * `git clone https://github.com/apache/incubator-superset/`
  * Comment out references to `db` in `docker-compose.yml`
  * Figure out how to reference the host OS from inside Docker. See e.g. 
    [this](https://forums.docker.com/t/accessing-host-machine-from-within-docker-container/14248/11). 
    This hostname will be used in the SQLAlchemy DB URI.
  * Maybe create PostGres user and database. In `psql`:
    * `CREATE USER superset_user WITH PASSWORD 'superset';`
    * `CREATE DATABASE superset;`
    * `GRANT ALL PRIVILEGES ON DATABASE superset to superset_user;`
  * Create the Superset config file:
    * Ensure that [superset_config.py](https://github.com/apache/incubator-superset/blob/master/docker/pythonpath_dev/superset_config.py) 
      will load the `superset_config_docker.py`
    * `cp ./docker/pythonpath_dev/superset_config_local.example ./docker/pythonpath_dev/superset_config_docker.py`
    * Update `./docker/pythonpath_dev/superset_config_docker.py`. E.g. the may be: 
    `postgresql+psycopg2:///superset`
  * Ensure that `unix_socket_directories` in `postgresql.conf` is set to `/var/run/postgresql`. May need 
    to `sudo mkdir /var/run/postgresql`.
  * In case PostGres needs to be cycled:
    * `sudo -u postgres  pg_ctl -D /Library/PostgreSQL/12/data stop` 
  * `docker-compose up`
  * If successful, you may see SQLAlchemy running DB migration.
  * Browse to http://localhost:8088/ to log in (admin/admin, as set up in `docker-init.sh`)
  * If the server seems to be up and healthy but the UI isn't responding, the JS libraries might be 
    installing and can take ~30min
  * Add a new DB to start playing with data 
    * `postgresql+psycopg2://superset_user:superset@host.docker.internal/superset`
  * 
* Possible errors during installation:
```
superset_1         | INFO:root:Configured event logger of type <class 'superset.utils.log.DBEventLogger'>
superset_1         | INFO:root:logging was configured successfully
superset_1         | ERROR:flask_appbuilder.security.sqla.manager:DB Creation and initialization failed: (psycopg2.OperationalError) could not connect to server: No such file or directory
superset_1         | 	Is the server running locally and accepting
superset_1         | 	connections on Unix domain socket "/var/run/postgresql/.s.PGSQL.5432"?
superset_1         | 
superset_1         | (Background on this error at: http://sqlalche.me/e/e3q8)
superset-worker_1  | INFO:root:logging was configured successfully
superset-worker_1  | ERROR:flask_appbuilder.security.sqla.manager:DB Creation and initialization failed: (psycopg2.OperationalError) could not connect to server: No such file or directory
superset-worker_1  | 	Is the server running locally and accepting
superset-worker_1  | 	connections on Unix domain socket "/var/run/postgresql/.s.PGSQL.5432"?
```
* PostGres or SQLAlchemy DB URI error e.g.
  * Socket path is different: `/tmp/.s.PGSQL.5432`. See https://stackoverflow.com/questions/5500332/cant-connect-the-postgresql-with-psycopg2
  * Host OS cannot be accessed
  * URI is incorrect
