# 🔍 Agent Typo & Grammar Checker

Program berbasis Python yang menggunakan **Groq API** untuk memeriksa dan memperbaiki teks berbahasa Indonesia secara otomatis — didukung model **Llama 3.3 70B**.

---

## ✨ Fitur

- **Deteksi & perbaikan typo** — menemukan kata yang salah ketik
- **Ejaan** — memperbaiki penulisan kata yang tidak sesuai EYD/KBBI
- **Tanda baca** — menambah atau memperbaiki koma, titik, tanda tanya, dll.
- **Huruf kapital** — memastikan huruf besar di awal kalimat, nama diri, dan singkatan
- **Spasi** — menghapus spasi berlebih atau menambah yang kurang
- **Konsistensi istilah** — menyeragamkan penulisan istilah yang sama
- **Tidak mengubah makna** — AI hanya memperbaiki kesalahan teknis, bukan mengubah konten

---

## 🗂️ Struktur Proyek

```
typo-checker-agent/
├── app.py        ← Program utama
└── README.md     ← Dokumentasi ini
```

---

## 📋 Prasyarat

| Kebutuhan | Keterangan |
|-----------|-----------|
| Python | Versi 3.9 atau lebih baru |
| Library `groq` | Groq Python SDK |
| Groq API Key | **Gratis** di https://console.groq.com |

---

## 🚀 Cara Menjalankan

### 1. Clone / Unduh proyek

```bash
git clone <url-repo>
cd typo-checker-agent
```

### 2. Instal dependensi

```bash
pip install groq
```

> **Opsional:** gunakan virtual environment agar dependensi terisolasi.
> ```bash
> python -m venv venv
>
> # Windows CMD
> venv\Scripts\activate
>
> # Windows PowerShell
> venv\Scripts\Activate.ps1
>
> # Linux / macOS
> source venv/bin/activate
>
> pip install groq
> ```

### 3. Dapatkan Groq API Key (Gratis)

1. Buka → [https://console.groq.com](https://console.groq.com)
2. Login dengan akun Google atau GitHub
3. Pilih menu **"API Keys"** di sidebar
4. Klik **"Create API Key"**
5. Salin key yang muncul (format: `gsk_...`)

### 4. Set environment variable `GROQ_API_KEY`

> ⚠️ **Jangan pernah menulis API key langsung di dalam kode.**

**Windows — Command Prompt:**
```cmd
set GROQ_API_KEY=gsk_...kunci-api-kamu...
```

**Windows — PowerShell:**
```powershell
$env:GROQ_API_KEY="gsk_...kunci-api-kamu..."
```

**Linux / macOS:**
```bash
export GROQ_API_KEY="gsk_...kunci-api-kamu..."
```

### 5. Jalankan program

```bash
python app.py
```

---

## 🖥️ Contoh Penggunaan

```
============================================================
   AGENT TYPO & GRAMMAR CHECKER — Bahasa Indonesia
   (Powered by Groq + Llama 3.3 70B)
============================================================
Ketik teks yang ingin diperiksa, lalu tekan Enter dua kali.
Ketik 'keluar' atau 'exit' untuk mengakhiri program.

Masukkan teks (tekan Enter dua kali untuk submit):
saya sudh makan pagi tadi , tapi lupa bawa dompet kekantor.

⏳  Memeriksa teks… (menghubungi Groq API)

────────────────────────────────────────────────────────────
  HASIL PEMERIKSAAN TEKS
────────────────────────────────────────────────────────────

📝  TEKS ASLI:
    saya sudh makan pagi tadi , tapi lupa bawa dompet kekantor.

✅  TEKS YANG DIPERBAIKI:
    Saya sudah makan pagi tadi, tapi lupa membawa dompet ke kantor.

🔍  DAFTAR KESALAHAN (5 ditemukan):

    [1] Jenis    : Huruf Kapital
        Asli      : "saya"
        Perbaikan : "Saya"

    [2] Jenis    : Typo
        Asli      : "sudh"
        Perbaikan : "sudah"

    [3] Jenis    : Spasi
        Asli      : "kekantor"
        Perbaikan : "ke kantor"

    [4] Jenis    : Ejaan
        Asli      : "bawa"
        Perbaikan : "membawa"

    [5] Jenis    : Tanda Baca
        Asli      : "tadi ,"
        Perbaikan : "tadi,"

💡  RINGKASAN PERBAIKAN:
    Teks telah diperbaiki untuk memperbaiki kesalahan typo, ejaan,
    tanda baca, huruf kapital, dan spasi.

────────────────────────────────────────────────────────────
```

---

## ⌨️ Cara Input Multi-baris

Program mendukung input beberapa baris teks:

1. Ketik baris pertama → tekan **Enter**
2. Ketik baris berikutnya → tekan **Enter**
3. Tekan **Enter sekali lagi** (baris kosong) untuk mengirim

---

## 🛑 Keluar dari Program

Ketik `keluar` atau `exit` lalu tekan **Enter**, atau tekan **Ctrl+C**.

---

## ⚙️ Konfigurasi Model

Model yang digunakan secara default adalah **`llama-3.3-70b-versatile`** (akurat dan mendukung bahasa Indonesia dengan baik).
Untuk mengganti ke model lain, ubah baris ini di `app.py`:

```python
MODEL_ID = "llama-3.3-70b-versatile"   # ← ganti sesuai kebutuhan
```

Model Groq yang tersedia (gratis):

| Model | Kecepatan | Kualitas |
|-------|-----------|---------|
| `llama-3.3-70b-versatile` | ⚡ Cepat | ★★★★★ |
| `llama-3.1-8b-instant` | ⚡⚡ Sangat cepat | ★★★ |
| `gemma2-9b-it` | ⚡ Cepat | ★★★★ |

---

## 📄 Lisensi

Proyek ini dibuat untuk keperluan pembelajaran. Silakan digunakan dan dimodifikasi sesuai kebutuhan.
