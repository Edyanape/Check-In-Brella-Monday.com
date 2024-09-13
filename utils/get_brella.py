import requests
from dotenv import load_dotenv
import os
import json

class GET_INVITE_LIST():

    def __init__(self):
        load_dotenv()
        self.apikey_brella = os.getenv("APIKEY_BRELLA")
        self.organization_id = os.getenv("ORGANIZATION_ID")
        self.event_id = os.getenv("EVENT_ID")
        self.apikey_monday = os.getenv("APIKEY_MONDAY")
        self.board_id = os.getenv("BOARD_ID")
        self.base_url = os.getenv("BASE_URL")

    def get_information_brella(self):
        try:
            headers = {'Brella-API-Access-Token': self.apikey_brella}
            url = f"{self.base_url}/{self.organization_id}/events/{self.event_id}/invites"
            r_brella = requests.get(url = url, headers = headers)
            r_brella.raise_for_status()
            return r_brella.json()
        except (requests.RequestException, KeyError, ValueError) as e:
            return print(f"Error fetching invites: {e}")