#!/bin/bash
uvicorn bot:app --host 0.0.0.0 --port 10000 &
python bot.py
