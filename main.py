import requests
import pandas as pd
import io
import os

os.makedirs('data', exist_ok=True)

API_REQUEST="https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"

PARAMETERS = {
    "begin_date":"20260619",
    "end_date":"20260720",
    "product":"water_temperature",
    "time_zone":"lst_ldt",
    "units":"metric",
    "format":"csv"
}

stations = pd.read_csv("stations.csv")

stations_ids = stations['id'].to_list()
station_names = stations['name'].to_list()

def filename_constructor(parameters:dict, station_name) -> str:
    start = parameters['begin_date']
    end = parameters['end_date']
    return f"data/water_temperature-{station_name}-{start}-{end}.csv"


def main():
    columns_order = ['StationID','StationName','Date_Time','Water_Temperature','X','N','R']
    for id, name in zip(stations_ids, station_names):
        PARAMETERS['station'] = id
        r = requests.get(API_REQUEST, PARAMETERS)
        filename = filename_constructor(PARAMETERS, name)
        if os.path.exists(filename):
            uinput = input(f"{filename} already exists. Do you want to overwrite the results? y/n: ")
            if uinput.lower() != "y":
                continue
        if r.status_code == 200:
            response = r.text
            if len([line for line in response.splitlines() if line.strip()]) < 3:
                print(response.splitlines()[1].replace("this station", name) + " " + PARAMETERS['begin_date'] + "-" + PARAMETERS['end_date'])
                print("Skipping")
                continue
            df = pd.read_csv(io.StringIO(r.text))
            df = df.rename(columns=lambda x: x.strip().replace(" ", "_"))
            df['StationID'] = id
            df['StationName'] = name
            df = df[columns_order]
            df.to_csv(filename, index=False)


if __name__ == "__main__":
    main()
