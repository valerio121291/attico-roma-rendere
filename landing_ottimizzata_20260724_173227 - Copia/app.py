
from flask import Flask, render_template, request, jsonify
import json, os, smtplib, ssl
from datetime import datetime
from email.mime.text import MIMEText

app = Flask(__name__)

# === CONFIG EMAIL (dalle tue info) ===
MITTENTE = "pvalerio910@gmail.com"
PASSWORD_APP = "wrzhcjrowqtlkfqm"   # tua app password senza spazi
DESTINATARI = ["pvalerio910@gmail.com", "katia.popova13@gmail.com"]

SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_SSL_PORT = int(os.environ.get("SMTP_SSL_PORT", "465"))
SMTP_STARTTLS_PORT = int(os.environ.get("SMTP_STARTTLS_PORT", "587"))

# === LOG & BACKUP ===
LOG_DIR = "logs"
DATA_DIR = "data"
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "email_debug.log")
SUB_FILE = os.path.join(DATA_DIR, "submissions.jsonl")

def log(msg):
    ts = datetime.now().isoformat()
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{ts}] {msg}\n")

def save_submission(kind, payload):
    payload = dict(payload or {})
    payload["__kind"] = kind
    payload["__ts"] = datetime.now().isoformat()
    with open(SUB_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")

def send_mail(subject, body, reply_to=None):
    msg = MIMEText(body, _charset="utf-8")
    msg["Subject"] = subject
    msg["From"] = MITTENTE
    msg["To"] = ", ".join(DESTINATARI)
    if reply_to:
        msg["Reply-To"] = reply_to

    ctx = ssl.create_default_context()

    # 1) SSL 465
    try:
        server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_SSL_PORT, context=ctx, timeout=20)
        server.set_debuglevel(1)
        log("SMTP_SSL connect ok")
        server.login(MITTENTE, PASSWORD_APP)
        log("SMTP_SSL login ok")
        server.sendmail(MITTENTE, DESTINATARI, msg.as_string())
        log("SMTP_SSL send ok")
        server.quit()
        return
    except Exception as e:
        log(f"SSL error: {e}")

    # 2) STARTTLS 587
    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_STARTTLS_PORT, timeout=20)
        server.set_debuglevel(1)
        log("SMTP connect ok (587)")
        server.ehlo()
        server.starttls(context=ctx)
        log("STARTTLS ok")
        server.login(MITTENTE, PASSWORD_APP)
        log("SMTP login ok (587)")
        server.sendmail(MITTENTE, DESTINATARI, msg.as_string())
        log("SMTP send ok (587)")
        server.quit()
        return
    except Exception as e2:
        log(f"STARTTLS error: {e2}")
        raise RuntimeError(str(e2))

# === DATI SITO ===
try:
    with open("dati.json", encoding="utf-8") as f:
        dati = json.load(f)
except Exception:
    dati = {"prezzo": 120}

@app.route("/")
def index():
    return render_template("index.html", dati=dati)

# --- API ---
@app.route("/api/test_email", methods=["POST"])
def api_test_email():
    try:
        subject = "Test email dal sito (adapt)"
        body = f"Questo è un test inviato alle {datetime.now().isoformat()}."
        send_mail(subject, body)
        return jsonify({"success": True})
    except Exception as e:
        log(f"/api/test_email error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/contact", methods=["POST"])
def api_contact():
    try:
        data = request.get_json(force=True, silent=True) or {}
        save_submission("contact", data)
        name = (data.get("name") or "").strip()
        email = (data.get("email") or "").strip()
        message = (data.get("message") or "").strip()
        if not name or not email or not message:
            return jsonify({"success": False, "error": "Campi mancanti"}), 400
        subject = f"Nuova richiesta contatti - {name}"
        body = f"Nome: {name}\nEmail: {email}\n\nMessaggio:\n{message}\n\nInviato: {datetime.now().isoformat()}"
        send_mail(subject, body, reply_to=email or None)
        return jsonify({"success": True})
    except Exception as e:
        log(f"/api/contact error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/prenota", methods=["POST"])
def prenota():
    try:
        data = request.get_json(force=True, silent=True) or {}
        save_submission("booking", data)
        nome = (data.get("nome") or "").strip()
        email = (data.get("email") or "").strip()
        checkin = (data.get("checkin") or "").strip()
        checkout = (data.get("checkout") or "").strip()
        adulti = int(data.get("adulti", 0) or 0)
        bambini = int(data.get("bambini", 0) or 0)
        neonati = int(data.get("neonati", 0) or 0)

        notti = 0
        totale = 0.0
        try:
            in_date = datetime.strptime(checkin, "%Y-%m-%d")
            out_date = datetime.strptime(checkout, "%Y-%m-%d")
            notti = max((out_date - in_date).days, 0)
            prezzo_notte = float(dati.get("prezzo", 0) or 0)
            totale = prezzo_notte * notti
        except Exception as e:
            log(f"date parse error: {e}")

        subject = "Nuova prenotazione dal sito"
        body = f"""Nuova prenotazione:

Nome: {nome}
Email: {email}
Check-in: {checkin}
Check-out: {checkout}
Adulti: {adulti}
Bambini: {bambini}
Neonati: {neonati}
Numero notti: {notti}
Prezzo totale: €{totale:.2f}

Inviato: {datetime.now().isoformat()}
"""
        send_mail(subject, body, reply_to=email or None)
        return jsonify({"success": True})
    except Exception as e:
        log(f"/prenota error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
# ============================================
# GEMINI CHATBOT
# ============================================
@app.route('/ask-gemini', methods=['POST'])
def ask_gemini():
    """Proxy per chiamare Google Gemini"""
    try:
        data = request.get_json(force=True, silent=True) or {}
        question = data.get('question', '').strip()
        
        if not question:
            return jsonify({'success': False, 'error': 'Domanda vuota'}), 400
        
        # La tua API Key di Gemini
        API_KEY = 'AIzaSyB_vcVb52oV4HsqX1hSP_B2ixTrklyAnac'
        MODEL = 'gemini-2.5-flash'
        
        # Prepara la richiesta per Gemini
        system_prompt = """Sei un assistente per un attico vacanze a Roma chiamato "Attico con terrazzo panoramico". 
        Rispondi in italiano, amichevole e conciso. Massimo 4 frasi.
        Informazioni sull'attico:
        - Prezzo: €120 a notte, sconto 10% se prenotano dal sito
        - Ospiti: massimo 3 persone
        - Camere: 2 camere da letto, 1 bagno, soggiorno con cucina attrezzata
        - Servizi: Wi-Fi, aria condizionata, lavatrice, parcheggio gratuito, TV, ascensore
        - Check-in: flessibile, istruzioni via email
        - Check-out: entro le 10:00 (flessibile su richiesta)
        - Posizione: Via Guido Ascoli, quartiere EUR, Roma
        - Metro: Laurentina (Linea B) a 10 minuti a piedi
        - Autobus: fermata a 5 minuti (linee 714, 780, 716)
        - Attrazioni vicine: Colosseo (20 min bus), Piazza Navona (30 min), Trastevere (15 min), Vaticano (30 min)
        - Ristorante consigliato: Osteria Sanmarzano a 5 minuti a piedi
        - Emergenza: 112
        
        Non inventare informazioni. Usa solo quelle che ti ho dato."""
        
        url = f'https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}'
        
        headers = {'Content-Type': 'application/json'}
        body = {
            'contents': [{
                'parts': [{
                    'text': f'{system_prompt}\n\nDOMANDA UTENTE: {question}\n\nRISPONDI IN MODO CHIARO E CONCISO:'
                }]
            }]
        }
        
        import requests
        response = requests.post(url, headers=headers, json=body, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                answer = result['candidates'][0]['content']['parts'][0]['text']
                # Pulisci la risposta
                answer = answer.replace('**', '').replace('#', '').replace('\n', ' ').strip()
                return jsonify({'success': True, 'answer': answer})
        
        return jsonify({'success': False, 'error': 'Gemini non ha risposto'})
        
    except Exception as e:
        log(f"/ask-gemini error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
