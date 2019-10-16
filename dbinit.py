import os
import sys

import psycopg2 as dbapi2

DATABASE_URL = "postgres://itucs:itucspw@localhost:32768/itucsdb"

INIT_STATEMENTS = [

    #---------------Goktug--------------------
    """CREATE EXTENSION IF NOT EXISTS pgcrypto
    """,
     """CREATE TABLE IF NOT EXISTS USERS (
        USERNAME VARCHAR PRIMARY KEY,
        PASSWORD VARCHAR NOT NULL,
        MEMBER_ID INTEGER REFERENCES MEMBER(ID) ON DELETE SET NULL ON UPDATE CASCADE
    )
    """,
    """CREATE TABLE IF NOT EXISTS SCHEDULE (
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR NOT NULL,
        DEADLINE DATE NOT NULL,
        DONE BOOL NOT NULL,
        DESCRIPTION VARCHAR NOT NULL,
        BUDGET VARCHAR NOT NULL,
        MEMBER_ID INTEGER REFERENCES MEMBER(ID) ON DELETE SET NULL ON UPDATE CASCADE
    )
    """,
    """CREATE TABLE IF NOT EXISTS EQUIPMENT (
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR NOT NULL,
        LINK VARCHAR NOT NULL,
        PURCHASEDATE DATE NOT NULL,
        AVAILABLE BOOL NOT NULL,
        PICTURE VARCHAR NOT NULL,
        TEAM_ID INTEGER REFERENCES TEAM(ID) ON DELETE SET NULL ON UPDATE CASCADE,
        SUBTEAM_ID INTEGER REFERENCES SUBTEAM(ID) ON DELETE SET NULL ON UPDATE CASCADE
    )
    """,
    """CREATE TABLE IF NOT EXISTS TUTORIAL (
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR NOT NULL,
        AREA VARCHAR NOT NULL,
        DESCRIPTION VARCHAR NOT NULL,
        LINK VARCHAR NOT NULL,
        ISVIDEO BOOL NOT NULL,
        MEMBER_ID INTEGER REFERENCES MEMBER(ID) ON DELETE SET NULL ON UPDATE CASCADE
    )
    """
    #---------------Goktug--------------------
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()

'''
if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
'''