import json

from ..constants import (
    REST_DZIALKI_API_BASE_URL,
    REST_ENDPOINT_VOIVODESHIP,
    REST_ENDPOINT_COUNTY,
    REST_ENDPOINT_COMMUNE,
    # REST_ENDPOINT_PRECINCT
)
from ..utils import MessageUtils, NetworkManager


class RegionFetch:
    def __init__(self):
        self.manager = NetworkManager()

    def fetchUnitDict(self, endpoint):
        unit_dict = {}
        url = f"{REST_DZIALKI_API_BASE_URL}{endpoint}"
        try:
            MessageUtils.logInfo(f"Pobieranie danych z: {url}")
            raw = self.manager.getRequest(url)
            if raw is None:
                MessageUtils.logWarning(
                    f"Błąd sieci przy pobieraniu: {url}"
                )
                return unit_dict
            data = json.loads(raw)
            for item in data:
                unit_dict[item['teryt']] = item['name']
        except Exception as e:
            MessageUtils.logWarning(
                f"Wyjątek przy pobieraniu {url}: {str(e)}"
            )
        return unit_dict

    def getVoivodeships(self):
        return self.fetchUnitDict(REST_ENDPOINT_VOIVODESHIP)

    def getCountiesByTeryt(self, teryt):
        if not teryt:
            return {}
        return self.fetchUnitDict(f"{REST_ENDPOINT_COUNTY}/{teryt}")

    def getCommunesByTeryt(self, teryt):
        if not teryt:
            return {}
        return self.fetchUnitDict(f"{REST_ENDPOINT_COMMUNE}/{teryt}")

    #def getPrecintsByTeryt(self, teryt):
    #    if not teryt:
    #        return {}
    #    return self.fetchUnitDict(f"{REST_ENDPOINT_PRECINCT}/{teryt}")

