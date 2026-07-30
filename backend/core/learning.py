"""Learning content: guided tutorial + child-friendly Markdown reference.

Markdown syntax is the same in every language, so the ``syntax`` and
``example`` fields are language-neutral and defined once. Only the human
text (labels, hints, titles, bodies) is translated. English is the fallback
for any unknown language.

Pure Python / stdlib only, mirroring :mod:`backend.core.i18n`.
"""

import re
from typing import Dict, List, Optional, Tuple

DEFAULT_LANGUAGE = "en"

# ---------------------------------------------------------------------------
# Markdown quick reference (6 kid-friendly items, fixed display order)
# ---------------------------------------------------------------------------

_MARKDOWN_ITEMS: List[str] = ["heading", "bold", "italic", "image", "choice", "list"]

_MARKDOWN_SYNTAX: Dict[str, str] = {
    "heading": "# My Story",
    "bold": "**brave**",
    "italic": "*whisper*",
    "image": "![cat](images/cat.png)",
    "choice": "[[Open the door]]",
    "list": "- a sword\n- a map",
}

_MARKDOWN_EXAMPLE: Dict[str, str] = {
    "heading": "# The Brave Knight",
    "bold": "She was **very brave**.",
    "italic": "He *whispered* softly.",
    "image": "![A dragon](images/dragon.png)",
    "choice": "[[Enter the dark cave]]",
    "list": "- a shiny sword\n- an old map",
}

# Per-language (label, hint) for every Markdown item id.
_MARKDOWN_TEXT: Dict[str, Dict[str, Tuple[str, str]]] = {
    "en": {
        "heading": ("Big title", "Start a line with # to make a title."),
        "bold": ("Bold words", "Wrap words in ** to make them strong."),
        "italic": ("Slanted words", "Wrap words in * to make them lean."),
        "image": ("Add a picture", "Use ![name](images/file.png) to show a picture."),
        "choice": ("A choice", "Write [[your choice]] so readers can pick."),
        "list": ("A list", "Start lines with - to make a list."),
    },
    "nl": {
        "heading": ("Grote titel", "Begin een regel met # om een titel te maken."),
        "bold": ("Vette woorden", "Zet woorden tussen ** om ze vet te maken."),
        "italic": ("Schuine woorden", "Zet woorden tussen * om ze schuin te maken."),
        "image": ("Voeg een plaatje toe", "Gebruik ![naam](images/bestand.png) om een plaatje te tonen."),
        "choice": ("Een keuze", "Schrijf [[jouw keuze]] zodat lezers kunnen kiezen."),
        "list": ("Een lijstje", "Begin regels met - om een lijstje te maken."),
    },
    "it": {
        "heading": ("Titolo grande", "Inizia una riga con # per fare un titolo."),
        "bold": ("Parole in grassetto", "Metti le parole tra ** per renderle forti."),
        "italic": ("Parole in corsivo", "Metti le parole tra * per renderle in corsivo."),
        "image": ("Aggiungi un'immagine", "Usa ![nome](images/file.png) per mostrare un'immagine."),
        "choice": ("Una scelta", "Scrivi [[la tua scelta]] per far scegliere i lettori."),
        "list": ("Un elenco", "Inizia le righe con - per fare un elenco."),
    },
    "es": {
        "heading": ("Título grande", "Empieza una línea con # para hacer un título."),
        "bold": ("Palabras en negrita", "Pon palabras entre ** para hacerlas fuertes."),
        "italic": ("Palabras inclinadas", "Pon palabras entre * para inclinarlas."),
        "image": ("Añade una imagen", "Usa ![nombre](images/archivo.png) para mostrar una imagen."),
        "choice": ("Una opción", "Escribe [[tu opción]] para que los lectores elijan."),
        "list": ("Una lista", "Empieza líneas con - para hacer una lista."),
    },
    "fr": {
        "heading": ("Grand titre", "Commence une ligne par # pour faire un titre."),
        "bold": ("Mots en gras", "Mets les mots entre ** pour les rendre gras."),
        "italic": ("Mots penchés", "Mets les mots entre * pour les pencher."),
        "image": ("Ajoute une image", "Utilise ![nom](images/fichier.png) pour montrer une image."),
        "choice": ("Un choix", "Écris [[ton choix]] pour laisser les lecteurs choisir."),
        "list": ("Une liste", "Commence les lignes par - pour faire une liste."),
    },
    "pt": {
        "heading": ("Título grande", "Começa uma linha com # para fazer um título."),
        "bold": ("Palavras em negrito", "Põe palavras entre ** para deixá-las fortes."),
        "italic": ("Palavras inclinadas", "Põe palavras entre * para incliná-las."),
        "image": ("Adiciona uma imagem", "Usa ![nome](images/ficheiro.png) para mostrar uma imagem."),
        "choice": ("Uma escolha", "Escreve [[a tua escolha]] para os leitores escolherem."),
        "list": ("Uma lista", "Começa as linhas com - para fazer uma lista."),
    },
    "de": {
        "heading": ("Große Überschrift", "Beginne eine Zeile mit #, um eine Überschrift zu machen."),
        "bold": ("Fette Wörter", "Setze Wörter zwischen **, um sie fett zu machen."),
        "italic": ("Schräge Wörter", "Setze Wörter zwischen *, um sie schräg zu machen."),
        "image": ("Bild hinzufügen", "Nutze ![Name](images/datei.png), um ein Bild zu zeigen."),
        "choice": ("Eine Wahl", "Schreibe [[deine Wahl]], damit Leser wählen können."),
        "list": ("Eine Liste", "Beginne Zeilen mit -, um eine Liste zu machen."),
    },
    "ru": {
        "heading": ("Большой заголовок", "Начни строку с #, чтобы сделать заголовок."),
        "bold": ("Жирные слова", "Помести слова между **, чтобы сделать их жирными."),
        "italic": ("Наклонные слова", "Помести слова между *, чтобы сделать их наклонными."),
        "image": ("Добавь картинку", "Используй ![имя](images/файл.png), чтобы показать картинку."),
        "choice": ("Выбор", "Напиши [[твой выбор]], чтобы читатели могли выбирать."),
        "list": ("Список", "Начинай строки с -, чтобы сделать список."),
    },
    "zh": {
        "heading": ("大标题", "用 # 开头来做一个标题。"),
        "bold": ("粗体字", "把文字放在 ** 之间，让它变粗。"),
        "italic": ("斜体字", "把文字放在 * 之间，让它变斜。"),
        "image": ("加一张图片", "用 ![名字](images/文件.png) 来显示图片。"),
        "choice": ("一个选择", "写 [[你的选择]]，让读者来选。"),
        "list": ("一个列表", "用 - 开头来做一个列表。"),
    },
    "hi": {
        "heading": ("बड़ा शीर्षक", "शीर्षक बनाने के लिए लाइन को # से शुरू करें।"),
        "bold": ("मोटे शब्द", "शब्दों को ** के बीच रखें ताकि वे मोटे हो जाएँ।"),
        "italic": ("तिरछे शब्द", "शब्दों को * के बीच रखें ताकि वे तिरछे हो जाएँ।"),
        "image": ("एक तस्वीर जोड़ें", "तस्वीर दिखाने के लिए ![नाम](images/file.png) का उपयोग करें।"),
        "choice": ("एक विकल्प", "पाठकों को चुनने देने के लिए [[आपका विकल्प]] लिखें।"),
        "list": ("एक सूची", "सूची बनाने के लिए लाइनों को - से शुरू करें।"),
    },
    "ar": {
        "heading": ("عنوان كبير", "ابدأ السطر بـ # لعمل عنوان."),
        "bold": ("كلمات عريضة", "ضع الكلمات بين ** لجعلها عريضة."),
        "italic": ("كلمات مائلة", "ضع الكلمات بين * لجعلها مائلة."),
        "image": ("أضف صورة", "استخدم ![اسم](images/file.png) لعرض صورة."),
        "choice": ("اختيار", "اكتب [[اختيارك]] ليختار القرّاء."),
        "list": ("قائمة", "ابدأ الأسطر بـ - لعمل قائمة."),
    },
    "bn": {
        "heading": ("বড় শিরোনাম", "শিরোনাম বানাতে লাইন # দিয়ে শুরু করো।"),
        "bold": ("মোটা শব্দ", "শব্দগুলো ** এর মাঝে রাখো যাতে মোটা হয়।"),
        "italic": ("তির্যক শব্দ", "শব্দগুলো * এর মাঝে রাখো যাতে বাঁকা হয়।"),
        "image": ("একটি ছবি যোগ করো", "ছবি দেখাতে ![নাম](images/file.png) ব্যবহার করো।"),
        "choice": ("একটি পছন্দ", "পাঠকদের বেছে নিতে দিতে [[তোমার পছন্দ]] লেখো।"),
        "list": ("একটি তালিকা", "তালিকা বানাতে লাইনগুলো - দিয়ে শুরু করো।"),
    },
    "ur": {
        "heading": ("بڑا عنوان", "عنوان بنانے کے لیے سطر کو # سے شروع کریں۔"),
        "bold": ("موٹے الفاظ", "الفاظ کو ** کے درمیان رکھیں تاکہ وہ موٹے ہو جائیں۔"),
        "italic": ("ترچھے الفاظ", "الفاظ کو * کے درمیان رکھیں تاکہ وہ ترچھے ہو جائیں۔"),
        "image": ("ایک تصویر شامل کریں", "تصویر دکھانے کے لیے ![نام](images/file.png) استعمال کریں۔"),
        "choice": ("ایک انتخاب", "قارئین کو منتخب کرنے دینے کے لیے [[آپ کا انتخاب]] لکھیں۔"),
        "list": ("ایک فہرست", "فہرست بنانے کے لیے سطریں - سے شروع کریں۔"),
    },
    "id": {
        "heading": ("Judul besar", "Mulai baris dengan # untuk membuat judul."),
        "bold": ("Kata tebal", "Apit kata dengan ** agar menjadi tebal."),
        "italic": ("Kata miring", "Apit kata dengan * agar menjadi miring."),
        "image": ("Tambahkan gambar", "Gunakan ![nama](images/file.png) untuk menampilkan gambar."),
        "choice": ("Sebuah pilihan", "Tulis [[pilihanmu]] agar pembaca bisa memilih."),
        "list": ("Sebuah daftar", "Mulai baris dengan - untuk membuat daftar."),
    },
    "bg": {
        "heading": ("Голямо заглавие", "Започни ред с #, за да направиш заглавие."),
        "bold": ("Удебелени думи", "Постави думите между **, за да станат удебелени."),
        "italic": ("Наклонени думи", "Постави думите между *, за да станат наклонени."),
        "image": ("Добави картинка", "Използвай ![име](images/file.png), за да покажеш картинка."),
        "choice": ("Избор", "Напиши [[твоят избор]], за да могат читателите да избират."),
        "list": ("Списък", "Започвай редовете с -, за да направиш списък."),
    },
}

# ---------------------------------------------------------------------------
# Guided tutorial (5 short micro-lessons, fixed order)
# ---------------------------------------------------------------------------

_TUTORIAL_STEPS: List[str] = ["heading", "style", "image", "choice", "play"]

_TUTORIAL_EXAMPLE: Dict[str, str] = {
    "heading": "# My Adventure",
    "style": "You feel **brave** but a little *scared*.",
    "image": "![A castle](images/castle.png)",
    "choice": "[[Enter the cave]]",
    "play": "# Start\n[[Go to the forest]]\n\n# Go to the forest\nYou see tall trees.",
}

# Per-language (title, body) for every tutorial step id.
_TUTORIAL_TEXT: Dict[str, Dict[str, Tuple[str, str]]] = {
    "en": {
        "heading": ("Give your story a title", "Every story starts with a title. Type # and your title."),
        "style": ("Make words fun", "Use ** for bold and * for slanted words to add feelings."),
        "image": ("Add a picture", "Show a picture with ![name](images/file.png)."),
        "choice": ("Let readers choose", "Add [[a choice]] so readers decide what happens next."),
        "play": ("Compile and play", "Press Compile, then Play to read your adventure!"),
    },
    "nl": {
        "heading": ("Geef je verhaal een titel", "Elk verhaal begint met een titel. Typ # en je titel."),
        "style": ("Maak woorden leuk", "Gebruik ** voor vet en * voor schuin om gevoel toe te voegen."),
        "image": ("Voeg een plaatje toe", "Laat een plaatje zien met ![naam](images/bestand.png)."),
        "choice": ("Laat lezers kiezen", "Voeg [[een keuze]] toe zodat lezers beslissen wat er gebeurt."),
        "play": ("Compileren en spelen", "Druk op Compileren en dan op Spelen om je avontuur te lezen!"),
    },
    "it": {
        "heading": ("Dai un titolo alla storia", "Ogni storia inizia con un titolo. Scrivi # e il titolo."),
        "style": ("Rendi le parole divertenti", "Usa ** per il grassetto e * per il corsivo per aggiungere emozioni."),
        "image": ("Aggiungi un'immagine", "Mostra un'immagine con ![nome](images/file.png)."),
        "choice": ("Fai scegliere i lettori", "Aggiungi [[una scelta]] così i lettori decidono cosa succede."),
        "play": ("Compila e gioca", "Premi Compila e poi Gioca per leggere la tua avventura!"),
    },
    "es": {
        "heading": ("Dale un título a tu historia", "Cada historia empieza con un título. Escribe # y tu título."),
        "style": ("Haz las palabras divertidas", "Usa ** para negrita y * para cursiva y añadir emociones."),
        "image": ("Añade una imagen", "Muestra una imagen con ![nombre](images/archivo.png)."),
        "choice": ("Deja elegir a los lectores", "Añade [[una opción]] para que los lectores decidan qué pasa."),
        "play": ("Compila y juega", "¡Pulsa Compilar y luego Jugar para leer tu aventura!"),
    },
    "fr": {
        "heading": ("Donne un titre à ton histoire", "Chaque histoire commence par un titre. Tape # et ton titre."),
        "style": ("Rends les mots amusants", "Utilise ** pour le gras et * pour l'italique pour ajouter des émotions."),
        "image": ("Ajoute une image", "Montre une image avec ![nom](images/fichier.png)."),
        "choice": ("Laisse les lecteurs choisir", "Ajoute [[un choix]] pour que les lecteurs décident de la suite."),
        "play": ("Compile et joue", "Appuie sur Compiler puis Jouer pour lire ton aventure !"),
    },
    "pt": {
        "heading": ("Dá um título à tua história", "Cada história começa com um título. Escreve # e o teu título."),
        "style": ("Torna as palavras divertidas", "Usa ** para negrito e * para itálico para dar emoção."),
        "image": ("Adiciona uma imagem", "Mostra uma imagem com ![nome](images/ficheiro.png)."),
        "choice": ("Deixa os leitores escolher", "Adiciona [[uma escolha]] para os leitores decidirem o que acontece."),
        "play": ("Compila e joga", "Carrega em Compilar e depois Jogar para ler a tua aventura!"),
    },
    "de": {
        "heading": ("Gib deiner Geschichte einen Titel", "Jede Geschichte beginnt mit einem Titel. Tippe # und deinen Titel."),
        "style": ("Mach Wörter lustig", "Nutze ** für fett und * für schräg, um Gefühle hinzuzufügen."),
        "image": ("Bild hinzufügen", "Zeige ein Bild mit ![Name](images/datei.png)."),
        "choice": ("Lass Leser wählen", "Füge [[eine Wahl]] hinzu, damit Leser entscheiden, was passiert."),
        "play": ("Kompilieren und spielen", "Drücke Kompilieren und dann Spielen, um dein Abenteuer zu lesen!"),
    },
    "ru": {
        "heading": ("Дай истории название", "Каждая история начинается с заголовка. Напиши # и название."),
        "style": ("Сделай слова весёлыми", "Используй ** для жирного и * для наклонного, чтобы добавить чувства."),
        "image": ("Добавь картинку", "Покажи картинку с помощью ![имя](images/файл.png)."),
        "choice": ("Пусть читатели выбирают", "Добавь [[выбор]], чтобы читатели решали, что будет дальше."),
        "play": ("Собери и играй", "Нажми Собрать, затем Играть, чтобы прочитать своё приключение!"),
    },
    "zh": {
        "heading": ("给你的故事起个标题", "每个故事都从标题开始。输入 # 和你的标题。"),
        "style": ("让文字变有趣", "用 ** 变粗，用 * 变斜，加入感情。"),
        "image": ("加一张图片", "用 ![名字](images/文件.png) 显示一张图片。"),
        "choice": ("让读者来选择", "加上 [[一个选择]]，让读者决定接下来发生什么。"),
        "play": ("编译并游玩", "按“编译”，再按“游玩”，来读你的冒险！"),
    },
    "hi": {
        "heading": ("अपनी कहानी को एक शीर्षक दें", "हर कहानी एक शीर्षक से शुरू होती है। # और अपना शीर्षक लिखें।"),
        "style": ("शब्दों को मज़ेदार बनाएँ", "भावनाएँ जोड़ने के लिए ** से मोटा और * से तिरछा करें।"),
        "image": ("एक तस्वीर जोड़ें", "![नाम](images/file.png) से एक तस्वीर दिखाएँ।"),
        "choice": ("पाठकों को चुनने दें", "[[एक विकल्प]] जोड़ें ताकि पाठक तय करें कि आगे क्या हो।"),
        "play": ("कंपाइल करें और खेलें", "अपना रोमांच पढ़ने के लिए कंपाइल दबाएँ, फिर खेलें!"),
    },
    "ar": {
        "heading": ("أعطِ قصتك عنوانًا", "كل قصة تبدأ بعنوان. اكتب # ثم عنوانك."),
        "style": ("اجعل الكلمات ممتعة", "استخدم ** للعريض و * للمائل لإضافة المشاعر."),
        "image": ("أضف صورة", "اعرض صورة باستخدام ![اسم](images/file.png)."),
        "choice": ("دع القرّاء يختارون", "أضف [[اختيارًا]] ليقرر القرّاء ما يحدث بعد ذلك."),
        "play": ("جمّع والعب", "اضغط جمّع ثم العب لتقرأ مغامرتك!"),
    },
    "bn": {
        "heading": ("তোমার গল্পকে একটি শিরোনাম দাও", "প্রতিটি গল্প শিরোনাম দিয়ে শুরু হয়। # আর তোমার শিরোনাম লেখো।"),
        "style": ("শব্দগুলো মজার করো", "অনুভূতি যোগ করতে ** দিয়ে মোটা আর * দিয়ে বাঁকা করো।"),
        "image": ("একটি ছবি যোগ করো", "![নাম](images/file.png) দিয়ে একটি ছবি দেখাও।"),
        "choice": ("পাঠকদের বেছে নিতে দাও", "[[একটি পছন্দ]] যোগ করো যাতে পাঠকরা ঠিক করে এরপর কী হবে।"),
        "play": ("কম্পাইল করো আর খেলো", "তোমার অ্যাডভেঞ্চার পড়তে কম্পাইল চাপো, তারপর খেলো!"),
    },
    "ur": {
        "heading": ("اپنی کہانی کو ایک عنوان دیں", "ہر کہانی ایک عنوان سے شروع ہوتی ہے۔ # اور اپنا عنوان لکھیں۔"),
        "style": ("الفاظ کو مزیدار بنائیں", "احساسات شامل کرنے کے لیے ** سے موٹا اور * سے ترچھا کریں۔"),
        "image": ("ایک تصویر شامل کریں", "![نام](images/file.png) سے ایک تصویر دکھائیں۔"),
        "choice": ("قارئین کو منتخب کرنے دیں", "[[ایک انتخاب]] شامل کریں تاکہ قارئین فیصلہ کریں کہ آگے کیا ہو۔"),
        "play": ("کمپائل کریں اور کھیلیں", "اپنی مہم پڑھنے کے لیے کمپائل دبائیں، پھر کھیلیں!"),
    },
    "id": {
        "heading": ("Beri judul ceritamu", "Setiap cerita dimulai dengan judul. Ketik # dan judulmu."),
        "style": ("Buat kata jadi seru", "Gunakan ** untuk tebal dan * untuk miring agar menambah perasaan."),
        "image": ("Tambahkan gambar", "Tampilkan gambar dengan ![nama](images/file.png)."),
        "choice": ("Biarkan pembaca memilih", "Tambahkan [[sebuah pilihan]] agar pembaca menentukan apa yang terjadi."),
        "play": ("Kompilasi dan mainkan", "Tekan Kompilasi lalu Mainkan untuk membaca petualanganmu!"),
    },
    "bg": {
        "heading": ("Дай заглавие на историята си", "Всяка история започва със заглавие. Напиши # и своето заглавие."),
        "style": ("Направи думите забавни", "Използвай ** за удебелено и * за наклонено, за да добавиш чувства."),
        "image": ("Добави картинка", "Покажи картинка с ![име](images/file.png)."),
        "choice": ("Остави читателите да избират", "Добави [[избор]], за да решават читателите какво става после."),
        "play": ("Компилирай и играй", "Натисни Компилирай, после Играй, за да прочетеш приключението си!"),
    },
}


# ---------------------------------------------------------------------------
# UI chrome labels (localized so no client string is left in English)
# ---------------------------------------------------------------------------

# Per-language (tutorial_cta, tutorial_heading, tutorial_done, help_summary,
# badges_label).
_UI_TEXT: Dict[str, Tuple[str, str, str, str, str]] = {
    "en": ("Show me how", "How to make a story", "Got it!", "Markdown help", "Badges earned"),
    "nl": ("Laat me zien", "Hoe maak je een verhaal", "Begrepen!", "Markdown-hulp", "Verdiende badges"),
    "it": ("Mostrami come", "Come creare una storia", "Capito!", "Aiuto Markdown", "Distintivi ottenuti"),
    "es": ("Muéstrame cómo", "Cómo crear una historia", "¡Entendido!", "Ayuda de Markdown", "Insignias ganadas"),
    "fr": ("Montre-moi", "Comment faire une histoire", "Compris !", "Aide Markdown", "Badges gagnés"),
    "pt": ("Mostra-me como", "Como criar uma história", "Percebi!", "Ajuda Markdown", "Emblemas ganhos"),
    "de": ("Zeig mir wie", "So machst du eine Geschichte", "Verstanden!", "Markdown-Hilfe", "Verdiente Abzeichen"),
    "ru": ("Покажи мне", "Как создать историю", "Понятно!", "Помощь по Markdown", "Полученные значки"),
    "zh": ("教我怎么做", "如何创作故事", "明白了！", "Markdown 帮助", "获得的徽章"),
    "hi": ("मुझे दिखाओ", "कहानी कैसे बनाएँ", "समझ गया!", "Markdown मदद", "अर्जित बैज"),
    "ar": ("أرِني كيف", "كيف تصنع قصة", "فهمت!", "مساعدة Markdown", "الأوسمة المكتسبة"),
    "bn": ("আমাকে দেখাও", "কীভাবে গল্প বানাবে", "বুঝেছি!", "Markdown সাহায্য", "অর্জিত ব্যাজ"),
    "ur": ("مجھے دکھائیں", "کہانی کیسے بنائیں", "سمجھ گیا!", "Markdown مدد", "حاصل کردہ بیجز"),
    "id": ("Tunjukkan caranya", "Cara membuat cerita", "Mengerti!", "Bantuan Markdown", "Lencana diperoleh"),
    "bg": ("Покажи ми как", "Как да направиш история", "Разбрах!", "Помощ за Markdown", "Спечелени значки"),
}


def get_ui_labels(lang: str) -> Dict[str, str]:
    """Return localized UI chrome labels for the learning features."""
    cta, heading, done, summary, badges = _UI_TEXT.get(lang, _UI_TEXT[DEFAULT_LANGUAGE])
    return {
        "tutorial_cta": cta,
        "tutorial_heading": heading,
        "tutorial_done": done,
        "help_summary": summary,
        "badges_label": badges,
    }


def get_markdown_help(lang: str) -> List[Dict[str, str]]:
    """Return the 6-item Markdown quick reference for a language.

    Falls back to English for unknown languages.
    """
    text = _MARKDOWN_TEXT.get(lang, _MARKDOWN_TEXT[DEFAULT_LANGUAGE])
    return [
        {
            "id": item_id,
            "label": text[item_id][0],
            "hint": text[item_id][1],
            "syntax": _MARKDOWN_SYNTAX[item_id],
            "example": _MARKDOWN_EXAMPLE[item_id],
        }
        for item_id in _MARKDOWN_ITEMS
    ]


def get_tutorial(lang: str) -> List[Dict[str, object]]:
    """Return the 5-step guided tutorial for a language.

    Falls back to English for unknown languages.
    """
    text = _TUTORIAL_TEXT.get(lang, _TUTORIAL_TEXT[DEFAULT_LANGUAGE])
    return [
        {
            "step": index + 1,
            "title": text[step_id][0],
            "body": text[step_id][1],
            "example": _TUTORIAL_EXAMPLE[step_id],
        }
        for index, step_id in enumerate(_TUTORIAL_STEPS)
    ]


# ---------------------------------------------------------------------------
# Child-friendly validation hints
# ---------------------------------------------------------------------------
#
# The compiler/validator emit precise but technical messages. We recognise the
# known ones and turn them into plain-language, actionable hints (what's wrong,
# which page, and one thing to try) localized for every supported language.
# The raw message is always kept alongside the hint, so nothing is lost.

# Each pattern maps a raw validator/compiler message to a hint ``kind`` and the
# ordered capture groups it exposes as ``{section}`` / ``{target}`` / ``{header}``.
_HINT_PATTERNS: List[Tuple[str, str, Tuple[str, ...]]] = [
    (
        "broken_choice",
        r"^Section '([^']+)' has choice pointing to non-existent section '([^']+)'",
        ("section", "target"),
    ),
    ("orphaned", r"^Section '([^']+)' is unreachable", ("section",)),
    ("missing_start", r"^Start section '([^']+)' does not exist", ("section",)),
    ("empty", r"^Story content is empty", ()),
    ("no_metadata", r"^No metadata block found", ()),
    ("no_title", r"^Metadata must include 'title' field", ()),
    ("no_sections", r"^No sections found in story", ()),
    ("bad_header", r"^Invalid section header: (.+?)\. Expected", ("header",)),
    ("duplicate", r"^Duplicate section name \(duplicate\): (.+)$", ("section",)),
]

# Per-language template for every hint kind. Placeholders: {section}, {target},
# {header}. Falls back to English for unknown languages.
_HINT_TEXT: Dict[str, Dict[str, str]] = {
    "en": {
        "broken_choice": "The page '{section}' has a choice that goes to '{target}', but that page doesn't exist yet. Make a page called '{target}', or fix the choice.",
        "orphaned": "No choice leads to the page '{section}', so readers can't reach it. Add a [[choice]] to it from another page.",
        "missing_start": "Your story starts at '{section}', but there's no page with that name. Fix the start name or add that page.",
        "empty": "Your story is empty. Add a title and a first page to begin!",
        "no_metadata": "Every story needs a title block at the top. Put your title between two --- lines.",
        "no_title": "Your story needs a title. Add a line like 'title: My Story' at the top.",
        "no_sections": "Your story has no pages yet. Add a page like [[start]] with some words.",
        "bad_header": "A page name should look like [[start]]. Check this line: '{header}'.",
        "duplicate": "Two pages are named '{section}'. Give each page its own name.",
    },
    "nl": {
        "broken_choice": "De pagina '{section}' heeft een keuze naar '{target}', maar die pagina bestaat nog niet. Maak een pagina '{target}' of pas de keuze aan.",
        "orphaned": "Geen enkele keuze leidt naar de pagina '{section}', dus lezers komen er niet. Voeg ergens een [[keuze]] ernaartoe toe.",
        "missing_start": "Je verhaal begint bij '{section}', maar die pagina bestaat niet. Pas de startnaam aan of maak die pagina.",
        "empty": "Je verhaal is leeg. Voeg een titel en een eerste pagina toe om te beginnen!",
        "no_metadata": "Elk verhaal heeft bovenaan een titelblok nodig. Zet je titel tussen twee --- regels.",
        "no_title": "Je verhaal heeft een titel nodig. Voeg bovenaan een regel toe zoals 'title: Mijn verhaal'.",
        "no_sections": "Je verhaal heeft nog geen pagina's. Voeg een pagina toe zoals [[start]] met wat woorden.",
        "bad_header": "Een paginanaam ziet eruit als [[start]]. Controleer deze regel: '{header}'.",
        "duplicate": "Twee pagina's heten '{section}'. Geef elke pagina een eigen naam.",
    },
    "it": {
        "broken_choice": "La pagina '{section}' ha una scelta verso '{target}', ma quella pagina non esiste ancora. Crea una pagina '{target}' o correggi la scelta.",
        "orphaned": "Nessuna scelta porta alla pagina '{section}', così i lettori non possono arrivarci. Aggiungi una [[scelta]] verso di essa da un'altra pagina.",
        "missing_start": "La tua storia inizia da '{section}', ma non c'è nessuna pagina con quel nome. Correggi il nome iniziale o crea quella pagina.",
        "empty": "La tua storia è vuota. Aggiungi un titolo e una prima pagina per iniziare!",
        "no_metadata": "Ogni storia ha bisogno di un blocco del titolo in alto. Metti il titolo tra due righe ---.",
        "no_title": "La tua storia ha bisogno di un titolo. Aggiungi in alto una riga come 'title: La mia storia'.",
        "no_sections": "La tua storia non ha ancora pagine. Aggiungi una pagina come [[inizio]] con qualche parola.",
        "bad_header": "Il nome di una pagina è tipo [[inizio]]. Controlla questa riga: '{header}'.",
        "duplicate": "Due pagine si chiamano '{section}'. Dai a ogni pagina un nome diverso.",
    },
    "es": {
        "broken_choice": "La página '{section}' tiene una opción hacia '{target}', pero esa página aún no existe. Crea una página '{target}' o corrige la opción.",
        "orphaned": "Ninguna opción lleva a la página '{section}', así que los lectores no pueden llegar. Añade una [[opción]] hacia ella desde otra página.",
        "missing_start": "Tu historia empieza en '{section}', pero no hay ninguna página con ese nombre. Corrige el nombre de inicio o crea esa página.",
        "empty": "Tu historia está vacía. ¡Añade un título y una primera página para empezar!",
        "no_metadata": "Cada historia necesita un bloque de título arriba. Pon tu título entre dos líneas ---.",
        "no_title": "Tu historia necesita un título. Añade arriba una línea como 'title: Mi historia'.",
        "no_sections": "Tu historia todavía no tiene páginas. Añade una página como [[inicio]] con algunas palabras.",
        "bad_header": "El nombre de una página es como [[inicio]]. Revisa esta línea: '{header}'.",
        "duplicate": "Dos páginas se llaman '{section}'. Dale a cada página su propio nombre.",
    },
    "fr": {
        "broken_choice": "La page '{section}' a un choix vers '{target}', mais cette page n'existe pas encore. Crée une page '{target}' ou corrige le choix.",
        "orphaned": "Aucun choix ne mène à la page '{section}', donc les lecteurs ne peuvent pas y aller. Ajoute un [[choix]] vers elle depuis une autre page.",
        "missing_start": "Ton histoire commence à '{section}', mais aucune page ne porte ce nom. Corrige le nom de départ ou crée cette page.",
        "empty": "Ton histoire est vide. Ajoute un titre et une première page pour commencer !",
        "no_metadata": "Chaque histoire a besoin d'un bloc de titre en haut. Mets ton titre entre deux lignes ---.",
        "no_title": "Ton histoire a besoin d'un titre. Ajoute en haut une ligne comme 'title: Mon histoire'.",
        "no_sections": "Ton histoire n'a pas encore de pages. Ajoute une page comme [[debut]] avec quelques mots.",
        "bad_header": "Un nom de page ressemble à [[debut]]. Vérifie cette ligne : '{header}'.",
        "duplicate": "Deux pages s'appellent '{section}'. Donne à chaque page son propre nom.",
    },
    "pt": {
        "broken_choice": "A página '{section}' tem uma escolha para '{target}', mas essa página ainda não existe. Cria uma página '{target}' ou corrige a escolha.",
        "orphaned": "Nenhuma escolha leva à página '{section}', por isso os leitores não conseguem chegar. Adiciona uma [[escolha]] para ela a partir de outra página.",
        "missing_start": "A tua história começa em '{section}', mas não há nenhuma página com esse nome. Corrige o nome inicial ou cria essa página.",
        "empty": "A tua história está vazia. Adiciona um título e uma primeira página para começar!",
        "no_metadata": "Cada história precisa de um bloco de título no topo. Põe o teu título entre duas linhas ---.",
        "no_title": "A tua história precisa de um título. Adiciona no topo uma linha como 'title: A minha história'.",
        "no_sections": "A tua história ainda não tem páginas. Adiciona uma página como [[inicio]] com algumas palavras.",
        "bad_header": "O nome de uma página é como [[inicio]]. Verifica esta linha: '{header}'.",
        "duplicate": "Duas páginas chamam-se '{section}'. Dá a cada página o seu próprio nome.",
    },
    "de": {
        "broken_choice": "Die Seite '{section}' hat eine Wahl zu '{target}', aber diese Seite gibt es noch nicht. Erstelle eine Seite '{target}' oder ändere die Wahl.",
        "orphaned": "Keine Wahl führt zur Seite '{section}', deshalb können Leser sie nicht erreichen. Füge von einer anderen Seite eine [[Wahl]] dorthin hinzu.",
        "missing_start": "Deine Geschichte beginnt bei '{section}', aber es gibt keine Seite mit diesem Namen. Ändere den Startnamen oder erstelle die Seite.",
        "empty": "Deine Geschichte ist leer. Füge einen Titel und eine erste Seite hinzu, um zu beginnen!",
        "no_metadata": "Jede Geschichte braucht oben einen Titelblock. Setze deinen Titel zwischen zwei --- Zeilen.",
        "no_title": "Deine Geschichte braucht einen Titel. Füge oben eine Zeile wie 'title: Meine Geschichte' hinzu.",
        "no_sections": "Deine Geschichte hat noch keine Seiten. Füge eine Seite wie [[start]] mit ein paar Wörtern hinzu.",
        "bad_header": "Ein Seitenname sieht aus wie [[start]]. Prüfe diese Zeile: '{header}'.",
        "duplicate": "Zwei Seiten heißen '{section}'. Gib jeder Seite einen eigenen Namen.",
    },
    "ru": {
        "broken_choice": "На странице '{section}' есть выбор к '{target}', но такой страницы ещё нет. Создай страницу '{target}' или исправь выбор.",
        "orphaned": "Ни один выбор не ведёт к странице '{section}', поэтому читатели не смогут её найти. Добавь [[выбор]] к ней с другой страницы.",
        "missing_start": "Твоя история начинается со страницы '{section}', но такой страницы нет. Исправь имя начала или создай эту страницу.",
        "empty": "Твоя история пустая. Добавь заголовок и первую страницу, чтобы начать!",
        "no_metadata": "Каждой истории нужен блок заголовка сверху. Помести заголовок между двумя строками ---.",
        "no_title": "Твоей истории нужен заголовок. Добавь сверху строку вроде 'title: Моя история'.",
        "no_sections": "В твоей истории пока нет страниц. Добавь страницу вроде [[start]] с несколькими словами.",
        "bad_header": "Имя страницы выглядит как [[start]]. Проверь эту строку: '{header}'.",
        "duplicate": "Две страницы называются '{section}'. Дай каждой странице своё имя.",
    },
    "zh": {
        "broken_choice": "页面 '{section}' 有一个通往 '{target}' 的选择，但那个页面还不存在。请创建一个 '{target}' 页面，或修改这个选择。",
        "orphaned": "没有任何选择通向页面 '{section}'，所以读者到不了那里。请在别的页面里加一个通向它的 [[选择]]。",
        "missing_start": "你的故事从 '{section}' 开始，但没有这个名字的页面。请修改开始的名字，或创建那个页面。",
        "empty": "你的故事是空的。加一个标题和第一个页面就能开始啦！",
        "no_metadata": "每个故事顶部都需要一个标题块。把标题放在两行 --- 之间。",
        "no_title": "你的故事需要一个标题。在顶部加一行，比如 'title: 我的故事'。",
        "no_sections": "你的故事还没有页面。加一个像 [[开始]] 的页面，再写点文字。",
        "bad_header": "页面名字应该像 [[开始]] 这样。检查这一行：'{header}'。",
        "duplicate": "有两个页面都叫 '{section}'。给每个页面起一个不同的名字。",
    },
    "hi": {
        "broken_choice": "पेज '{section}' में '{target}' की ओर एक विकल्प है, पर वह पेज अभी नहीं है। '{target}' नाम का पेज बनाएँ या विकल्प ठीक करें।",
        "orphaned": "कोई विकल्प पेज '{section}' तक नहीं ले जाता, इसलिए पाठक वहाँ नहीं पहुँच सकते। किसी दूसरे पेज से उस तक एक [[विकल्प]] जोड़ें।",
        "missing_start": "आपकी कहानी '{section}' से शुरू होती है, पर उस नाम का कोई पेज नहीं है। शुरू का नाम ठीक करें या वह पेज बनाएँ।",
        "empty": "आपकी कहानी खाली है। शुरू करने के लिए एक शीर्षक और पहला पेज जोड़ें!",
        "no_metadata": "हर कहानी को ऊपर एक शीर्षक ब्लॉक चाहिए। अपना शीर्षक दो --- लाइनों के बीच रखें।",
        "no_title": "आपकी कहानी को एक शीर्षक चाहिए। ऊपर एक लाइन जोड़ें जैसे 'title: मेरी कहानी'।",
        "no_sections": "आपकी कहानी में अभी कोई पेज नहीं है। [[start]] जैसा एक पेज कुछ शब्दों के साथ जोड़ें।",
        "bad_header": "पेज का नाम [[start]] जैसा दिखना चाहिए। इस लाइन को देखें: '{header}'।",
        "duplicate": "दो पेज का नाम '{section}' है। हर पेज को अलग नाम दें।",
    },
    "ar": {
        "broken_choice": "الصفحة '{section}' فيها اختيار نحو '{target}'، لكن تلك الصفحة غير موجودة بعد. أنشئ صفحة اسمها '{target}' أو صحّح الاختيار.",
        "orphaned": "لا يوجد اختيار يؤدي إلى الصفحة '{section}'، لذلك لا يستطيع القرّاء الوصول إليها. أضف [[اختيارًا]] نحوها من صفحة أخرى.",
        "missing_start": "قصتك تبدأ من '{section}'، لكن لا توجد صفحة بهذا الاسم. صحّح اسم البداية أو أنشئ تلك الصفحة.",
        "empty": "قصتك فارغة. أضف عنوانًا وصفحة أولى لتبدأ!",
        "no_metadata": "كل قصة تحتاج إلى كتلة عنوان في الأعلى. ضع عنوانك بين سطرين ---.",
        "no_title": "قصتك تحتاج إلى عنوان. أضف في الأعلى سطرًا مثل 'title: قصتي'.",
        "no_sections": "قصتك ليس فيها صفحات بعد. أضف صفحة مثل [[start]] مع بعض الكلمات.",
        "bad_header": "اسم الصفحة يجب أن يكون مثل [[start]]. تحقق من هذا السطر: '{header}'.",
        "duplicate": "صفحتان بالاسم '{section}'. أعطِ كل صفحة اسمًا مختلفًا.",
    },
    "bn": {
        "broken_choice": "'{section}' পেজে '{target}' এর দিকে একটি পছন্দ আছে, কিন্তু সেই পেজ এখনও নেই। '{target}' নামে একটি পেজ বানাও বা পছন্দটি ঠিক করো।",
        "orphaned": "কোনো পছন্দ '{section}' পেজে নিয়ে যায় না, তাই পাঠকরা সেখানে পৌঁছাতে পারে না। অন্য পেজ থেকে সেটির দিকে একটি [[পছন্দ]] যোগ করো।",
        "missing_start": "তোমার গল্প '{section}' থেকে শুরু হয়, কিন্তু সেই নামে কোনো পেজ নেই। শুরুর নাম ঠিক করো বা সেই পেজ বানাও।",
        "empty": "তোমার গল্প খালি। শুরু করতে একটি শিরোনাম আর প্রথম পেজ যোগ করো!",
        "no_metadata": "প্রতিটি গল্পের উপরে একটি শিরোনাম ব্লক দরকার। তোমার শিরোনাম দুটি --- লাইনের মাঝে রাখো।",
        "no_title": "তোমার গল্পের একটি শিরোনাম দরকার। উপরে একটি লাইন যোগ করো যেমন 'title: আমার গল্প'।",
        "no_sections": "তোমার গল্পে এখনও কোনো পেজ নেই। কিছু শব্দ দিয়ে [[start]] এর মতো একটি পেজ যোগ করো।",
        "bad_header": "পেজের নাম [[start]] এর মতো হওয়া উচিত। এই লাইনটি দেখো: '{header}'।",
        "duplicate": "দুটি পেজের নাম '{section}'। প্রতিটি পেজকে আলাদা নাম দাও।",
    },
    "ur": {
        "broken_choice": "صفحہ '{section}' میں '{target}' کی طرف ایک انتخاب ہے، لیکن وہ صفحہ ابھی موجود نہیں۔ '{target}' نام کا صفحہ بنائیں یا انتخاب درست کریں۔",
        "orphaned": "کوئی انتخاب صفحہ '{section}' تک نہیں لے جاتا، اس لیے قارئین وہاں نہیں پہنچ سکتے۔ کسی اور صفحے سے اس کی طرف ایک [[انتخاب]] شامل کریں۔",
        "missing_start": "آپ کی کہانی '{section}' سے شروع ہوتی ہے، لیکن اس نام کا کوئی صفحہ نہیں۔ شروع کا نام درست کریں یا وہ صفحہ بنائیں۔",
        "empty": "آپ کی کہانی خالی ہے۔ شروع کرنے کے لیے ایک عنوان اور پہلا صفحہ شامل کریں!",
        "no_metadata": "ہر کہانی کو اوپر ایک عنوان بلاک چاہیے۔ اپنا عنوان دو --- لائنوں کے درمیان رکھیں۔",
        "no_title": "آپ کی کہانی کو ایک عنوان چاہیے۔ اوپر ایک لائن شامل کریں جیسے 'title: میری کہانی'۔",
        "no_sections": "آپ کی کہانی میں ابھی کوئی صفحہ نہیں۔ کچھ الفاظ کے ساتھ [[start]] جیسا ایک صفحہ شامل کریں۔",
        "bad_header": "صفحے کا نام [[start]] جیسا ہونا چاہیے۔ اس لائن کو دیکھیں: '{header}'۔",
        "duplicate": "دو صفحوں کا نام '{section}' ہے۔ ہر صفحے کو الگ نام دیں۔",
    },
    "id": {
        "broken_choice": "Halaman '{section}' punya pilihan menuju '{target}', tetapi halaman itu belum ada. Buat halaman '{target}' atau perbaiki pilihannya.",
        "orphaned": "Tidak ada pilihan yang menuju halaman '{section}', jadi pembaca tidak bisa sampai. Tambahkan [[pilihan]] ke sana dari halaman lain.",
        "missing_start": "Ceritamu dimulai di '{section}', tetapi tidak ada halaman dengan nama itu. Perbaiki nama awal atau buat halaman itu.",
        "empty": "Ceritamu kosong. Tambahkan judul dan halaman pertama untuk memulai!",
        "no_metadata": "Setiap cerita perlu blok judul di atas. Letakkan judulmu di antara dua baris ---.",
        "no_title": "Ceritamu perlu judul. Tambahkan baris di atas seperti 'title: Ceritaku'.",
        "no_sections": "Ceritamu belum punya halaman. Tambahkan halaman seperti [[start]] dengan beberapa kata.",
        "bad_header": "Nama halaman seperti [[start]]. Periksa baris ini: '{header}'.",
        "duplicate": "Dua halaman bernama '{section}'. Beri setiap halaman nama sendiri.",
    },
    "bg": {
        "broken_choice": "Страницата '{section}' има избор към '{target}', но такава страница още няма. Направи страница '{target}' или поправи избора.",
        "orphaned": "Никой избор не води до страницата '{section}', затова читателите не могат да стигнат до нея. Добави [[избор]] към нея от друга страница.",
        "missing_start": "Историята ти започва от '{section}', но няма страница с това име. Поправи името на началото или направи тази страница.",
        "empty": "Историята ти е празна. Добави заглавие и първа страница, за да започнеш!",
        "no_metadata": "Всяка история има нужда от блок със заглавие най-горе. Сложи заглавието между два реда ---.",
        "no_title": "Историята ти има нужда от заглавие. Добави най-горе ред като 'title: Моята история'.",
        "no_sections": "Историята ти още няма страници. Добави страница като [[start]] с няколко думи.",
        "bad_header": "Името на страница изглежда като [[start]]. Провери този ред: '{header}'.",
        "duplicate": "Две страници се казват '{section}'. Дай на всяка страница собствено име.",
    },
}


def get_error_hint(message: str, lang: str = DEFAULT_LANGUAGE) -> Optional[str]:
    """Turn a raw validator/compiler message into a child-friendly hint.

    Returns a localized, plain-language suggestion for known messages, or
    ``None`` when the message isn't recognised (so callers keep the raw text).
    """
    text = _HINT_TEXT.get(lang, _HINT_TEXT[DEFAULT_LANGUAGE])
    for kind, pattern, groups in _HINT_PATTERNS:
        match = re.search(pattern, message)
        if not match:
            continue
        params = {name: match.group(index + 1) for index, name in enumerate(groups)}
        return text[kind].format(**params)
    return None
