# 📌 Smart Door IoT Project — Kelompok 15

## 👥 Anggota
- **Ariel Yosua Hasibuan** — 105222004  
- **Faris Farhan** — 105222013

---

## 📘 Deskripsi
**Smart Door** adalah sistem keamanan pintu berbasis **ESP32-CAM** dan **Internet of Things (IoT)**. Sistem ini dirancang untuk:
- Mengambil gambar pengunjung saat tombol ditekan.
- Mengirim gambar ke smartphone pemilik rumah via internet (rencana menggunakan **Telegram API**).
- Memberi kontrol akses jarak jauh untuk membuka pintu secara otomatis melalui **servo** atau **solenoid lock**.

---

## 🎯 Tujuan Proyek
1. Mendeteksi pengunjung dan menangkap gambar otomatis.
2. Mengirimkan gambar ke pemilik rumah secara real-time.
3. Memberikan kontrol jarak jauh untuk membuka pintu.
4. Mengintegrasikan sistem buka pintu otomatis (servo/solenoid).
5. Menyediakan solusi keamanan IoT yang terjangkau dan fleksibel.

---

## 🌍 SDGs Relevan: Nomor 11 — Kota dan Permukiman Berkelanjutan
**Target:**
- 11.1: Akses terhadap perumahan layak, aman, dan terjangkau.
- 11.7: Akses universal ke ruang publik aman dan inklusif.
- 11.B: Penerapan teknologi inovatif di tingkat lokal.

**Kontribusi Proyek:**
- Memberikan kontrol akses terhadap siapa yang boleh masuk rumah.
- Mempromosikan teknologi keamanan berbasis IoT.
- Menunjang keamanan perumahan dengan solusi efisien dan hemat energi.

---

## 🧩 Diagram Blok Sistem

![Diagram Blok Sistem](Task%202/Diagram%20Blok%20Sistem.png)

---

## 🧰 Daftar Komponen

| No | Komponen             | Fungsi                                                                 |
|----|----------------------|------------------------------------------------------------------------|
| 1  | ESP32-CAM            | Mikrokontroler + kamera, kirim gambar via Wi-Fi                        |
| 2  | Push Button          | Ditekan pengunjung untuk trigger kamera                                |
| 3  | Solenoid Lock/Servo  | Membuka/tutup pintu secara otomatis                                    |
| 4  | Resistor             | Menstabilkan sinyal input dari button                                  |
| 5  | Kabel Jumper         | Menghubungkan komponen elektronik                                      |
| 6  | Breadboard           | Tempat merakit rangkaian prototipe                                     |

---

## ⚙️ Alur Sistem (Flow)
1. Pengunjung menekan tombol.
2. ESP32-CAM mengambil gambar.
3. Gambar dikirim via Wi-Fi ke Telegram.
4. Pemilik rumah menerima gambar.
5. Pemilik dapat memilih untuk membuka pintu.
6. Servo atau solenoid akan membuka pintu secara otomatis.
