import fiona
import requests
from datetime import datetime, timezone
from geojson import Feature, FeatureCollection


def get_active_fires():
    """
    Get GeoMAC data
    """
    url = 'https://rmgsc.cr.usgs.gov/outgoing/GeoMAC/current_year_fire_data/current_year_all_states/active_perimeters_dd83.zip'
    with fiona.open(f'zip+{url}') as f:
        return FeatureCollection([Feature(geometry=d['geometry'], properties=d['properties']) for d in f])

def get_all_fires():
    """
    Get GeoMAC data for all fires
    """
    url = 'https://rmgsc.cr.usgs.gov/outgoing/GeoMAC/current_year_fire_data/current_year_all_states/perimeters_dd83.zip'

    r = requests.head(url)
    url_time = r.headers['last-modified']
    local_dt = datetime.strptime(url_time.split(', ')[1], '%d %b %Y %H:%M:%S GMT')

    def utc_to_local(utc_dt):
        return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)

    with fiona.open(f'zip+{url}') as f:
        collection = FeatureCollection([Feature(geometry=d['geometry'], properties=d['properties'], precision=4) for d in f])
        collection['metadata'] = {
            'last_updated_datetime': str(utc_to_local(local_dt)),
            'last_updated_date': str(utc_to_local(local_dt)).split(' ')[0]
        }
        return collection

def get_nifc_sitrep():
    """
    Get NIFC Sit Rep data
    """
    url = 'https://rmgsc.cr.usgs.gov/outgoing/GeoMAC/current_year_fire_data/current_year_all_states/nifc_sit_rep_dd83.zip'
    with fiona.open(f'zip+{url}') as f:
        return FeatureCollection([Feature(geometry=d['geometry'], properties=d['properties']) for d in f])
