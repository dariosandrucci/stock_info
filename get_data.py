# --------------------------------------------------------------------------- #
#                                  Imports                                    #
# --------------------------------------------------------------------------- #

# ----------------------- Built-in/Generic Imports -------------------------- #

import sqlalchemy
import mysql.connector as connector
import os
import pymysql
import pandas as pd
import sys
import yfinance as yf
import scipy.optimize as sco
import scipy.interpolate as sci
import numpy as np
import plotly.express as px

# --------------------------- DB Connection --------------------------------- #


def connect(
        user: str = "reader",
        password: str = "reader",
        host: str = "pmcbackpack.mysql.database.azure.com",
        port: int = 3306,
        database: str = "pmcbackpack",
        ssl_ca: str = os.path.join(sys.path[0], "DigiCertGlobalRootCA.crt.pem"),
        ssl_verify_cert: bool = True,
        buffered: bool = True,
) -> bool:
    "Establishes MYSQL Connection"
    global DB
    DB = connector.connect(
        user=user,
        password=password,
        host=host,
        port=port,
        database=database,
        ssl_ca=ssl_ca,
        ssl_verify_cert=ssl_verify_cert,
        buffered=buffered,
        use_pure=True,
    )

    global MYCURSOR
    MYCURSOR = DB.cursor()
    return DB.is_connected()


# SQLAlchemy Engine
def sqlalchemy_engine(
        user: str = "reader",
        pw: str = "reader",
        host: str = "pmcbackpack.mysql.database.azure.com",
        DB: str = "pmcbackpack",
) -> sqlalchemy.engine.base.Connection:
    global ENGINE
    ENGINE = sqlalchemy.create_engine(
        f"mysql+pymysql://{user}:{pw}@{host}/{DB}",
        connect_args={
            "ssl": {
                "ssl_ca": str(os.path.join(sys.path[0], "DigiCertGlobalRootCA.crt.pem")),
            }
        },
    )
    return ENGINE.connect()


connect()
sqlalchemy_engine()


def get_portfolio_data(db=DB, engine=ENGINE):
    db.reconnect()
    engine.connect()

    portfolio = pd.read_sql_table("portfolio", con=engine)
    df = pd.DataFrame(portfolio)

    # only for better visualization and understanding of the df

    html = df.to_html()
    # write html to file
    text_file = open("index.html", "w")
    text_file.write(html)
    text_file.close()

    return df

