REST_API_BASE_URL = 'https://rest.envirosolutions.pl/integrator'
REST_ENDPOINT_COUNTRY = '/get-country-urls'
REST_SERVICES_ENDPOINT = '/get-services-urls'
RESULT_SERVICE_TAG = 'Service'

# REST API endpoints (nowe API)
REST_DZIALKI_API_BASE_URL = "https://rest.envirosolutions.pl/dzialki"
REST_ENDPOINT_VOIVODESHIP = "/getVoivodeship"
REST_ENDPOINT_COUNTY = "/getCounty"
REST_ENDPOINT_COMMUNE = "/getCommune"
# REST_ENDPOINT_PRECINCT = "/getPrecinct"

FEED_URL = 'https://qgisfeed.envirosolutions.pl/'

INDUSTRIES = {
    "999": 'Nie wybrano',
    "e": 'Energetyka/OZE',
    "u": 'Urząd',
    "td": 'Transport/Drogi',
    "pg": 'Planowanie/Geodezja',
    "wk": 'WodKan',
    "s": 'Środowisko',
    "rl": 'Rolnictwo/Leśnictwo',
    "tk": 'Telkom',
    "edu": 'Edukacja',
    "i": 'Inne',
    "it": 'IT',
    "n": 'Nieruchomości'
}

ENCODING_SYSTEM = "utf-8"

RADIOBUTTONS_SERVICES = [
    'wms_rdbtn',
    'wmts_rdbtn',
    'wcs_rdbtn',
    'wfs_rdbtn',
]

SERVICES_NAMESPACES = {
    'WCS': {
        'wcs': 'http://www.opengis.net/wcs/2.0',
        'ows': 'http://www.opengis.net/ows/2.0'
    },
    'WFS': {
        'wfs': 'http://www.opengis.net/wfs/2.0',
        'ows': 'http://www.opengis.net/ows/1.1'
    },
    'WMS': {
        'wms': 'http://www.opengis.net/wms'
    },
    'WMTS': {
        'wmts': 'http://www.opengis.net/wmts/1.0',
        'ows': 'http://www.opengis.net/ows/1.1'
    },
}
