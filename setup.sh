#!/bin/bash

echo "=========================================="
echo " Creating virtual environment..."
echo "=========================================="

python3 -m venv venv

echo "=========================================="
echo " Activating virtual environment..."
echo "=========================================="

source venv/bin/activate

echo "=========================================="
echo " Upgrading pip..."
echo "=========================================="

pip install --upgrade pip

echo "=========================================="
echo " Installing dependencies..."
echo "=========================================="

pip install scapy colorama mac-vendor-lookup

echo "=========================================="
echo " Verifying installation..."
echo "=========================================="

python -c "from mac_vendor_lookup import MacLookup; print('mac_vendor_lookup installed successfully')"

echo "=========================================="
echo " Running scanner.py..."
echo "=========================================="

sudo venv/bin/python scanner.py