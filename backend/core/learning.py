"""Learning content: guided tutorial + child-friendly Markdown reference.

Markdown syntax is the same in every language, so the ``syntax`` and
``example`` fields are language-neutral and defined once. Only the human
text (labels, hints, titles, bodies) is translated. English is the fallback
for any unknown language.

Pure Python / stdlib only, mirroring :mod:`backend.core.i18n`.
"""

from typing import Dict, List, Tuple

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
        "italic": ("Parole inclinate", "Metti le parole tra * per inclinarle."),
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

# Per-language (tutorial_cta, tutorial_heading, tutorial_done, help_summary).
_UI_TEXT: Dict[str, Tuple[str, str, str, str]] = {
    "en": ("Show me how", "How to make a story", "Got it!", "Markdown help"),
    "nl": ("Laat me zien", "Hoe maak je een verhaal", "Begrepen!", "Markdown-hulp"),
    "it": ("Mostrami come", "Come creare una storia", "Capito!", "Aiuto Markdown"),
    "es": ("Muéstrame cómo", "Cómo crear una historia", "¡Entendido!", "Ayuda de Markdown"),
    "fr": ("Montre-moi", "Comment faire une histoire", "Compris !", "Aide Markdown"),
    "pt": ("Mostra-me como", "Como criar uma história", "Percebi!", "Ajuda Markdown"),
    "de": ("Zeig mir wie", "So machst du eine Geschichte", "Verstanden!", "Markdown-Hilfe"),
    "ru": ("Покажи мне", "Как создать историю", "Понятно!", "Помощь по Markdown"),
    "zh": ("教我怎么做", "如何创作故事", "明白了！", "Markdown 帮助"),
    "hi": ("मुझे दिखाओ", "कहानी कैसे बनाएँ", "समझ गया!", "Markdown मदद"),
    "ar": ("أرِني كيف", "كيف تصنع قصة", "فهمت!", "مساعدة Markdown"),
    "bn": ("আমাকে দেখাও", "কীভাবে গল্প বানাবে", "বুঝেছি!", "Markdown সাহায্য"),
    "ur": ("مجھے دکھائیں", "کہانی کیسے بنائیں", "سمجھ گیا!", "Markdown مدد"),
    "id": ("Tunjukkan caranya", "Cara membuat cerita", "Mengerti!", "Bantuan Markdown"),
    "bg": ("Покажи ми как", "Как да направиш история", "Разбрах!", "Помощ за Markdown"),
}


def get_ui_labels(lang: str) -> Dict[str, str]:
    """Return localized UI chrome labels for the learning features."""
    cta, heading, done, summary = _UI_TEXT.get(lang, _UI_TEXT[DEFAULT_LANGUAGE])
    return {
        "tutorial_cta": cta,
        "tutorial_heading": heading,
        "tutorial_done": done,
        "help_summary": summary,
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
