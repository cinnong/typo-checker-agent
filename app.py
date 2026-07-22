"""
Agent Typo & Grammar Checker — REST API Server
Memperbaiki typo, ejaan, tanda baca, huruf kapital, spasi,
dan konsistensi istilah pada teks berbahasa Indonesia.

Backend : Groq API (llama-3.3-70b-versatile)
Server  : FastAPI + Uvicorn
"""

import os
import json
from typing import Optional

from groq import Groq
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn


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

MODEL_ID = "llama-3.3-70b-versatile"


# ── Pydantic Models ───────────────────────────────────────────────────────────

class OrchestratorPayload(BaseModel):
    raw_text: Optional[str] = None
    url: Optional[str] = None
    keyword: Optional[str] = None


class OrchestratorRequest(BaseModel):
    task_id: str
    agent_type: str
    payload: OrchestratorPayload


class AgentSuccessData(BaseModel):
    result: Optional[str] = None
    file_url: Optional[str] = None


class AgentSuccessResponse(BaseModel):
    status: str = "success"
    task_id: str
    data: AgentSuccessData
    message: str


class AgentErrorResponse(BaseModel):
    status: str = "error"
    task_id: Optional[str] = None
    data: Optional[dict] = None
    message: str


# ── FastAPI App ───────────────────────────────────────────────────────────────

app = FastAPI(
    title="Typo Checker Agent",
    description="REST API Agent untuk memeriksa typo dan grammar Bahasa Indonesia.",
    version="2.0.0",
)

# CORS Middleware
CORS_ORIGINS = [
    "https://jokitugas.bananaunion.web.id",
    "http://localhost:3000",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Helper ────────────────────────────────────────────────────────────────────

def get_groq_client() -> Groq:
    """Membuat instance Groq client dari environment variable."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "Environment variable GROQ_API_KEY tidak ditemukan. "
            "Dapatkan API key gratis di: https://console.groq.com"
        )
    return Groq(api_key=api_key)


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


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/", summary="Health Check")
def health_check():
    """Endpoint untuk mengecek status agen."""
    return {"status": "online", "agent": "typo_checker"}


@app.post(
    "/process",
    response_model=AgentSuccessResponse,
    summary="Proses Pemeriksaan Typo & Grammar",
)
def process(request: OrchestratorRequest):
    """
    Menerima request dari Orchestrator, memeriksa typo & grammar pada
    `raw_text` menggunakan Groq API, dan mengembalikan teks yang telah
    diperbaiki.
    """
    task_id = request.task_id
    raw_text = request.payload.raw_text

    # Validasi input
    if not raw_text or not raw_text.strip():
        raise HTTPException(
            status_code=400,
            detail=AgentErrorResponse(
                status="error",
                task_id=task_id,
                data=None,
                message="Field 'raw_text' tidak boleh kosong.",
            ).model_dump(),
        )

    # Proses dengan Groq API
    try:
        client = get_groq_client()
        hasil = check_and_fix(client, raw_text.strip())
        teks_diperbaiki = hasil.get("teks_diperbaiki", raw_text)

        return AgentSuccessResponse(
            status="success",
            task_id=task_id,
            data=AgentSuccessData(
                result=teks_diperbaiki,
                file_url=None,
            ),
            message="Pemeriksaan typo dan grammar berhasil diproses.",
        )

    except EnvironmentError as e:
        raise HTTPException(
            status_code=500,
            detail=AgentErrorResponse(
                status="error",
                task_id=task_id,
                data=None,
                message=f"Konfigurasi server error: {str(e)}",
            ).model_dump(),
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail=AgentErrorResponse(
                status="error",
                task_id=task_id,
                data=None,
                message="Gagal mem-parse respons dari Groq API sebagai JSON.",
            ).model_dump(),
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=AgentErrorResponse(
                status="error",
                task_id=task_id,
                data=None,
                message=f"Terjadi kesalahan saat memproses: {str(e)}",
            ).model_dump(),
        )


# ── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
