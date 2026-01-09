#!/usr/bin/env python3
"""
TCS Production WSGI Entry Point
Deploy: gunicorn --workers 4 --bind 0.0.0.0:5000 wsgi:app
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import app, df

if __name__ == "__main__":
    app.run()
