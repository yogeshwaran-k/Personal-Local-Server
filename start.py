import subprocess
import time
import os
import qrcode
from pyngrok import ngrok
from PIL import Image

# Config
FLASK_APP = "server.py"  # <- change to your actual Flask filename
FLASK_PORT = 5000

# Step 1: Start Flask server
print("🚀 Launching Flask server...")
flask_process = subprocess.Popen(["python", FLASK_APP])

# Give Flask a moment to start
time.sleep(3)

# Step 2: Open ngrok tunnel
print("🌐 Opening ngrok tunnel...")
public_url = ngrok.connect(FLASK_PORT, "http").public_url
print(f"🔗 Ngrok URL: {public_url}")

# Step 3: Generate QR Code
print("📱 Creating QR code...")
qr = qrcode.make(public_url)
qr_file = "ngrok_qr.png"
qr.save(qr_file)
Image.open(qr_file).show()

# Step 4: Keep it alive
try:
    print("\n✅ Scan the QR or open this link on your mobile:\n", public_url)
    print("\nPress Ctrl+C to stop the server and ngrok tunnel.")
    flask_process.wait()
except KeyboardInterrupt:
    print("\n🛑 Stopping server and tunnel...")
    flask_process.terminate()
    ngrok.kill()
