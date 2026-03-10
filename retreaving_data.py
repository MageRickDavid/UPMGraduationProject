# imports
import requests
from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict
from datetime import datetime
import json
import pprint
import sqlite3

GTFS_URL = "https://gtfsrt.renfe.com/vehicle_positions.pb"
TIMEOUT = 30


# -----------------------------
# FUNCTIONS
# -----------------------------
def load_station_ids():

    conn = sqlite3.connect("cercanias.db")
    cursor = conn.cursor()

    cursor.execute("SELECT station_id FROM stations")

    station_ids = {str(row[0]) for row in cursor.fetchall()}

    conn.close()

    return station_ids

def fetch_gtfs_feed():
    try:
        response = requests.get(GTFS_URL, timeout=TIMEOUT)
        response.raise_for_status()

        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)
        return feed

    except Exception as e:
        print(f"[ERROR] {e}")
        return None


def extract_vehicle_data(feed, station_ids):
    vehicles = []

    if not feed:
        return vehicles

    for entity in feed.entity:
        if entity.HasField("vehicle"):
            v = entity.vehicle
            if str(v.stop_id) not in station_ids:
                continue
            status_name = gtfs_realtime_pb2.VehiclePosition.VehicleStopStatus.Name(
                v.current_status)
            vehicle_data = {
                "label" : v.vehicle.label if v.vehicle.label else None,
                "Status" : status_name,
                "Stop_id" : v.stop_id if v.stop_id else None,
                "vehicle_id": v.vehicle.id if v.vehicle.id else None,
                "latitude": v.position.latitude if v.position else None,
                "longitude": v.position.longitude if v.position else None,
                "trip_id": v.trip.trip_id if v.trip else None,
                "timestamp": datetime.fromtimestamp(
                    v.timestamp) if v.timestamp else None
            }

            vehicles.append(vehicle_data)

    return vehicles


# -----------------------------
# MAIN EXECUTION
# -----------------------------

if __name__ == "__main__":
    station_ids = load_station_ids()

    print("Fetching RENFE GTFS-Realtime feed...\n")

    feed = fetch_gtfs_feed()

    if not feed:
        print("Failed to retrieve feed.")
        exit()

    print("Feed timestamp:",
          datetime.fromtimestamp(feed.header.timestamp))
    print("-" * 50)

    vehicles = extract_vehicle_data(feed, station_ids)

    print(f"Total active vehicles: {len(vehicles)}\n")

    pp = pprint.PrettyPrinter(indent=2)
    for v in vehicles:
        pp.pprint(v)

    with open("renfe_vehicles_snapshot.json", "w") as f:
        json.dump(vehicles, f, default=str, indent=2)

    feed_dict = MessageToDict(feed)

    with open("renfe_full_feed.json", "w") as f:
        json.dump(feed_dict, f, indent=2)

    print("\nData saved successfully.")