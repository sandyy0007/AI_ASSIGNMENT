#!/bin/bash

# AI App Config Compiler - Unix startup script

echo "========================================"
echo "AI App Config Compiler"
echo "========================================"
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Error: Node.js not found. Please install Node.js."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 not found. Please install Python 3.8+"
    exit 1
fi

echo "Starting AI App Config Compiler..."
echo ""

# Start backend
echo "[1/2] Starting backend server..."
cd backend
python3 app.py &
BACKEND_PID=$!
cd ..
sleep 3

# Start frontend
echo "[2/2] Starting frontend server..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi
npm run dev
cd ..

# Cleanup on exit
trap "kill $BACKEND_PID" EXIT

echo ""
echo "========================================"
echo "Frontend: http://localhost:5173"
echo "Backend:  http://localhost:8000"
echo "========================================"
