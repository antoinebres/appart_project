import pandas as pd
import datetime
import requests
import unidecode

STOP_COORDS = pd.read_csv('../../stops_coords.csv')

def get_coords_stop_by_name(name):
    name = unidecode.unidecode(name)
    stop_coords = STOP_COORDS[STOP_COORDS.stop_name.str.contains(name, case=False)]
    if stop_coords.empty:
        raise ValueError('Cannot find any stop with the following name "%s"' % name)
    stop_coords = stop_coords.groupby('stop_name').mean()
    if stop_coords.shape[0] != 1:
        if stop_coords.stop_lat.std() < 3e-02 and stop_coords.stop_lon.std() < 3e-02: 
            # Les entrees sont au plus distantes de ~30m
            return (stop_coords.stop_lat.mean(), stop_coords.stop_lon.mean())
        raise ValueError('There is more than one stop containing the following name "%s"' % name, stop_coords)

def estimate_travel_time_form_coords(start_coord, end_coords=(48.8687306,2.3312111)):
    citymapper_API_key = 'aaae1d79bbb63d27921a4dfa21dcb34d'
    simulated_datetime = next_weekday().replace(hour=10, minute=30)

    citymapper_url = "https://developer.citymapper.com/api/1/traveltime/?startcoord={}%2C{}&endcoord={}%2C{}&time={}T{}%3A{}%3A{}-0500&time_type=arrival&key={}".format(
        start_coord[0], start_coord[1], end_coords[0], end_coords[1], simulated_datetime.date(), simulated_datetime.hour, simulated_datetime.minute, simulated_datetime.second, citymapper_API_key
        )
    response = requests.get(citymapper_url)

    temps_de_trajet_jusqu_au_34 = response.json()
    if temps_de_trajet_jusqu_au_34:
        return temps_de_trajet_jusqu_au_34['travel_time_minutes']

def next_weekday():
    today = datetime.datetime.now()
    if today.weekday() is 5:
        return today + datetime.timedelta(days=2)
    if today.weekday() is 6:
        return today + datetime.timedelta(days=1)
    return today

def get_travel_time_from(station_de_depart):
    try:
        start_coord = get_coords_stop_by_name(station_de_depart)
        if start_coord:
            return estimate_travel_time_form_coords(start_coord)
        print('Warning: ', station_de_depart)
        return 500
    except Exception as e:
        raise e
