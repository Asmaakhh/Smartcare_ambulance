# app/ambulance/__init__.py
import sys
import os

# Add project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ambulance.ambulances_service import *
from ambulance.ambulance_model import *
