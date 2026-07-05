"""
Agent Typo & Grammar Checker
Memperbaiki typo, ejaan, tanda baca, huruf kapital, spasi,
dan konsistensi istilah pada teks berbahasa Indonesia.

Backend: Groq API (gratis, cepat, tanpa kartu kredit)
"""

import os
import sys
import json
import textwrap
from groq import Groq

# Paksa stdout ke UTF-8 agar emoji tampil di terminal Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# ── Konstanta ─────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """
Kamu adalah editor bahasa Indonesia yang teliti dan berpengalaman.
Tugasmu adalah memeriksa dan memperbaiki teks yang diberikan oleh pengguna.

Yang HARUS kamu periksa dan perbaiki:
1. Typo (salah ketik)
2. Ejaan yang salah
3. Tanda baca yang kurang atau salah
4. Huruf kapital (awal kalimat, nama diri, singkatan)
5. Spasi yang berlebihan atau kurang
6. Konsistensi istilah (misalnya: "e-mail" vs "email" → pilih satu)

Yang TIDAK BOLEH kamu ubah:
- Makna atau isi asli teks
- Gaya penulisan penulis (formal/informal) selama sudah benar
- Pilihan kata yang sudah tepat
- Struktur kalimat yang sudah baik

Format respons kamu HARUS berupa JSON yang valid seperti berikut:
{
    "teks_diperbaiki": "<teks lengkap setelah diperbaiki>",
    "daftar_kesalahan": [
        {
            "no": 1,
            "teks_asli": "<kata atau frasa yang salah>",
            "perbaikan": "<kata atau frasa yang benar>",
            "jenis_kesalahan": "<jenis: Typo / Ejaan / Tanda Baca / Huruf Kapital / Spasi / Konsistensi Istilah>"
        }
    ],
    "ringkasan": "<penjelasan singkat 1–3 kalimat tentang perbaikan yang dilakukan>"
}

Jika tidak ada kesalahan, kembalikan "daftar_kesalahan" sebagai list kosong [] dan tulis
"ringkasan" yang menyatakan teks sudah benar.
Pastikan JSON yang kamu kembalikan bisa di-parse tanpa error. Jangan tambahkan teks apa pun
di luar JSON.
""".strip()

MODEL_ID  = "llama-3.3-70b-versatile"
SEPARATOR = "─" * 60


# ── Fungsi utama ───────────────────────────────────────────────────────────────

def get_api_key() -> str:
    """Membaca Groq API key dari environment variable."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "Environment variable GROQ_API_KEY tidak ditemukan.\n"
            "Silakan set terlebih dahulu:\n"
            "  Windows CMD  : set GROQ_API_KEY=gsk_...\n"
            "  Windows PS   : $env:GROQ_API_KEY='gsk_...'\n"
            "  Linux/macOS  : export GROQ_API_KEY=gsk_...\n\n"
            "Dapatkan API key gratis di: https://console.groq.com"
        )
    return api_key


def check_and_fix(client: Groq, teks: str) -> dict:
    """
    Mengirim teks ke Groq API dan mengembalikan hasil perbaikan
    dalam bentuk dictionary.
    """
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": teks},
        ],
        temperature=0.2,                          # rendah agar konsisten & presisi
        response_format={"type": "json_object"},  # paksa output JSON
    )

    raw_json = response.choices[0].message.content
    hasil = json.loads(raw_json)
    return hasil


def tampilkan_hasil(teks_asli: str, hasil: dict) -> None:
    """Menampilkan hasil perbaikan ke terminal dengan format yang rapi."""

    teks_diperbaiki  = hasil.get("teks_diperbaiki", "")
    daftar_kesalahan = hasil.get("daftar_kesalahan", [])
    ringkasan        = hasil.get("ringkasan", "")

    print(f"\n{SEPARATOR}")
    print("  HASIL PEMERIKSAAN TEKS")
    print(SEPARATOR)

    # ── Teks asli ──
    print("\n📝  TEKS ASLI:")
    print(textwrap.fill(teks_asli, width=70,
                        initial_indent="    ", subsequent_indent="    "))

    # ── Teks diperbaiki ──
    print("\n✅  TEKS YANG DIPERBAIKI:")
    print(textwrap.fill(teks_diperbaiki, width=70,
                        initial_indent="    ", subsequent_indent="    "))

    # ── Daftar kesalahan ──
    print(f"\n🔍  DAFTAR KESALAHAN ({len(daftar_kesalahan)} ditemukan):")
    if not daftar_kesalahan:
        print("    Tidak ada kesalahan yang ditemukan.")
    else:
        for item in daftar_kesalahan:
            print(
                f"\n    [{item.get('no', '?')}] Jenis    : {item.get('jenis_kesalahan', '-')}\n"
                f"        Asli      : \"{item.get('teks_asli', '-')}\"\n"
                f"        Perbaikan : \"{item.get('perbaikan', '-')}\""
            )

    # ── Ringkasan ──
    print(f"\n💡  RINGKASAN PERBAIKAN:")
    print(textwrap.fill(ringkasan, width=70,
                        initial_indent="    ", subsequent_indent="    "))

    print(f"\n{SEPARATOR}\n")


# ── Entry point ────────────────────────────────────────────────────────────────

def main() -> None:
    print("=" * 60)
    print("   AGENT TYPO & GRAMMAR CHECKER — Bahasa Indonesia")
    print("   (Powered by Groq + Llama 3.3 70B)")
    print("=" * 60)
    print("Ketik teks yang ingin diperiksa, lalu tekan Enter dua kali.")
    print("Ketik 'keluar' atau 'exit' untuk mengakhiri program.\n")

    # Inisialisasi klien Groq (API key dibaca dari env variable)
    try:
        api_key = get_api_key()
    except EnvironmentError as e:
        print(f"\n[ERROR] {e}")
        return

    client = Groq(api_key=api_key)

    while True:
        print("Masukkan teks (tekan Enter dua kali untuk submit):")
        baris = []
        try:
            while True:
                baris_input = input()
                if baris_input.strip().lower() in ("keluar", "exit"):
                    print("\nTerima kasih telah menggunakan Agent Typo & Grammar Checker. Sampai jumpa!")
                    return
                if baris_input == "" and baris:
                    break           # baris kosong setelah ada isi → submit
                if baris_input != "":
                    baris.append(baris_input)
        except (KeyboardInterrupt, EOFError):
            print("\n\nProgram dihentikan.")
            return

        teks = "\n".join(baris).strip()
        if not teks:
            print("[INFO] Teks kosong, silakan coba lagi.\n")
            continue

        print("\n⏳  Memeriksa teks… (menghubungi Groq API)\n")
        try:
            hasil = check_and_fix(client, teks)
            tampilkan_hasil(teks, hasil)
        except json.JSONDecodeError:
            print("[ERROR] Respons dari AI tidak dapat diparse sebagai JSON. Coba lagi.\n")
        except Exception as e:
            print(f"[ERROR] Terjadi kesalahan: {e}\n")


if __name__ == "__main__":
    main()
