"""Setup at app startup"""
import os
import sqlalchemy
from flask import Flask, render_template, request, redirect, url_for, flash
from yaml import load, Loader




app = Flask(__name__)
app.secret_key = 'super secret key'

# def init_connection_engine():
#     """ initialize database setup
#     Takes in os variables from environment if on GCP
#     Reads in local variables that will be ignored in public repository.
#     Returns:
#         pool -- a connection to GCP MySQL
#     """
#
#
#     # detect env local or gcp
#     if os.environ.get('GAE_ENV') != 'standard':
#         try:
#             variables = load(open("app.yaml"), Loader=Loader)
#         except OSError as e:
#             print("Make sure you have the app.yaml file setup")
#             os.exit()
#
#         env_variables = variables['env_variables']
#         for var in env_variables:
#             os.environ[var] = env_variables[var]
#
#     db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
#
#
#     pool = sqlalchemy.create_engine(
#         sqlalchemy.engine.url.URL(
#             drivername="mysql+pymysql",
#             username=os.environ.get('MYSQL_USER'),
#             password=os.environ.get('MYSQL_PASSWORD'),
#             database=os.environ.get('MYSQL_DB'),
#             host=os.environ.get('MYSQL_HOST')
#
#
#         )
#     )
#
#     return pool





def init_connection_engine():
    db_config = {
        # [START cloud_sql_mysql_sqlalchemy_limit]
        # Pool size is the maximum number of permanent connections to keep.
        "pool_size": 5,
        # Temporarily exceeds the set pool_size if no connections are available.
        "max_overflow": 2,
        # The total number of concurrent connections for your application will be
        # a total of pool_size and max_overflow.
        # [END cloud_sql_mysql_sqlalchemy_limit]

        # [START cloud_sql_mysql_sqlalchemy_backoff]
        # SQLAlchemy automatically uses delays between failed connection attempts,
        # but provides no arguments for configuration.
        # [END cloud_sql_mysql_sqlalchemy_backoff]

        # [START cloud_sql_mysql_sqlalchemy_timeout]
        # 'pool_timeout' is the maximum number of seconds to wait when retrieving a
        # new connection from the pool. After the specified amount of time, an
        # exception will be thrown.
        "pool_timeout": 30,  # 30 seconds
        # [END cloud_sql_mysql_sqlalchemy_timeout]

        # [START cloud_sql_mysql_sqlalchemy_lifetime]
        # 'pool_recycle' is the maximum number of seconds a connection can persist.
        # Connections that live longer than the specified amount of time will be
        # reestablished
        "pool_recycle": 1800,  # 30 minutes
        # [END cloud_sql_mysql_sqlalchemy_lifetime]

    }

    return init_unix_connection_engine(db_config)



def init_unix_connection_engine(db_config):
    # [START cloud_sql_mysql_sqlalchemy_create_socket]
    # Remember - storing secrets in plaintext is potentially unsafe. Consider using
    # something like https://cloud.google.com/secret-manager/docs/overview to help keep
    # secrets secret.
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]
    db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
    instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]

    pool = sqlalchemy.create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@/<db_name>?unix_socket=<socket_path>/<cloud_sql_instance_name>
        sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
            username=db_user,  # e.g. "my-database-user"
            password=db_pass,  # e.g. "my-database-password"
            database=db_name,  # e.g. "my-database-name"
            query={
                "unix_socket": "{}/{}".format(
                    db_socket_dir,  # e.g. "/cloudsql"
                    instance_connection_name)  # i.e "<PROJECT-NAME>:<INSTANCE-REGION>:<INSTANCE-NAME>"
            }
        ),
        **db_config
    )
    # [END cloud_sql_mysql_sqlalchemy_create_socket]

    return pool

db = init_connection_engine()





# To prevent from using a blueprint, we use a cyclic import
# This also means that we need to place this import here
# pylint: disable=cyclic-import, wrong-import-position
from app import routes