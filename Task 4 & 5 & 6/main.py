import network
import socket
import ujson as json
import time
import _thread
import gc
import urequests
import ntptime
from machine import Pin
import asyncio

from hcsr04 import HCSR04
from servo import Servo

SSID = "Not4Public"
PASSWORD = "password"

BOT_TOKEN = ""
CHAT_ID = ""

PIN_TRIGGER = 12
PIN_ECHO = 14
PIN_SERVO = 15
PIN_SOLENOID = 5
PIN_BUZZER = 25
PIN_BUTTON = 26
PIN_LED_RED = 27
PIN_LED_GREEN = 33

POS_KUNCI = 190
POS_BUKA = 125

sensor = HCSR04(trigger_pin=PIN_TRIGGER, echo_pin=PIN_ECHO)
servo = Servo(pin_number=PIN_SERVO)
solenoid = Pin(PIN_SOLENOID, Pin.OUT)
buzzer = Pin(PIN_BUZZER, Pin.OUT)
button = Pin(PIN_BUTTON, Pin.IN, Pin.PULL_UP)
led_merah = Pin(PIN_LED_RED, Pin.OUT)
led_hijau = Pin(PIN_LED_GREEN, Pin.OUT)

sistem_terkunci = True
sensor_distance = -1.0
event_log = []

# -------------------------- NTP TIME SYNC --------------------------

def sync_ntp_time():
    max_attempt = 5
    for attempt in range(max_attempt):
        try:
            ntptime.host = "pool.ntp.org"
            ntptime.settime()
            print("Waktu berhasil disinkronkan (UTC).")
            return
        except Exception as e:
            print(f"Gagal sinkron waktu NTP (percobaan {attempt+1}):", e)
            time.sleep(2)
    print("Sinkronisasi waktu gagal total.")

def waktu_wib():
    try:
        t = time.localtime(time.time() + 7 * 3600)  # UTC+7
        return "{:02d}:{:02d}:{:02d}".format(t[3], t[4], t[5])
    except:
        return "HH:MM:SS"

# -------------------------- LOGGING --------------------------

def log_event(pesan):
    global event_log
    timestamp = waktu_wib()
    log = f"{timestamp} - {pesan}"
    event_log.insert(0, log)
    if len(event_log) > 10:
        event_log.pop()
    print(log)

def send_telegram_message(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}"
        res = urequests.get(url)
        res.close()
    except Exception as e:
        print("Error kirim Telegram:", e)

# -------------------------- FUNGSI AKSI --------------------------

async def beep(ms=50):
    buzzer.on()
    await asyncio.sleep_ms(ms)
    buzzer.off()

async def kunci_sistem():
    global sistem_terkunci
    if not sistem_terkunci:
        await asyncio.sleep_ms(1000)
        servo.move_to_angle(POS_KUNCI)
        await asyncio.sleep_ms(300)
        solenoid.off()
        led_hijau.off()
        led_merah.on()
        await beep(150)
        sistem_terkunci = True
        log_event("Sistem dikunci")

async def buka_sistem(sumber="Tidak Diketahui"):
    global sistem_terkunci
    if sistem_terkunci:
        solenoid.on()
        await asyncio.sleep_ms(1000)
        servo.move_to_angle(POS_BUKA)
        led_merah.off()
        led_hijau.on()
        await beep(50)
        await asyncio.sleep_ms(50)
        await beep(50)
        sistem_terkunci = False
        log_event(f"Dibuka via {sumber}")

# -------------------------- MONITOR --------------------------

async def monitor_sensor():
    global sensor_distance
    objek_terdeteksi_start = None
    notifikasi_terkirim = False

    while True:
        try:
            distance = sensor.distance_cm()
            sensor_distance = distance

            if 5 <= distance <= 15:
                if objek_terdeteksi_start is None:
                    objek_terdeteksi_start = time.time()
                elif time.time() - objek_terdeteksi_start >= 3 and not notifikasi_terkirim:
                    pesan = f"Ada orang di depan pintu pada {waktu_wib()}, http://192.168.74.181/"
                    send_telegram_message(pesan)
                    log_event("Notifikasi objek dalam 5–15cm dikirim")
                    notifikasi_terkirim = True
            else:
                objek_terdeteksi_start = None
                notifikasi_terkirim = False

        except:
            sensor_distance = -1.0

        await asyncio.sleep(0.5)

async def monitor_tombol():
    global sistem_terkunci
    while True:
        if button.value() == 0:
            if sistem_terkunci:
                log_event("Tombol ditekan - membuka pintu")
                send_telegram_message("Ada orang keluar pada " + waktu_wib())
                await buka_sistem("Tombol")
                await asyncio.sleep(5)
                await kunci_sistem()
            else:
                log_event("Tombol ditekan - menutup pintu (manual)")
                send_telegram_message("Pintu ditutup manual pada " + waktu_wib())
                await kunci_sistem()
        await asyncio.sleep_ms(100)

async def ntp_loop():
    while True:
        sync_ntp_time()
        await asyncio.sleep(3600)  # Setiap 1 jam

# -------------------------- WEB HTML UI --------------------------

def generate_html_page():
    return f"""<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Smart Lockbox</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    html, body {{ height: 100%; background: #f0f2f5; font-family: 'Segoe UI', sans-serif; }}
    body {{ display: flex; justify-content: center; align-items: center; padding: 12px; }}
    .container {{
      width: 100%; max-width: 440px; background: white; border-radius: 18px;
      padding: 20px; box-shadow: 0 6px 18px rgba(0,0,0,0.1); display: flex; flex-direction: column; gap: 16px;
    }}
    h1 {{ text-align: center; font-size: 22px; color: #007bff; }}
    .status-box {{
      text-align: center; padding: 14px; font-size: 20px; font-weight: bold;
      border-radius: 10px;
    }}
    .locked {{ background: #ffe6e6; color: #c0392b; border: 1px solid #e74c3c; }}
    .unlocked {{ background: #d4edda; color: #155724; border: 1px solid #28a745; }}
    .info {{ text-align: center; font-size: 16px; }}
    .btn-container {{ display: flex; flex-direction: column; gap: 10px; }}
    button {{
      padding: 14px; font-size: 18px; font-weight: bold; background: #007bff;
      color: white; border: none; border-radius: 10px;
    }}
    button:active {{ background: #0056b3; }}
    .log-area {{
      background: #f9f9f9; border: 1px solid #ccc; padding: 10px; font-family: monospace;
      font-size: 13px; border-radius: 8px; max-height: 150px; overflow-y: auto; white-space: pre-wrap;
    }}
  </style>
</head>
<body>
  <div class="container">
    <h1>Smart Lockbox</h1>
    <div id="status" class="status-box">Memuat status...</div>
    <div id="distance" class="info">Sensor Jarak: - cm</div>
    <div class="btn-container">
      <button onclick="manualUnlock()">🔓 Buka Kunci</button>
      <button onclick="manualLock()">🔒 Kunci</button>
    </div>
    <div class="log-area" id="log">Memuat log...</div>
  </div>
  <script>
    async function fetchStatus() {{
      try {{
        const res = await fetch('/status');
        const data = await res.json();
        const statusBox = document.getElementById('status');
        statusBox.textContent = data.locked ? 'TERKUNCI' : 'TERBUKA';
        statusBox.className = 'status-box ' + (data.locked ? 'locked' : 'unlocked');
        document.getElementById('distance').textContent = 'Sensor Jarak: ' + data.distance + ' cm';
        document.getElementById('log').textContent = data.log.join('\\n');
      }} catch (e) {{
        document.getElementById('status').textContent = 'Gagal mendapatkan status';
      }}
    }}
    async function manualUnlock() {{
      await fetch('/unlock', {{ method: 'POST' }});
      setTimeout(fetchStatus, 300);
    }}
    async function manualLock() {{
      await fetch('/lock', {{ method: 'POST' }});
      setTimeout(fetchStatus, 300);
    }}
    setInterval(fetchStatus, 1000);
    fetchStatus();
  </script>
</body>
</html>"""

# -------------------------- HTTP HANDLER --------------------------

def handle_http_request(conn):
    try:
        request = conn.recv(1024).decode()
        print("Request:", request)
        if 'GET /status' in request:
            response = json.dumps({
                "locked": sistem_terkunci,
                "distance": f"{sensor_distance:.1f}",
                "log": event_log
            })
            conn.send('HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n')
            conn.sendall(response)
        elif 'POST /unlock' in request:
            loop.create_task(buka_sistem("Web"))
            conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nOK')
        elif 'POST /lock' in request:
            loop.create_task(kunci_sistem())
            conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nOK')
        else:
            html = generate_html_page()
            conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
            conn.sendall(html)
    except Exception as e:
        print("Error:", e)
    finally:
        conn.close()

def run_http_server():
    s = socket.socket()
    s.bind(('', 80))
    s.listen(5)
    print("HTTP Server aktif di port 80")
    while True:
        conn, addr = s.accept()
        print("Koneksi dari", addr)
        handle_http_request(conn)

# -------------------------- MAIN --------------------------

async def main():
    global loop
    loop = asyncio.get_event_loop()
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(SSID, PASSWORD)
    print("Menghubungkan ke WiFi...")
    while not sta_if.isconnected():
        await asyncio.sleep(1)

    print("Terhubung:", sta_if.ifconfig()[0])
    sync_ntp_time()
    asyncio.create_task(ntp_loop())

    log_event("Sistem dimulai. Mengunci...")
    led_hijau.off(); led_merah.on(); solenoid.off()
    servo.move_to_angle(POS_KUNCI)

    asyncio.create_task(monitor_sensor())
    asyncio.create_task(monitor_tombol())
    _thread.start_new_thread(run_http_server, ())

    while True:
        await asyncio.sleep(10)
        gc.collect()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Program dihentikan.")
finally:
    solenoid.off(); led_merah.on(); led_hijau.off(); servo.deinit()
