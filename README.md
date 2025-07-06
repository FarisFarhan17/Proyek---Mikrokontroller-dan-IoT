# Smart Door IoT Project — Kelompok 15

## Anggota
- **Ariel Yosua Hasibuan** — 105222004  
- **Faris Farhan** — 105222013

---

## Deskripsi
Sistem **Smart Lockbox** ini merupakan solusi keamanan rumah berbasis **ESP32**, dikembangkan menggunakan **MicroPython**, yang memungkinkan **penguncian/pembukaan pintu otomatis**, **notifikasi real-time via Telegram**, serta kontrol melalui **antarmuka web lokal**.

---

## 📦 Fitur Utama

- Deteksi keberadaan tamu menggunakan **sensor ultrasonik HC-SR04**
- Mekanisme **kunci otomatis** menggunakan **servo motor + solenoid**
- Kontrol pintu dari jarak jauh via **Web UI** dan **Telegram Bot**
- Indikator visual/audio dengan **LED & buzzer**
- Logging aktivitas pintu disertai timestamp
- **Berbasis MicroPython** dan dapat dijalankan langsung di ESP32

---

## 🧰 Komponen yang Digunakan

| No | Komponen           | Fungsi                                 |
|----|--------------------|----------------------------------------|
| 1  | ESP32              | Mikrokontroler utama                   |
| 2  | HC-SR04            | Sensor ultrasonik (deteksi objek)     |
| 3  | Servo SG90         | Menggerakkan mekanisme pintu          |
| 4  | Solenoid 12V       | Aktuator pengunci pintu                |
| 5  | Push Button        | Akses manual dari dalam rumah          |
| 6  | LED Merah/Hijau    | Indikator status sistem                |
| 7  | Buzzer             | Notifikasi audio                       |
| 8  | Transistor TIP122  | Driver solenoid                        |
| 9  | Diode 1N4007       | Proteksi back EMF                      |
| 10 | Catu Daya 12V      | Sumber daya eksternal                  |

---

## ⚙️ Cara Kerja Sistem

1. Saat tamu berdiri di depan pintu, sensor HC-SR04 mendeteksi keberadaan selama 3 detik.
2. Sistem mengirim notifikasi ke Telegram beserta tautan Web UI.
3. Pemilik rumah membuka Web UI dan menekan tombol “🔓 Buka Kunci”.
4. Sistem membuka pintu dengan solenoid & servo, lalu menunggu tombol ditekan dari dalam untuk menutup kembali secara otomatis.

---

## 🌐 Web Interface

Dapat diakses melalui IP lokal (contoh: `http://192.168.1.100/`), berisi:

- Status sistem (TERKUNCI/TERBUKA)
- Sensor jarak real-time
- Tombol kontrol manual (Buka/Kunci)
- Log aktivitas terakhir

---

## 💬 Telegram Bot

Gunakan Telegram bot untuk menerima:

- Notifikasi tamu terdeteksi
- Log orang keluar
- Tautan akses cepat ke Web UI

> Buat bot baru di [@BotFather](https://t.me/BotFather), lalu masukkan `BOT_TOKEN` dan `CHAT_ID` Anda ke `main.py`.

---

## 📁 Struktur File
main.py: "File utama logika ESP32"
hcsr04.py: "Library HC-SR04"
servo.py: "Library servo motor"
README.md: "Dokumentasi proyek"



## Diagram Perangkat Keras

![Diagram Blok Sistem](Task%202%20&%203/Diagram.png)

---

---

## 🚫 Catatan

- **ESP32-CAM tidak digunakan** dalam proyek ini karena tidak mendukung penuh MicroPython.
- Pastikan koneksi Wi-Fi stabil agar Web UI dan notifikasi Telegram bekerja maksimal.
- Jalankan kode menggunakan firmware MicroPython versi terbaru untuk ESP32.

---

## 📽️ Demo

Tonton video demonstrasi sistem:  
[▶️ Video Demo Smart Lockbox](https://drive.google.com/file/d/1It_olBMoI0XDhckOkO42Efe23fB0Skgu/view?usp=sharing)

---
