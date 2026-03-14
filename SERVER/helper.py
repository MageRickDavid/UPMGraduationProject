# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    helper.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rortiz <rortiz@student.42madrid.com>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/03/11 22:59:51 by rortiz            #+#    #+#              #
#    Updated: 2026/03/15 04:37:37 by rortiz           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sqlite3
from collector import *
import asyncio
import json
import math


columns = "name, station_id"
def find_station(station_name):
    conn = sqlite3.connect("../databases/cercanias.db")
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT {columns} FROM stations WHERE LOWER(name) LIKE (?)", (f"%{station_name}%",))
    results = cursor.fetchall()
    conn.close()
    return results

def get_lines(station_name):
    station_id = find_station(station_name)
    station_id = station_id[0][1]
    conn = sqlite3.connect("../databases/cercanias.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT line_id FROM station_lines WHERE station_id LIKE (?)", (f"%{station_id}%",)
    )
    results = cursor.fetchall()
    conn.close()
    return results

def haversine(lat1, lon1, lat2, lon2):

    R = 6371000  # Earth radius in meters

    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    dlat = lat2 - lat1
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    distance = R * c

    return distance