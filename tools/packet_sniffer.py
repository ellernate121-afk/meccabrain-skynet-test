# tools/packet_sniffer.py
# This is a placeholder to collect logs from external sniffers (rtl_433, hackrf, etc.)
# It accepts JSON lines on stdin and forwards them to the dashboard.
import sys, json, requests, os
DASHBOARD_URL = os.getenv('DASHBOARD_URL', 'http://localhost:3000/log')

def forward(line):
    try:
        obj = json.loads(line)
    except:
        obj = {"raw": line}
    try:
        requests.post(DASHBOARD_URL, json={"type":"sniffer", "msg":"packet", "data": obj}, timeout=2)
    except:
        pass

if __name__ == "__main__":
    for l in sys.stdin:
        forward(l.strip())
