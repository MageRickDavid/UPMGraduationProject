# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    server.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rortiz <rortiz@student.42madrid.com>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/03/11 21:59:35 by rortiz            #+#    #+#              #
#    Updated: 2026/03/15 01:40:13 by rortiz           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from fastapi import FastAPI
from helper import *
from collector import *
import json
import asyncio
from contextlib import asynccontextmanager


station_ids = load_station_ids()
async def renfe_collector():

    while True:

        try:

            print("Updating RENFE vehicles...")

            feed = fetch_gtfs_feed()

            vehicles = extract_vehicle_data(feed, station_ids)

            print("Vehicles found:", len(vehicles))

            update_vehicle_positions(vehicles)

        except Exception as e:

            print("Collector error:", e)

        await asyncio.sleep(25)

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Starting RENFE collector...")

    task = asyncio.create_task(renfe_collector())

    yield

    task.cancel()


app = FastAPI(lifespan=lifespan)



@app.get("/stations/{name}")
def get_station(name: str):
    stations = find_station(name)
    return {"query": name, "results": stations}

@app.get("/linesFromStation/{name}")
def get_lines_from_station_name(name):
    lines = get_lines(name)
    return {"query": name, "results": lines}

@app.get("/vehicles")
def get_vehicles():

    conn = sqlite3.connect("../databases/cercanias.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM vehicle_positions")

    rows = cursor.fetchall()

    conn.close()

    return rows

