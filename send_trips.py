import pandas as pd
import requests

# API:n osoite, johon POST-pyynnöt lähetetään
API_URL = "http://127.0.0.1:8000/trips"

# Luetaan CSV-tiedosto
df = pd.read_csv("yellow_tripdata_2023-07.csv")

# Käydään tiedoston läpi ja tallennetaan data
for index, row in df.head(10).iterrows():
    try:
        # Tarkistetaan, että kaikki tarvittavat kentät ovat kelvollisia (ei NaN)
        if pd.isna(row["tpep_pickup_datetime"]) or pd.isna(row["tpep_dropoff_datetime"]):
            continue
        if pd.isna(row["passenger_count"]) or pd.isna(row["trip_distance"]) or pd.isna(row["total_amount"]):
            continue

        # Muodostetaan JSON-dict muodossa, jonka API hyväksyy
        trip_data = {
            "start_time": pd.to_datetime(row["tpep_pickup_datetime"]).isoformat(),
            "end_time": pd.to_datetime(row["tpep_dropoff_datetime"]).isoformat(),
            "passenger_count": int(row["passenger_count"]),
            "distance_km": float(row["trip_distance"]),
            "total_price": float(row["total_amount"])
        }

        # Lähetetään POST-pyyntö API:lle
        response = requests.post(API_URL, json=trip_data)
        response.raise_for_status()
        returned = response.json()

        # Tulostetaan lähetetyt tiedot ja palautettu ID
        print(f"[{index}] Lähetetty!")

    except Exception as e:
        print(f"[{index}] Virhe rivillä {index}: {e}")