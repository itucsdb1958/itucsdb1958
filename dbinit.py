import os
import sys

import psycopg2 as dbapi2

INIT_STATEMENTS = [

    """CREATE EXTENSION IF NOT EXISTS pgcrypto
    """,
    """CREATE TABLE IF NOT EXISTS COMPETITION (
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR NOT NULL,
        DATE DATE NOT NULL,
        COUNTRY VARCHAR NOT NULL,
        DESCRIPTION VARCHAR NOT NULL,
        REWARD VARCHAR NOT NULL,
        URL VARCHAR,
        LOGO VARCHAR,
        TEAM_ID INTEGER NOT NULL
    )
    """,
    """CREATE TABLE IF NOT EXISTS TEAM(
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR NOT NULL,
        NUM_MEMBERS INTEGER NOT NULL,
        FOUND_YEAR VARCHAR NOT NULL,
        EMAIL VARCHAR NOT NULL,
        ADRESS VARCHAR NOT NULL,
        LOGO VARCHAR NOT NULL,
        COMPETITION_ID INTEGER REFERENCES COMPETITION(ID) ON DELETE SET NULL ON UPDATE CASCADE
    )
    """,
    """CREATE TABLE IF NOT EXISTS SUBTEAM(
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR NOT NULL,
        TEAM_ID INTEGER REFERENCES TEAM(ID) ON DELETE SET NULL ON UPDATE CASCADE
    )
    """,
    """CREATE TABLE IF NOT EXISTS STATUS (
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR NOT NULL
    )
    """,
    """CREATE TABLE IF NOT EXISTS MAJOR (
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR NOT NULL
    )
    """,
    """CREATE TABLE IF NOT EXISTS AUTH_TYPE(
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR NOT NULL
    )
    """,
    """CREATE TABLE IF NOT EXISTS PERSON(
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR NOT NULL,
        AGE INTEGER NOT NULL,
        PHONE VARCHAR NOT NULL,
        CV VARCHAR NOT NULL,
        EMAIL VARCHAR NOT NULL,
        CLASS INTEGER NOT NULL,
        AUTH_TYPE INTEGER NOT NULL,
        STATUS INTEGER NOT NULL,
        TEAM_ID INTEGER REFERENCES TEAM(ID) ON DELETE SET NULL ON UPDATE CASCADE,
        SUBTEAM_ID INTEGER REFERENCES SUBTEAM(ID) ON DELETE SET NULL ON UPDATE CASCADE,
        MAJOR_ID INTEGER REFERENCES MAJOR(ID) ON DELETE SET NULL ON UPDATE CASCADE
    )
    """,
    """CREATE TABLE IF NOT EXISTS VEHICLE_TYPE(
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR NOT NULL
    )
    """,
    """CREATE TABLE IF NOT EXISTS MEMBER (
        ID SERIAL PRIMARY KEY,
        ROLE VARCHAR NOT NULL,
        ENTRYDATE DATE NOT NULL,
        ACTIVE BOOL NOT NULL,
        PICTURE VARCHAR NOT NULL,
        ADDRESS VARCHAR NOT NULL,
        PERSON_ID INTEGER REFERENCES PERSON(ID) ON DELETE SET NULL ON UPDATE CASCADE
    )
    """,

    """CREATE TABLE IF NOT EXISTS SPONSORTYPE (
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR NOT NULL
    )
    """,
    """CREATE TABLE IF NOT EXISTS SPONSOR (
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR NOT NULL,
        DESCRIPTION VARCHAR NOT NULL,
        FIELD VARCHAR NOT NULL,
        COUNTRY VARCHAR NOT NULL,
        LOGO VARCHAR NOT NULL,
        ADDRESS VARCHAR NOT NULL,
        TYPE_ID INTEGER REFERENCES SPONSORTYPE(ID) ON DELETE SET NULL ON UPDATE CASCADE
    )
    """,
    """CREATE TABLE IF NOT EXISTS SPONSORINDEX(
        ID SERIAL PRIMARY KEY,
        SPONSOR_ID INTEGER REFERENCES SPONSOR(ID) ON DELETE SET NULL ON UPDATE CASCADE,
        TEAM_ID INTEGER REFERENCES TEAM(ID) ON DELETE SET NULL ON UPDATE CASCADE
    )
    """,
    """CREATE TABLE IF NOT EXISTS DESIGN(
        ID SERIAL PRIMARY KEY,
        NAME VARCHAR NOT NULL,
        YEAR VARCHAR NOT NULL,
        MAXSPEED VARCHAR NOT NULL,
        WEIGHT VARCHAR NOT NULL,
        DURATION VARCHAR NOT NULL,
        IS_AUTONOMOUS BOOL NOT NULL,
        TEAM_ID INTEGER REFERENCES TEAM(ID) ON DELETE SET NULL ON UPDATE CASCADE,
        TYPE_OF_VEHICLE INTEGER REFERENCES VEHICLE_TYPE(ID) ON DELETE SET NULL ON UPDATE CASCADE
    )
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
        PICTURE VARCHAR NOT NULL,
        ISVIDEO BOOL NOT NULL,
        MEMBER_ID INTEGER REFERENCES MEMBER(ID) ON DELETE SET NULL ON UPDATE CASCADE
    )
    """,
    """CREATE TABLE IF NOT EXISTS ADMIN (
        ID SERIAL PRIMARY KEY,
        USERNAME VARCHAR,
        PASSWORD VARCHAR
    )
    """
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py")  # , file=sys.stderr)
        sys.exit(1)
    initialize(url)
