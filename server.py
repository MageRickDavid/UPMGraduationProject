# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    server.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rortiz <rortiz@student.42madrid.com>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/03/11 21:59:35 by rortiz            #+#    #+#              #
#    Updated: 2026/03/11 22:39:37 by rortiz           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from fastapi import FastAPI
import sqlite3

app = FastAPI()

def find_station(station_name):
    conn = sqlite3.connect("cercanias.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name, station_id FROM stations WHERE LOWER(name) LIKE (?)", (f"%{station_name}%",))
    results = cursor.fetchall()
    conn.close()
    return results

@app.get("/stations/{name}")
def get_station(name: str):
    stations = find_station(name)
    return {"query": name, "results": stations}