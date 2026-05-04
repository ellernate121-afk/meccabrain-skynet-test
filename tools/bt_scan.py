# tools/bt_scan.py
# Requires: pip install bleak requests
import asyncio
from bleak import BleakScanner
import requests
import os

DASHBOARD_URL = os.getenv('DASHBOARD_URL', 'http://localhost:3000/log')

async def scan_once(timeout=8):
    devices = await BleakScanner.discover(timeout=timeout)
    results = []
    for d in devices:
        info = {"address": d.address, "name": d.name, "rssi": d.rssi}
        results.append(info)
        try:
            requests.post(DASHBOARD_URL, json={"type":"ble-scan", "msg": f"Found {d.address} ({d.name})", "data": info}, timeout=2)
        except Exception:
            pass
    return results

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    devices = loop.run_until_complete(scan_once())
    print("Found devices:", devices)
