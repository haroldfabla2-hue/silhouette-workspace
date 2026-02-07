#!/usr/bin/env python3
# Script regenerado con OAuth refresh automático

import json
import requests
import sys
from pathlib import Path

# Import oauth helper dinámicamente
import importlib.util
oauth_spec = importlib.util.spec_from_file_location("oauth_helper", str(Path(__file__).parent / "google-oauth.py"))
oauth_module = importlib.util.module_from_spec(oauth_spec)
oauth_spec.loader.exec_module(oauth_module)
get_valid_token = oauth_module.get_valid_token

TOKEN_FILE = Path.home() / ".openclaw" / "google-oauth" / "tokens" / "tokens.json"

def get_token():
    token, error = get_valid_token("alberto.farah.b@gmail.com")
    if error:
        raise Exception(f"OAuth Error: {error}")
    return token
