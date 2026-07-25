// CHATBOT CON GOOGLE GEMINI - VERSIONE PER LOCALHOST (CON PROXY)
(function() {
    "use strict";
    
    // ============================================
    // CONFIGURAZIONE
    // ============================================
    const GEMINI_API_KEY = 'AIzaSyB_vcVb52oV4HsqX1hSP_B2ixTrklyAnac';
    const GEMINI_MODEL = 'gemini-2.5-flash';
    
    // Usa un proxy CORS gratuito per localhost
    // ATTENZIONE: Da usare SOLO per sviluppo!
    const CORS_PROXY = 'https://cors-anywhere.herokuapp.com/';
    const USE_PROXY = true; // Metti false quando sei su PythonAnywhere
    
    // ============================================
    // KNOWLEDGE BASE LOCALE (FALLBACK)
    // ============================================
    var KB = {
        it: {
            'prezzo': 'Il prezzo è €120 a notte. Sconto del 10% se prenoti direttamente!',
            'quanto costa': 'Il prezzo è €120 a notte. Sconto del 10% se prenoti direttamente!',
            'costa': 'Il prezzo è €120 a notte. 10% di sconto se prenoti dal sito!',
            'ospiti': 'L\'attico può ospitare fino a 3 persone.',
            'persone': 'L\'attico può ospitare fino a 3 persone.',
            'camere': 'L\'attico ha 2 camere da letto, un bagno e un ampio soggiorno con cucina.',
            'letti': 'Ci sono 3 letti: un letto matrimoniale e due letti singoli.',
            'wi-fi': 'Sì, abbiamo Wi-Fi veloce in tutto l\'attico!',
            'wifi': 'Sì, abbiamo Wi-Fi veloce in tutto l\'attico!',
            'aria condizionata': 'Sì, l\'attico è dotato di aria condizionata.',
            'cucina': 'La cucina è completamente attrezzata.',
            'lavatrice': 'Sì, c\'è una lavatrice.',
            'parcheggio': 'Sì, il parcheggio è gratuito!',
            'parking': 'Sì, il parcheggio è gratuito!',
            'tv': 'Sì, c\'è una TV a schermo piatto.',
            'ascensore': 'Sì, l\'edificio ha un ascensore.',
            'animali': 'Purtroppo non sono ammessi animali domestici.',
            'fumare': 'Non è consentito fumare all\'interno.',
            'check-in': 'Check-in flessibile. Istruzioni via email il giorno prima.',
            'checkin': 'Check-in flessibile. Istruzioni via email.',
            'check-out': 'Check-out entro le 10:00. Possiamo essere flessibili.',
            'checkout': 'Check-out entro le 10:00.',
            'ciao': 'Ciao! Come posso aiutarti? 🏠',
            'grazie': 'Grazie a te! 😊',
            'colosseo': 'Il Colosseo si raggiunge in 20 minuti di autobus (linea 714) o in metro Linea B fino a Colosseo.',
            'centro': 'Prendi la metro Linea B da Laurentina. In 15 minuti sei a Termini, il cuore di Roma.',
            'metro': 'La fermata della metro più vicina è Laurentina (Linea B). Da lì in 15 minuti sei a Termini.',
            'bus': 'Autobus 714, 780, 716. Fermata a 5 minuti a piedi.',
            'taxi': 'Taxi: 06 3570 o app FreeNow. Per andare in centro circa €20-25.',
            'ristorante': 'Osteria Sanmarzano a 5 minuti a piedi. Cucina romana tradizionale. Super consigliato!',
            'emergenza': 'Emergenza: 112'
        },
        en: {
            'price': 'The price is €120 per night. 10% discount if you book directly!',
            'how much': 'The price is €120 per night. 10% discount if you book directly!',
            'guests': 'The penthouse can accommodate up to 3 people.',
            'rooms': '2 bedrooms, 1 bathroom and a living room with kitchen.',
            'wi-fi': 'Yes, we have fast Wi-Fi!',
            'parking': 'Parking is free!',
            'check-in': 'Flexible check-in. Instructions via email.',
            'check-out': 'Check-out by 10:00 am.',
            'city center': 'Take metro Line B from Laurentina. In 15 minutes you are at Termini.',
            'metro': 'The nearest metro is Laurentina (Line B). 15 minutes to Termini.',
            'bus': 'Buses 714, 780, 716. Stop 5 minutes walk.',
            'taxi': 'Taxi: 06 3570 or FreeNow app. About €20-25 to the center.',
            'restaurant': 'Osteria Sanmarzano is 5 minutes walk away. Traditional Roman cuisine.',
            'emergency': 'Emergency: 112',
            'hello': 'Hello! How can I help you? 🏠',
            'thanks': 'Thank you! 😊'
        },
        es: {
            'precio': 'El precio es €120 por noche. ¡10% de descuento si reservas directamente!',
            'cuanto cuesta': 'El precio es €120 por noche. ¡10% de descuento!',
            'huéspedes': 'El ático puede alojar hasta 3 personas.',
            'centro': 'Toma el metro Línea B desde Laurentina. En 15 minutos estás en Termini.',
            'restaurante': 'Osteria Sanmarzano a 5 minutos a pie. Cocina romana tradicional.',
            'emergencia': 'Emergencia: 112',
            'hola': '¡Hola! ¿Cómo puedo ayudarte? 🏠',
            'gracias': '¡Gracias a ti! 😊'
        },
        ru: {
            'цена': 'Цена €120 за ночь. Скидка 10% при бронировании напрямую!',
            'сколько стоит': 'Цена €120 за ночь. Скидка 10%!',
            'гости': 'Пентхаус может разместить до 3 человек.',
            'центр': 'Метро Линия B от Laurentina. Через 15 минут вы в Термини.',
            'ресторан': 'Osteria Sanmarzano в 5 минутах ходьбы. Традиционная римская кухня.',
            'экстренная': 'Экстренная помощь: 112',
            'привет': 'Привет! Чем я могу помочь? 🏠',
            'спасибо': 'Спасибо! 😊'
        },
        zh: {
            '价格': '每晚€120。直接预订可享9折优惠！',
            '多少钱': '每晚€120。直接预订可享9折优惠！',
            '住客': '顶层公寓可容纳最多3人。',
            '中心': '乘坐地铁B线从Laurentina出发。15分钟到达Termini。',
            '餐厅': 'Osteria Sanmarzano步行5分钟。传统罗马美食。',
            '紧急': '紧急电话：112',
            '你好': '你好！我能帮你什么？ 🏠',
            '谢谢': '谢谢！ 😊'
        }
    };
    
    // ============================================
    // ELEMENTI DOM
    // ============================================
    var toggleBtn = document.getElementById('chatbotToggleBtn');
    var windowEl = document.getElementById('chatbotWindow');
    var closeBtn = document.getElementById('chatbotCloseBtn');
    var sendBtn = document.getElementById('chatbotSendBtn');
    var input = document.getElementById('chatbotInput');
    var messages = document.getElementById('chatbotMessages');
    
    if (!toggleBtn || !windowEl) {
        console.error('❌ Elementi chatbot non trovati!');
        return;
    }
    
    var isOpen = false;
    var isProcessing = false;
    var apiWorking = false;
    
    // ============================================
    // FUNZIONI BASE
    // ============================================
    
    function getLang() {
        var htmlLang = document.documentElement.lang || 'it';
        var map = { 'it':'it', 'en':'en', 'es':'es', 'ru':'ru', 'zh':'zh', 'zh-Hans':'zh', 'zh-CN':'zh' };
        return map[htmlLang] || 'it';
    }
    
    function toggleChat() {
        isOpen = !isOpen;
        if (isOpen) {
            windowEl.style.display = 'flex';
            windowEl.classList.add('open');
            setTimeout(function() { if (input) input.focus(); }, 300);
        } else {
            windowEl.style.display = 'none';
            windowEl.classList.remove('open');
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
    
    function findLocalAnswer(question) {
        var q = question.toLowerCase().trim();
        var lang = getLang();
        var t = KB[lang] || KB.it || {};
        for (var key in t) {
            if (q.indexOf(key) !== -1 || key.indexOf(q) !== -1) {
                return t[key];
            }
        }
        return null;
    }
    
    // ============================================
    // GOOGLE GEMINI CON PROXY PER LOCALHOST
    // ============================================
    async function askGemini(question) {
        try {
            var lang = getLang();
            
            var systemPrompt = {
                'it': `Sei un assistente per un attico vacanze a Roma. Rispondi in italiano, amichevole e conciso. Massimo 4 frasi.
                Info: Prezzo €120/notte, sconto 10% se prenotano dal sito. Max 3 ospiti. 2 camere, 1 bagno, cucina attrezzata.
                Servizi: Wi-Fi, aria condizionata, lavatrice, parcheggio gratuito, TV, ascensore. Check-in flessibile. Check-out 10:00.
                Posizione: Via Guido Ascoli, EUR, Roma. Metro Laurentina (Linea B) a 10 min. Autobus 714,780,716 a 5 min.
                Attrazioni: Colosseo (20 min bus), Piazza Navona (30 min), Trastevere (15 min), Vaticano (30 min).
                Ristorante: Osteria Sanmarzano a 5 min. Emergenza: 112.`,
                'en': `You are an assistant for a penthouse in Rome. Answer in English, friendly and concise. Max 4 sentences.
                Info: Price €120/night, 10% discount. Max 3 guests. 2 bedrooms, 1 bathroom, kitchen.
                Services: Wi-Fi, AC, washing machine, free parking, TV, elevator. Flexible check-in. Check-out 10:00.
                Location: Via Guido Ascoli, EUR, Rome. Metro Laurentina (Line B) 10 min walk. Buses 714,780,716.
                Attractions: Colosseum (20 min bus), Piazza Navona (30 min), Trastevere (15 min), Vatican (30 min).
                Restaurant: Osteria Sanmarzano 5 min walk. Emergency: 112.`,
                'es': `Eres un asistente para un ático en Roma. Responde en español, amable y conciso. Máximo 4 frases.
                Info: Precio €120/noche, 10% descuento. Máx 3 huéspedes. 2 dormitorios, 1 baño, cocina.
                Servicios: Wi-Fi, AC, lavadora, parking gratis, TV, ascensor. Check-in flexible. Check-out 10:00.
                Ubicación: Via Guido Ascoli, EUR, Roma. Metro Laurentina (Línea B) 10 min. Autobuses 714,780,716.
                Atracciones: Coliseo (20 min bus), Piazza Navona (30 min), Trastevere (15 min), Vaticano (30 min).
                Restaurante: Osteria Sanmarzano 5 min. Emergencia: 112.`,
                'ru': `Вы ассистент для пентхауса в Риме. Отвечайте на русском, дружелюбно и кратко. Максимум 4 предложения.
                Информация: Цена €120/ночь, скидка 10%. Макс 3 гостя. 2 спальни, 1 ванная, кухня.
                Услуги: Wi-Fi, кондиционер, стиральная машина, парковка, ТВ, лифт. Гибкий заезд. Выезд 10:00.
                Адрес: Via Guido Ascoli, EUR, Рим. Метро Laurentina (Линия B) 10 мин. Автобусы 714,780,716.
                Достопримечательности: Колизей (20 мин автобус), Пьяцца Навона (30 мин), Трастевере (15 мин), Ватикан (30 мин).
                Ресторан: Osteria Sanmarzano 5 мин. Экстренная помощь: 112.`,
                'zh': `您是罗马顶层公寓的助手。用中文回答，友好简洁。最多4句话。
                信息：价格€120/晚，9折优惠。最多3位住客。2间卧室，1间浴室，厨房。
                服务：Wi-Fi、空调、洗衣机、免费停车、电视、电梯。灵活入住。退房10:00。
                地址：Via Guido Ascoli, EUR, 罗马。地铁Laurentina（B线）步行10分钟。巴士714,780,716。
                景点：斗兽场（巴士20分钟）、纳沃纳广场（30分钟）、特拉斯提弗列（15分钟）、梵蒂冈（30分钟）。
                餐厅：Osteria Sanmarzano步行5分钟。紧急电话：112。`
            };
            
            var prompt = systemPrompt[lang] || systemPrompt.it;
            var fullPrompt = prompt + '\n\nDOMANDA: ' + question + '\n\nRISPOSTA:';
            
            var url;
            if (USE_PROXY) {
                // Usa proxy CORS per localhost
                url = CORS_PROXY + 'https://generativelanguage.googleapis.com/v1beta/models/' + GEMINI_MODEL + ':generateContent?key=' + GEMINI_API_KEY;
            } else {
                url = 'https://generativelanguage.googleapis.com/v1beta/models/' + GEMINI_MODEL + ':generateContent?key=' + GEMINI_API_KEY;
            }
            
            console.log('🤖 Chiamata Gemini via proxy...');
            
            var response = await fetch(url, {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Origin': window.location.origin
                },
                body: JSON.stringify({
                    contents: [{ parts: [{ text: fullPrompt }] }]
                })
            });
            
            if (!response.ok) {
                console.error('❌ Errore Gemini:', response.status);
                return null;
            }
            
            var data = await response.json();
            
            if (data.candidates && data.candidates[0] && data.candidates[0].content) {
                var answer = data.candidates[0].content.parts[0].text;
                answer = answer.replace(/\*\*/g, '').replace(/#/g, '').replace(/\n/g, ' ').trim();
                return answer;
            }
            
            return null;
            
        } catch (error) {
            console.error('❌ Errore Gemini:', error);
            return null;
        }
    }
    
    // ============================================
    // SEND MESSAGE
    // ============================================
    async function sendMessage() {
        var text = input.value.trim();
        if (!text || isProcessing) return;
        
        isProcessing = true;
        addMessage(text, 'user');
        input.value = '';
        
        var typing = document.createElement('div');
        typing.className = 'msg bot';
        typing.id = 'typingIndicator';
        typing.innerHTML = '<div class="msg-avatar">🤖</div><div class="msg-content" style="font-size:12px;color:#999;">🧠 Sto pensando...</div>';
        messages.appendChild(typing);
        messages.scrollTop = messages.scrollHeight;
        
        try {
            var answer = null;
            
            // Prova Gemini (con proxy se necessario)
            if (USE_PROXY) {
                console.log('🔄 Usando proxy CORS per localhost...');
            }
            answer = await askGemini(text);
            
            var el = document.getElementById('typingIndicator');
            if (el) el.remove();
            
            if (answer) {
                addMessage(answer, 'bot');
                console.log('✅ Risposta da Gemini');
            } else {
                // Fallback knowledge base
                var localAnswer = findLocalAnswer(text);
                if (localAnswer) {
                    addMessage(localAnswer, 'bot');
                    console.log('📚 Risposta locale');
                } else {
                    var fallback = {
                        'it': 'Non ho capito. Posso aiutarti su: prezzo, servizi, trasporti, ristoranti. 😊',
                        'en': 'I didn\'t understand. I can help with: price, services, transport, restaurants. 😊',
                        'es': 'No entendí. Puedo ayudarte con: precio, servicios, transporte, restaurantes. 😊',
                        'ru': 'Я не понял. Я могу помочь с: цена, услуги, транспорт, рестораны. 😊',
                        'zh': '我没明白。我可以帮你：价格、服务、交通、餐厅。😊'
                    };
                    addMessage(fallback[getLang()] || fallback.it, 'bot');
                }
            }
        } catch (error) {
            var el = document.getElementById('typingIndicator');
            if (el) el.remove();
            console.error('❌ Errore:', error);
            addMessage('Scusa, c\'è stato un problema. Riprova! 😊', 'bot');
        }
        
        isProcessing = false;
    }
    
    // ============================================
    // EVENTI
    // ============================================
    toggleBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        e.preventDefault();
        toggleChat();
    });
    
    if (closeBtn) {
        closeBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            e.preventDefault();
            toggleChat();
        });
    }
    
    if (sendBtn) {
        sendBtn.addEventListener('click', function(e) {
            e.preventDefault();
            sendMessage();
        });
    }
    
    if (input) {
        input.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                sendMessage();
            }
        });
    }
    
    document.addEventListener('click', function(e) {
        if (isOpen) {
            var container = document.querySelector('.chatbot-container');
            if (container && !container.contains(e.target)) {
                toggleChat();
            }
        }
    });
    
    // ============================================
    // AVVIO
    // ============================================
    console.log('🤖 Chatbot con Google Gemini');
    console.log('═══════════════════════════════════');
    if (USE_PROXY) {
        console.log('🔄 Modalità LOCALHOST con proxy CORS');
        console.log('⚠️ Il proxy è gratuito e ha limiti di chiamate');
        console.log('📌 Carica su PythonAnywhere per usare Gemini senza proxy');
    } else {
        console.log('✅ Modalità PRODUZIONE (senza proxy)');
    }
    console.log('💡 Clicca sul robottino 🤖 per aprire la chat!');
    console.log('═══════════════════════════════════');
    
})();