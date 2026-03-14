# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    collector.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rortiz <rortiz@student.42madrid.com>       +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/03/15 00:17:17 by rortiz            #+#    #+#              #
#    Updated: 2026/03/15 01:55:14 by rortiz           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import requests
import sqlite3
from datetime import datetime
from google.transit import gtfs_realtime_pb2

GTFS_URL = "https://gtfsrt.renfe.com/vehicle_positions.pb"
TIMEOUT = 30


def load_station_ids():

    conn = sqlite3.connect("../databases/cercanias.db")
    cursor = conn.cursor()

    cursor.execute("SELECT station_id FROM stations")

    station_ids = {str(row[0]) for row in cursor.fetchall()}

    conn.close()

    return station_ids


def fetch_gtfs_feed():

    response = requests.get(GTFS_URL, timeout=TIMEOUT)

    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)

    return feed


def extract_vehicle_data(feed, station_ids):

    vehicles = []

    for entity in feed.entity:

        if entity.HasField("vehicle"):

            v = entity.vehicle

            if str(v.stop_id) not in station_ids:
                continue
            status_name = gtfs_realtime_pb2.VehiclePosition.VehicleStopStatus.Name(
                v.current_status)
            vehicle_data = {
                "label" : v.vehicle.label if v.vehicle.label else None,
                "vehicle_id": v.vehicle.id if v.vehicle.id else None,
                "trip_id": v.trip.trip_id if v.trip else None,
                "stop_id": v.stop_id if v.stop_id else None,
                "latitude": v.position.latitude if v.position else None,
                "longitude": v.position.longitude if v.position else None,
                "status": status_name,
                "timestamp": datetime.fromtimestamp(v.timestamp).isoformat() if v.timestamp else None
            }

            vehicles.append(vehicle_data)

    return vehicles

import sqlite3

def update_vehicle_positions(vehicles):

    conn = sqlite3.connect("../databases/cercanias.db")
    cursor = conn.cursor()

    # clear previous snapshot
    cursor.execute("DELETE FROM vehicle_positions")

    # insert new snapshot
    for v in vehicles:
        cursor.execute("""
            INSERT INTO vehicle_positions
            (vehicle_id, trip_id, stop_id, latitude, longitude, status, timestamp, label)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            v["vehicle_id"],
            v["trip_id"],
            v["stop_id"],
            v["latitude"],
            v["longitude"],
            v["status"],
            v["timestamp"],
            v["label"]
        ))

    conn.commit()
    conn.close()