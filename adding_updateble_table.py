# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    adding_updateble_table.py                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rortiz <rortiz@student.42madrid.com>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/03/15 00:44:51 by rortiz            #+#    #+#              #
#    Updated: 2026/03/15 03:21:31 by rortiz           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sqlite3

conn = sqlite3.connect("databases/cercanias.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS vehicle_positions (

    vehicle_id TEXT PRIMARY KEY,
    trip_id TEXT,
    stop_id TEXT,
    latitude REAL,
    longitude REAL,
    status TEXT,
    timestamp TEXT,
    label TEXT,
    line TEXT
)
""")

conn.commit()
conn.close()