# install_chatbot_clean.py - VERSIONE DEFINITIVA CHE PULISCE TUTTO
import os
import re
import shutil
from pathlib import Path

class ChatbotInstaller:
    def __init__(self, source_path):
        self.source = Path(source_path)
        self.templates_dir = self.source / 'templates'
        self.static_dir = self.source / 'static'
        self.js_dir = self.static_dir / 'js'
        self.css_dir = self.static_dir / 'css'
        
    def clean_everything(self):
        """Rimuove TUTTE le tracce del chatbot da OGNI file"""
        print("🧹 Pulizia COMPLETA...")
        
        # 1. Elimina i file fisici
        files_to_delete = [
            self.js_dir / 'chatbot.js',
            self.css_dir / 'chatbot.css',
            self.js_dir / 'main.js',  # se esiste
        ]
        for file in files_to_delete:
            if file.exists():
                file.unlink()
                print(f"  ✅ Rimosso: {file}")
        
        # 2. Pulisci OGNI pagina HTML
        pages = [
            self.templates_dir / 'index.html',
            self.templates_dir / 'en' / 'index.html',
            self.templates_dir / 'es' / 'index.html',
            self.templates_dir / 'ru' / 'index.html',
            self.templates_dir / 'zh' / 'index.html'
        ]
        
        for page in pages:
            if page.exists():
                self.clean_page_completely(page)
        
        print("  ✅ Pulizia completata!")
        
    def clean_page_completely(self, html_path):
        """Rimuove COMPLETAMENTE il chatbot da una pagina"""
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Rimuovi TUTTO ciò che riguarda il chatbot
        # Pattern da rimuovere
        patterns = [
            # Chatbot container
            r'<!-- CHATBOT - .*? -->',
            r'<div class="chatbot-container".*?</div>',
            r'<div class="chatbot-float".*?</div>',
            r'<div class="chatbot-wrapper".*?</div>',
            r'<div class="floating-buttons".*?</div>',
            # Link CSS
            r'<link rel="stylesheet" href="[^"]*chatbot[^"]*\.css">',
            r'<link rel="stylesheet" href="[^"]*main\.css">',
            # Script JS
            r'<script src="[^"]*chatbot[^"]*\.js"></script>',
            r'<script src="[^"]*main\.js"></script>',
            # CSS inline del chatbot
            r'/\* ===== CHATBOT.*?\*/.*?}',
        ]
        
        for pattern in patterns:
            content = re.sub(pattern, '', content, flags=re.DOTALL)
        
        # Rimuovi righe vuote multiple
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        content = re.sub(r'\n\s*\n', '\n', content)
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ Pulita: {html_path.name}")

    def create_chatbot_files(self):
        """Crea i file del chatbot"""
        print("\n🤖 Creazione file del chatbot...")
        
        self.js_dir.mkdir(parents=True, exist_ok=True)
        self.css_dir.mkdir(parents=True, exist_ok=True)
        
        # Crea chatbot.js
        js_path = self.js_dir / 'chatbot.js'
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(self.get_chatbot_js())
        print("  ✅ Creata: static/js/chatbot.js")
        
        # Crea chatbot.css
        css_path = self.css_dir / 'chatbot.css'
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(self.get_chatbot_css())
        print("  ✅ Creata: static/css/chatbot.css")
        
        return True
    
    def install_in_page(self, html_path):
        """Installa il chatbot in una pagina"""
        if not html_path.exists():
            return False
        
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pulisci TUTTO prima di installare
        patterns = [
            r'<!-- CHATBOT - .*? -->',
            r'<div class="chatbot-container".*?</div>',
            r'<div class="chatbot-float".*?</div>',
            r'<div class="chatbot-wrapper".*?</div>',
            r'<div class="floating-buttons".*?</div>',
            r'<link rel="stylesheet" href="[^"]*chatbot[^"]*\.css">',
            r'<script src="[^"]*chatbot[^"]*\.js"></script>',
        ]
        for pattern in patterns:
            content = re.sub(pattern, '', content, flags=re.DOTALL)
        
        # 1. Aggiungi CSS (solo se non c'è già)
        css_link = '<link rel="stylesheet" href="/static/css/chatbot.css">'
        if 'chatbot.css' not in content:
            if 'font-awesome' in content:
                content = content.replace(
                    '<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet">',
                    f'<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet">\n    {css_link}'
                )
            else:
                content = content.replace('</head>', f'    {css_link}\n</head>')
        
        # 2. Aggiungi HTML del chatbot (subito dopo body)
        chatbot_html = self.get_chatbot_html()
        # Trova la posizione giusta dopo <body>
        if '<body>' in content:
            content = content.replace('<body>', f'<body>\n{chatbot_html}')
        
        # 3. Aggiungi JS (prima di </body>)
        js_script = '<script src="/static/js/chatbot.js"></script>'
        if 'chatbot.js' not in content:
            content = content.replace('</body>', f'    {js_script}\n</body>')
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ Installato in: {html_path.name}")
        return True
    
    def install_all(self):
        """Installa in tutte le pagine"""
        print("\n📄 Installazione nelle pagine...")
        
        pages = [
            self.templates_dir / 'index.html',
            self.templates_dir / 'en' / 'index.html',
            self.templates_dir / 'es' / 'index.html',
            self.templates_dir / 'ru' / 'index.html',
            self.templates_dir / 'zh' / 'index.html'
        ]
        
        installed = 0
        for page in pages:
            if self.install_in_page(page):
                installed += 1
        
        print(f"\n✅ Installato in {installed} pagine!")
        return installed

    def get_chatbot_html(self):
        return '''<!-- CHATBOT -->
<div class="chatbot-container">
    <div class="chatbot-window" id="chatbotWindow">
        <div class="chatbot-header">
            <span class="chatbot-title">🤖 Assistente Attico Roma</span>
            <button class="chatbot-close-btn" id="chatbotCloseBtn">✕</button>
        </div>
        <div class="chatbot-messages" id="chatbotMessages">
            <div class="msg bot">
                <div class="msg-avatar">🤖</div>
                <div class="msg-content">
                    Ciao! Sono il tuo assistente virtuale.<br>
                    Chiedimi tutto sull'attico, Roma, ristoranti e mezzi di trasporto! 🏛️
                </div>
            </div>
        </div>
        <div class="chatbot-input-area">
            <input type="text" id="chatbotInput" placeholder="Scrivi la tua domanda..." class="chatbot-input">
            <button id="chatbotSendBtn" class="chatbot-send-btn">➤</button>
        </div>
    </div>
    <button class="chatbot-toggle-btn" id="chatbotToggleBtn">
        <span class="robot-icon">🤖</span>
        <span class="pulse-ring"></span>
    </button>
</div>'''

    def get_chatbot_css(self):
        return '''/* CHATBOT UNICO */
.chatbot-container {
    position: fixed;
    bottom: 30px;
    right: 30px;
    z-index: 9999;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
}
.chatbot-window {
    display: none;
    width: 370px;
    max-width: 90vw;
    height: 480px;
    max-height: 65vh;
    background: #fff;
    border-radius: 18px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    flex-direction: column;
    overflow: hidden;
    margin-bottom: 12px;
    animation: slideUp 0.3s ease;
}
.chatbot-window.open { display: flex; }
@keyframes slideUp {
    from { opacity: 0; transform: translateY(20px) scale(0.95); }
    to { opacity: 1; transform: translateY(0) scale(1); }
}
.chatbot-header {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: #fff;
    padding: 14px 18px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-shrink: 0;
}
.chatbot-title { font-weight: 600; font-size: 15px; }
.chatbot-close-btn {
    background: rgba(255,255,255,0.2);
    border: none;
    color: #fff;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    cursor: pointer;
    font-size: 16px;
    transition: background 0.3s;
}
.chatbot-close-btn:hover { background: rgba(255,255,255,0.3); }
.chatbot-messages {
    flex: 1;
    padding: 14px 16px;
    overflow-y: auto;
    background: #f5f6fa;
}
.chatbot-messages::-webkit-scrollbar { width: 4px; }
.chatbot-messages::-webkit-scrollbar-thumb { background: #ccc; border-radius: 10px; }
.msg {
    display: flex;
    gap: 10px;
    margin-bottom: 12px;
    animation: msgIn 0.3s ease;
}
@keyframes msgIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}
.msg.bot { justify-content: flex-start; }
.msg.user { justify-content: flex-end; }
.msg-avatar {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea, #764ba2);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
    flex-shrink: 0;
}
.msg-content {
    max-width: 78%;
    padding: 10px 14px;
    border-radius: 14px;
    font-size: 14px;
    line-height: 1.5;
    word-wrap: break-word;
}
.msg.bot .msg-content {
    background: #fff;
    color: #333;
    border-radius: 14px 14px 14px 4px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
}
.msg.user .msg-content {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: #fff;
    border-radius: 14px 14px 4px 14px;
}
.chatbot-input-area {
    padding: 10px 14px;
    background: #fff;
    border-top: 1px solid #eee;
    display: flex;
    gap: 8px;
    flex-shrink: 0;
}
.chatbot-input {
    flex: 1;
    padding: 10px 14px;
    border: 2px solid #e8e8e8;
    border-radius: 10px;
    font-size: 14px;
    outline: none;
    transition: border-color 0.3s;
}
.chatbot-input:focus { border-color: #667eea; }
.chatbot-send-btn {
    width: 42px;
    height: 42px;
    border: none;
    border-radius: 10px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: #fff;
    font-size: 18px;
    cursor: pointer;
    transition: transform 0.2s;
    flex-shrink: 0;
}
.chatbot-send-btn:hover { transform: scale(1.05); }
.chatbot-toggle-btn {
    width: 62px;
    height: 62px;
    border-radius: 50%;
    background: linear-gradient(135deg, #667eea, #764ba2);
    border: none;
    cursor: pointer;
    box-shadow: 0 6px 25px rgba(102,126,234,0.5);
    transition: transform 0.3s;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
}
.chatbot-toggle-btn:hover { transform: scale(1.08); }
.robot-icon {
    font-size: 30px;
    animation: jump 1.8s ease-in-out infinite;
}
@keyframes jump {
    0%, 100% { transform: translateY(0) rotate(0deg); }
    30% { transform: translateY(-14px) rotate(-6deg); }
    50% { transform: translateY(-8px) rotate(6deg); }
    70% { transform: translateY(-14px) rotate(-6deg); }
}
.pulse-ring {
    position: absolute;
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background: rgba(102,126,234,0.3);
    animation: ring 2.5s ease-out infinite;
    top: 0;
    left: 0;
}
@keyframes ring {
    0% { transform: scale(1); opacity: 0.7; }
    100% { transform: scale(1.7); opacity: 0; }
}
@media (max-width: 768px) {
    .chatbot-container { bottom: 20px; right: 16px; }
    .chatbot-window { width: 92vw; height: 55vh; position: fixed; bottom: 85px; right: 10px; }
    .chatbot-toggle-btn { width: 54px; height: 54px; }
    .robot-icon { font-size: 26px; }
}
@media (max-width: 480px) {
    .chatbot-container { bottom: 15px; right: 12px; }
    .chatbot-window { width: 95vw; height: 50vh; bottom: 75px; right: 8px; }
    .chatbot-toggle-btn { width: 48px; height: 48px; }
    .robot-icon { font-size: 22px; }
}'''

    def get_chatbot_js(self):
        return '''// CHATBOT FUNZIONANTE
(function() {
    "use strict";
    
    var KB = {
        it: {
            'prezzo': 'Il prezzo è €120 a notte. Sconto del 10% se prenoti direttamente!',
            'quanto costa': 'Il prezzo è €120 a notte. Sconto del 10% se prenoti direttamente!',
            'ospiti': 'L\'attico può ospitare fino a 3 persone.',
            'camere': 'L\'attico ha 2 camere da letto, un bagno e soggiorno con cucina.',
            'wi-fi': 'Sì, abbiamo Wi-Fi veloce in tutto l\'attico.',
            'aria condizionata': 'Sì, l\'attico è dotato di aria condizionata.',
            'cucina': 'La cucina è completamente attrezzata.',
            'lavatrice': 'Sì, c\'è una lavatrice.',
            'parcheggio': 'Il parcheggio è gratuito.',
            'check-in': 'Check-in flessibile, istruzioni via email.',
            'colosseo': 'Il Colosseo si raggiunge in 20 minuti di autobus.',
            'piazza navona': 'Piazza Navona è a 30 minuti a piedi.',
            'trastevere': 'Trastevere è a 15 minuti con i mezzi.',
            'vaticano': 'Il Vaticano è a 30 minuti con i mezzi.',
            'metropolitana': 'Metro: Laurentina (Linea B).',
            'bus': 'La fermata dell\'autobus è a 5 minuti a piedi.',
            'taxi': 'Taxi: 06 3570 o app FreeNow.',
            'ristorante': 'Osteria Sanmarzano a 5 minuti a piedi.',
            'mangiare': 'Osteria Sanmarzano a 5 minuti a piedi.',
            'emergenza': 'Emergenza: 112',
            'ciao': 'Ciao! Come posso aiutarti? 🏠',
            'grazie': 'Grazie a te! 😊'
        },
        en: {
            'price': 'The price is €120 per night. 10% discount if you book directly!',
            'how much': 'The price is €120 per night. 10% discount if you book directly!',
            'guests': 'The penthouse can accommodate up to 3 people.',
            'rooms': 'The penthouse has 2 bedrooms, 1 bathroom and a living room with kitchen.',
            'wi-fi': 'Yes, we have fast Wi-Fi throughout the penthouse.',
            'air conditioning': 'Yes, the penthouse has air conditioning.',
            'kitchen': 'The kitchen is fully equipped.',
            'washing machine': 'Yes, there is a washing machine.',
            'parking': 'Parking is free.',
            'check-in': 'Flexible check-in, instructions via email.',
            'colosseum': 'The Colosseum is 20 minutes away by bus.',
            'piazza navona': 'Piazza Navona is 30 minutes on foot.',
            'trastevere': 'Trastevere is 15 minutes by public transport.',
            'vatican': 'The Vatican is 30 minutes by public transport.',
            'metro': 'Metro: Laurentina (Line B).',
            'bus': 'The bus stop is 5 minutes walk away.',
            'taxi': 'Taxi: 06 3570 or FreeNow app.',
            'restaurant': 'Osteria Sanmarzano is 5 minutes walk away.',
            'eat': 'Osteria Sanmarzano is 5 minutes walk away.',
            'emergency': 'Emergency: 112',
            'hello': 'Hello! How can I help you? 🏠',
            'thanks': 'Thank you! 😊'
        },
        es: {
            'precio': 'El precio es €120 por noche. ¡10% de descuento si reservas directamente!',
            'cuanto cuesta': 'El precio es €120 por noche. ¡10% de descuento si reservas directamente!',
            'huéspedes': 'El ático puede alojar hasta 3 personas.',
            'habitaciones': 'El ático tiene 2 dormitorios, 1 baño y salón con cocina.',
            'wi-fi': 'Sí, tenemos Wi-Fi rápido en todo el ático.',
            'aire acondicionado': 'Sí, el ático tiene aire acondicionado.',
            'cocina': 'La cocina está totalmente equipada.',
            'lavadora': 'Sí, hay lavadora.',
            'aparcamiento': 'El aparcamiento es gratuito.',
            'check-in': 'Check-in flexible, instrucciones por email.',
            'coliseo': 'El Coliseo está a 20 minutos en autobús.',
            'piazza navona': 'Piazza Navona está a 30 minutos a pie.',
            'trastevere': 'Trastevere está a 15 minutos en transporte público.',
            'vaticano': 'El Vaticano está a 30 minutos en transporte público.',
            'metro': 'Metro: Laurentina (Línea B).',
            'autobús': 'La parada de autobús está a 5 minutos a pie.',
            'taxi': 'Taxi: 06 3570 o app FreeNow.',
            'restaurante': 'Osteria Sanmarzano a 5 minutos a pie.',
            'comer': 'Osteria Sanmarzano a 5 minutos a pie.',
            'emergencia': 'Emergencia: 112',
            'hola': '¡Hola! ¿Cómo puedo ayudarte? 🏠',
            'gracias': '¡Gracias a ti! 😊'
        },
        ru: {
            'цена': 'Цена €120 за ночь. Скидка 10% при бронировании напрямую!',
            'сколько стоит': 'Цена €120 за ночь. Скидка 10% при бронировании напрямую!',
            'гости': 'Пентхаус может разместить до 3 человек.',
            'комнаты': 'В пентхаусе 2 спальни, 1 ванная и гостиная с кухней.',
            'wi-fi': 'Да, у нас быстрый Wi-Fi во всем пентхаусе.',
            'кондиционер': 'Да, в пентхаусе есть кондиционер.',
            'кухня': 'Кухня полностью оборудована.',
            'стиральная машина': 'Да, есть стиральная машина.',
            'парковка': 'Парковка бесплатная.',
            'заезд': 'Гибкий заезд, инструкции по email.',
            'колизей': 'Колизей в 20 минутах на автобусе.',
            'пьяцца навона': 'Пьяцца Навона в 30 минутах пешком.',
            'трастевере': 'Трастевере в 15 минутах на транспорте.',
            'ватикан': 'Ватикан в 30 минутах на транспорте.',
            'метро': 'Метро: Laurentina (Линия B).',
            'автобус': 'Остановка автобуса в 5 минутах ходьбы.',
            'такси': 'Такси: 06 3570 или приложение FreeNow.',
            'ресторан': 'Osteria Sanmarzano в 5 минутах ходьбы.',
            'есть': 'Osteria Sanmarzano в 5 минутах ходьбы.',
            'экстренная': 'Экстренная помощь: 112',
            'привет': 'Привет! Чем я могу помочь? 🏠',
            'спасибо': 'Спасибо! 😊'
        },
        zh: {
            '价格': '每晚€120。直接预订可享9折优惠！',
            '多少钱': '每晚€120。直接预订可享9折优惠！',
            '住客': '顶层公寓可容纳最多3人。',
            '房间': '顶层公寓有2间卧室、1间浴室和带厨房的客厅。',
            'wi-fi': '是的，整个顶层公寓都有高速Wi-Fi。',
            '空调': '是的，顶层公寓有空调。',
            '厨房': '厨房设备齐全。',
            '洗衣机': '是的，有洗衣机。',
            '停车': '停车免费。',
            '入住': '灵活入住，通过电子邮件发送说明。',
            '斗兽场': '斗兽场乘坐巴士20分钟可达。',
            '纳沃纳广场': '纳沃纳广场步行30分钟。',
            '特拉斯提弗列': '特拉斯提弗列乘坐公共交通15分钟。',
            '梵蒂冈': '梵蒂冈乘坐公共交通30分钟。',
            '地铁': '地铁：Laurentina（B线）。',
            '巴士': '巴士站步行5分钟。',
            '出租车': '出租车：06 3570或FreeNow应用。',
            '餐厅': 'Osteria Sanmarzano步行5分钟。',
            '吃饭': 'Osteria Sanmarzano步行5分钟。',
            '紧急': '紧急电话：112',
            '你好': '你好！我能帮你什么？ 🏠',
            '谢谢': '谢谢！ 😊'
        }
    };
    
    var toggleBtn = document.getElementById('chatbotToggleBtn');
    var windowEl = document.getElementById('chatbotWindow');
    var closeBtn = document.getElementById('chatbotCloseBtn');
    var sendBtn = document.getElementById('chatbotSendBtn');
    var input = document.getElementById('chatbotInput');
    var messages = document.getElementById('chatbotMessages');
    
    if (!toggleBtn || !windowEl) {
        console.error('Elementi chatbot non trovati!');
        return;
    }
    
    var isOpen = false;
    
    function getLang() {
        var htmlLang = document.documentElement.lang || 'it';
        var map = { 'it':'it', 'en':'en', 'es':'es', 'ru':'ru', 'zh':'zh', 'zh-Hans':'zh', 'zh-CN':'zh' };
        return map[htmlLang] || 'it';
    }
    
    function getTranslations(lang) {
        return KB[lang] || KB.it || {};
    }
    
    function toggleChat() {
        isOpen = !isOpen;
        windowEl.classList.toggle('open', isOpen);
        if (isOpen) {
            setTimeout(function() { input.focus(); }, 200);
        }
    }
    
    function addMessage(text, sender) {
        var div = document.createElement('div');
        div.className = 'msg ' + sender;
        if (sender === 'bot') {
            div.innerHTML = '<div class="msg-avatar">🤖</div><div class="msg-content">' + text + '</div>';
        } else {
            div.innerHTML = '<div class="msg-content">' + text + '</div>';
        }
        messages.appendChild(div);
        messages.scrollTop = messages.scrollHeight;
    }
    
    function findAnswer(question) {
        var q = question.toLowerCase().trim();
        var lang = getLang();
        var t = getTranslations(lang);
        
        for (var key in t) {
            if (q.indexOf(key) !== -1 || key.indexOf(q) !== -1) {
                return t[key];
            }
        }
        
        var fallback = {
            'it': 'Non ho capito. Posso aiutarti su: prezzo, servizi, trasporti, ristoranti. 😊',
            'en': 'I didn\'t understand. I can help with: price, services, transport, restaurants. 😊',
            'es': 'No entendí. Puedo ayudarte con: precio, servicios, transporte, restaurantes. 😊',
            'ru': 'Я не понял. Я могу помочь с: цена, услуги, транспорт, рестораны. 😊',
            'zh': '我没明白。我可以帮你：价格、服务、交通、餐厅。😊'
        };
        return fallback[lang] || fallback.it;
    }
    
    function sendMessage() {
        var text = input.value.trim();
        if (!text) return;
        
        addMessage(text, 'user');
        input.value = '';
        
        var typing = document.createElement('div');
        typing.className = 'msg bot';
        typing.id = 'typingIndicator';
        typing.innerHTML = '<div class="msg-avatar">🤖</div><div class="msg-content" style="font-size:12px;color:#999;">Sto pensando...</div>';
        messages.appendChild(typing);
        messages.scrollTop = messages.scrollHeight;
        
        setTimeout(function() {
            var el = document.getElementById('typingIndicator');
            if (el) el.remove();
            var answer = findAnswer(text);
            addMessage(answer, 'bot');
        }, 600 + Math.random() * 400);
    }
    
    toggleBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        toggleChat();
    });
    
    closeBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        toggleChat();
    });
    
    sendBtn.addEventListener('click', sendMessage);
    
    input.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    document.addEventListener('click', function(e) {
        if (isOpen) {
            var container = document.querySelector('.chatbot-container');
            if (container && !container.contains(e.target)) {
                toggleChat();
            }
        }
    });
    
    console.log('🤖 Chatbot attivo! Lingua:', getLang());
})();'''

    def install(self):
        """Esegue l'installazione"""
        print("="*60)
        print("🤖 INSTALLAZIONE CHATBOT")
        print("="*60)
        
        self.clean_everything()
        self.create_chatbot_files()
        self.install_all()
        
        print("\n" + "="*60)
        print("✅ INSTALLAZIONE COMPLETATA!")
        print("="*60)
        print("\n📁 File creati:")
        print("  ✅ static/js/chatbot.js")
        print("  ✅ static/css/chatbot.css")
        print("\n📄 PAGINE MODIFICATE (TUTTE le lingue):")
        print("  ✅ templates/index.html (italiano)")
        print("  ✅ templates/en/index.html (inglese)")
        print("  ✅ templates/es/index.html (spagnolo)")
        print("  ✅ templates/ru/index.html (russo)")
        print("  ✅ templates/zh/index.html (cinese)")
        print("\n🤖 UN SOLO robottino in basso a destra!")
        print("="*60)


if __name__ == '__main__':
    import sys
    source_path = Path(__file__).parent
    installer = ChatbotInstaller(source_path)
    installer.install()