<p align="center">
  <img src="assets/banner.png" alt="AegisVault Banner" width="600">
</p>

# 🛡️ AegisVault: Ultimate Image Steganography

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8%2B-blue?style=for-the-badge&logo=python" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/badge/GUI-PySide6-orange?style=for-the-badge&logo=qt" alt="GUI">
  <img src="https://img.shields.io/badge/Security-AES--256-red?style=for-the-badge&logo=lock" alt="Security">
  <img src="https://img.shields.io/badge/Maintainer-Athallah1234-purple?style=for-the-badge" alt="Maintainer">
</p>

**AegisVault** adalah aplikasi desktop steganografi tingkat lanjut yang menggabungkan keindahan desain modern dengan keamanan enkripsi militer. Sembunyikan pesan rahasia Anda di dalam gambar PNG tanpa meninggalkan jejak visual sedikitpun.

---

## 🌟 Kenapa Memilih AegisVault?

AegisVault dirancang untuk pengguna yang mementingkan **Privasi**, **Estetika**, dan **Keamanan**.

### ✨ Fitur Unggulan:
- 🎨 **Modern Dark Interface**: Desain UI premium dengan tema gelap yang elegan dan transisi halus.
- 🔐 **Military-Grade Encryption**: Enkripsi **AES-256 (Fernet)** dengan salt **PBKDF2**.
- 🕵️ **Invisible LSB Technique**: Perubahan bit yang tidak terdeteksi oleh mata manusia.
- ⚡ **Multi-Threaded Engine**: Aplikasi tetap responsif saat memproses gambar resolusi tinggi.
- 📦 **Smart Compression**: Menggunakan **Zlib** untuk memaksimalkan kapasitas simpan.
- 🖱️ **Drag & Drop Experience**: Tarik dan lepas gambar untuk mulai secara instan.

---

## 📸 Antarmuka Pengguna (UI)

| Encode Mode | Decode Mode |
| :--- | :--- |
| ![Encode](assets/encode.png) | ![Decode](assets/decode.png) |

---

## 🚀 Memulai Cepat (Quick Start)

### 1. Instalasi
```bash
git clone https://github.com/username/AegisVault.git
cd AegisVault
pip install -r requirements.txt
```

### 2. Jalankan Aplikasi
```bash
python main.py
```

### 3. Pintasan Keyboard (Shortcuts) ⌨️
| Tombol | Fungsi | Tombol | Fungsi |
| :--- | :--- | :--- | :--- |
| `Ctrl + O` | Buka Gambar | `Ctrl + S` | Simpan Hasil |
| `Ctrl + E` | Tab Encode | `Ctrl + D` | Tab Decode |
| `Ctrl + T` | Ganti Tema | `Ctrl + C` | Salin Hasil |

---

## 📘 Panduan Penggunaan

### 🔐 Menyembunyikan Pesan (Encoding):
1. Pilih gambar PNG di tab **Encode**.
2. Masukkan pesan rahasia dan password enkripsi.
3. Klik **"Mulai Encode & Simpan"**.

### 🔓 Mengambil Pesan (Decoding):
1. Masukkan gambar hasil steganografi di tab **Decode**.
2. Masukkan password yang benar dan klik **"Ekstrak Pesan"**.

---

## 📊 Analisis Performa & Kapasitas

| Resolusi Gambar | Total Sub-Piksel | Kapasitas Teoritis | Estimasi Karakter |
| :--- | :--- | :--- | :--- |
| **HD (1280x720)** | 3.686.400 | ~460 KB | ~450.000 |
| **Full HD (1920x1080)** | 8.294.400 | ~1 MB | ~1.000.000 |
| **4K (3840x2160)** | 33.177.600 | ~4.1 MB | ~4.000.000 |

---

## 🔐 Keamanan & Detail Teknis (Deep Dive)

### 🛠️ Alur Kerja (Workflow)
```text
[PESAN] -> [KOMPRESI ZLIB] -> [ENKRIPSI AES-256] -> [LSB EMBEDDING] -> [GAMBAR STEGO]
```

### 🛡️ Lapisan Keamanan
1. **PBKDF2-HMAC-SHA256**: 100,000 iterasi untuk derivasi kunci dari password.
2. **AES-256 CBC**: Standar enkripsi global untuk kerahasiaan data.
3. **Just Noticeable Difference (JND)**: Perubahan warna ±1 unit, aman dari persepsi visual.

---

## 🧩 Ekosistem Proyek

### 📂 Struktur Folder
```text
├── src/
│   ├── core/           # Logika LSB & Bit Manipulation
│   ├── crypto/         # Enkripsi AES & Hashing
│   ├── gui/            # UI, Styles, & Custom Widgets
│   └── utils/          # Logger & Helpers
├── assets/             # Media & Banner Proyek
└── main.py             # Entry Point
```

### 📦 Dependensi Utama
- **PySide6**: Core Framework GUI.
- **Pillow & NumPy**: Image Processing & Vector Math.
- **Cryptography**: Security Standard.

---

## 🗺️ Roadmap & Changelog

### 🚀 Roadmap Masa Depan
- [ ] **AI Detector**: Menguji ketahanan gambar terhadap steganografi.
- [ ] **Batch Processing**: Memproses banyak gambar sekaligus.
- [ ] **Mobile Support**: Versi Android & iOS.

### 📝 Changelog v1.0.0
- Rilis awal AegisVault dengan LSB, AES-256, dan Dark Mode UI.

---

## ❓ FAQ & Troubleshooting

**Q: Kenapa gambar hasil decode tidak muncul?**
Pastikan gambar tidak di-*resize* atau di-*compress* oleh aplikasi lain (seperti WhatsApp), karena ini akan merusak data LSB.

**Q: Error: ModuleNotFoundError?**
Pastikan sudah menjalankan `pip install -r requirements.txt`.

---

## 🤝 Kontribusi & Dukungan

### Cara Berkontribusi
1. Fork proyek.
2. Buat branch fitur.
3. Submit Pull Request.

### 💖 Dukung Kami
Jika bermanfaat, berikan ⭐ **Star** atau dukung melalui [GitHub Sponsors](https://example.com).

---

## ⚖️ Legalitas & Kredit

### Ucapan Terima Kasih 🙏
Terima kasih kepada komunitas **Qt**, **Pillow**, dan **Cryptography.io**.

### Lisensi & Penafian
- Berlisensi di bawah **MIT License**.
- **Disclaimer**: Digunakan hanya untuk tujuan edukasi. Penulis tidak bertanggung jawab atas penyalahgunaan aplikasi.

---

<p align="center">
  Dibuat dengan ❤️ oleh <b>Athallah1234</b>
  <br>
  <i>"AegisVault - Protecting your secrets, one pixel at a time."</i>
</p>
