#!/bin/bash
./venv/Scripts/activate
python app.py
git status
git add .
git commit -m "update file orders.txt"