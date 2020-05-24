import xml.etree.ElementTree as ET
import requests

def fetch_year(year, fmisid):
    parameters = {
        'service': 'WFS',
        'version': '2.0.0',
        'request': 'getFeature',
        'storedquery_id': 'fmi::observations::weather::daily::simple', 
        'starttime': str(year)+'-01-01T00:00:00Z',
        'endtime': str(year)+'-12-31T00:00:00Z',
        'fmisid': fmisid,
        'parameters': 'tmin',
    }
    response = requests.get('http://opendata.fmi.fi/wfs', params=parameters)
    return ET.fromstring(response.text)