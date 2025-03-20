#!/bin/bash

echo "Starting Focus Peaking Application..."

# Start Backend
cd backend
source venv/bin/activate
python focus_peaking.py &

# Start Frontend
cd ../frontend
npm run dev
