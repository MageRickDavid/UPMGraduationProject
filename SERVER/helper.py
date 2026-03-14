# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    helper.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rortiz <rortiz@student.42madrid.com>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/03/11 22:59:51 by rortiz            #+#    #+#              #
#    Updated: 2026/03/15 00:23:13 by rortiz           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sqlite3
from collector import *
import asyncio
import json


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


