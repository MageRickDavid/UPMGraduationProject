# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    build_database.py                                  :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rortiz <rortiz@student.42madrid.com>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/03/10 08:16:16 by rortiz            #+#    #+#              #
#    Updated: 2026/03/10 08:20:45 by rortiz           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import pandas as pd
import sqlite3

# load csv
df = pd.read_csv("data.csv", sep=",")

# create database
conn = sqlite3.connect("cercanias.db")
cursor = conn.cursor()

# create tables
cursor.execute("""
CREATE TABLE stations (
    station_id INTEGER PRIMARY KEY,
    name TEXT,
    latitude REAL,
    longitude REAL
)
""")

cursor.execute("""
CREATE TABLE station_lines (
    station_id INTEGER,
    line_id TEXT
)
""")

# insert data
for _, row in df.iterrows():

    # insert station
    cursor.execute(
        "INSERT INTO stations VALUES (?, ?, ?, ?)",
        (row["CODIGO"], row["DESCRIPCION"], row["LATITUD"], row["LONGITUD"])
    )

    # split lines
    lines = row["LINES"].split("-")

    # insert lines
    for line in lines:
        cursor.execute(
            "INSERT INTO station_lines VALUES (?, ?)",
            (row["CODIGO"], line)
        )

conn.commit()
conn.close()

print("Database created: cercanias.db")