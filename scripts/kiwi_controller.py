"""Shared Kiwi TCMS client setup."""

import os
import ssl

import tcms_api

KIWI_URL = "https://172.18.246.37:30666/xml-rpc/"
KIWI_USERNAME = "penny6_lee"
KIWI_PASSWORD = "pega#1234"


def get_kiwi_ctr():
    """Write ~/.tcms.conf and return an authenticated XML-RPC client."""
    config = f"""[tcms]
url = {KIWI_URL}
username = {KIWI_USERNAME}
password = {KIWI_PASSWORD}
"""
    config_path = os.path.expanduser("~/.tcms.conf")
    with open(config_path, "w") as f:
        f.write(config)

    try:
        ssl._create_default_https_context = ssl._create_unverified_context
    except AttributeError:
        pass

    return tcms_api.TCMS().exec
