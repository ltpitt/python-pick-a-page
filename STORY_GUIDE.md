# 📖 How to Create Your Own Adventure Story

*Create amazing "Choose Your Own Adventure" stories that open in your web browser!*

---

## 🇬🇧 English

### What is Pick-a-Page?

Pick-a-Page helps you write interactive stories where **YOU** choose what happens next! Write your story in a simple text file, and the program turns it into a beautiful webpage that you can read in your browser.

### Quick Start (3 Easy Steps!)

1. **Create a story file** - Make a new file called `my-story.txt`
2. **Write your story** - Follow the simple format below
3. **Compile it** - Run: `python -m pick_a_page compile my-story.txt`

The story will automatically open in your browser! 🎉

### Writing Your Story

Every story needs two parts:

#### 1. Story Information (at the top)

```
---
title: My Amazing Adventure
author: Your Name
---
```

#### 2. Story Sections

Each section starts with `[[section name]]` and contains your story text:

```
[[beginning]]

You wake up in a mysterious castle. A dragon is sleeping nearby!

What do you do?

[[Wake the dragon]]
[[Sneak past quietly]]

---

[[Wake the dragon]]

The dragon opens one eye and smiles. "Hello, friend!"

You made a new friend!

---

[[Sneak past quietly]]

You tiptoe past the dragon and find a treasure chest!

You won!
```

### Important Rules (Keep it Simple!)

- ✅ Section names: `[[section name]]` (NO colon at the end!)
- ✅ Choices: `[[Choice text]]` creates a button
- ✅ Custom buttons: `[[Go home|beginning]]` (button says "Go home" but goes to "beginning")
- ✅ Separate sections with `---` (three dashes)
- ✅ Sections with no choices = story endings

### Adding Pictures 🖼️

Want to add images? Easy!

1. Put your images in a folder (like `images/`)
2. Add them to your story like this:

```
[[beginning]]

![A spooky castle](images/castle.jpg)

You see a mysterious castle in the distance...

[[Enter the castle]]
```

### Special Formatting

Make your text **bold** or *italic*:

```
You find a **magic sword**!

The wizard says, *"Be careful, young hero!"*
```

### Full Example Story

```
---
title: The Dragon's Secret
author: Gaia
---

[[start]]

You are exploring a mysterious forest when you find a glowing cave.

Do you want to explore it?

[[Yes, go inside|cave]]
[[No, go home|home]]

---

[[cave]]

Inside the cave, you see a **friendly dragon** sleeping on a pile of gold!

The dragon wakes up and smiles at you. "Hello, brave explorer!"

[[Talk to the dragon]]
[[Take some gold]]

---

[[Talk to the dragon]]

The dragon tells you amazing stories about flying and treasure hunting.

You made a magical friend!

**THE END**

---

[[Take some gold]]

The dragon lets you take a small handful of gold coins.

"Use it wisely," the dragon says kindly.

**THE END**

---

[[home]]

You decide to go home. Maybe another day you'll be brave enough!

**THE END**
```

### Compiling Your Story

Once your story is written:

```bash
# Compile and open in browser automatically
python -m pick_a_page compile my-story.txt

# Compile without opening browser
python -m pick_a_page compile my-story.txt --no-open

# Check if your story has any errors
python -m pick_a_page validate my-story.txt

# Create a new story from a template
python -m pick_a_page init my-new-story
```

### Tips for Great Stories

1. **Plan your adventure** - Draw a map of your story paths!
2. **Give choices meaning** - Make different choices lead to different endings
3. **Keep sections short** - A few sentences per section is perfect
4. **Test your story** - Click through every path to make sure it works
5. **Have fun!** - Be creative and tell the story YOU want to tell!

---

## 🇳🇱 Nederlands

### Wat is Pick-a-Page?

Pick-a-Page helpt je interactieve verhalen te schrijven waar **JIJ** kiest wat er gebeurt! Schrijf je verhaal in een simpel tekstbestand, en het programma maakt er een mooie webpagina van die je in je browser kunt lezen.

### Snel Beginnen (3 Simpele Stappen!)

1. **Maak een verhaalbestand** - Maak een nieuw bestand genaamd `mijn-verhaal.txt`
2. **Schrijf je verhaal** - Volg het simpele format hieronder
3. **Compileer het** - Run: `python -m pick_a_page compileren mijn-verhaal.txt`

Het verhaal opent automatisch in je browser! 🎉

### Je Verhaal Schrijven

Elk verhaal heeft twee delen:

#### 1. Verhaalinformatie (bovenaan)

```
---
title: Mijn Geweldige Avontuur
author: Jouw Naam
---
```

#### 2. Verhaalsecties

Elke sectie begint met `[[sectie naam]]` en bevat je verhaaltekst:

```
[[beginning]]

Je wordt wakker in een mysterieus kasteel. Een draak slaapt in de buurt!

Wat doe je?

[[Maak de draak wakker]]
[[Sluip stilletjes voorbij]]

---

[[Maak de draak wakker]]

De draak opent één oog en glimlacht. "Hallo, vriend!"

Je hebt een nieuwe vriend gemaakt!

---

[[Sluip stilletjes voorbij]]

Je sluipt langs de draak en vindt een schatkist!

Je hebt gewonnen!
```

### Belangrijke Regels (Houd het Simpel!)

- ✅ Sectienamen: `[[sectie naam]]` (GEEN dubbele punt aan het einde!)
- ✅ Keuzes: `[[Keuze tekst]]` maakt een knop
- ✅ Aangepaste knoppen: `[[Ga naar huis|beginning]]` (knop zegt "Ga naar huis" maar gaat naar "beginning")
- ✅ Scheid secties met `---` (drie streepjes)
- ✅ Secties zonder keuzes = verhaaleinden

### Afbeeldingen Toevoegen 🖼️

Wil je afbeeldingen toevoegen? Makkelijk!

1. Zet je afbeeldingen in een map (zoals `images/`)
2. Voeg ze toe aan je verhaal zo:

```
[[beginning]]

![Een eng kasteel](images/kasteel.jpg)

Je ziet een mysterieus kasteel in de verte...

[[Ga het kasteel binnen]]
```

### Speciale Opmaak

Maak je tekst **vet** of *cursief*:

```
Je vindt een **magisch zwaard**!

De tovenaar zegt, *"Wees voorzichtig, jonge held!"*
```

### Volledig Voorbeeldverhaal

```
---
title: Het Geheim van de Draak
author: Gaia
---

[[start]]

Je verkent een mysterieus bos wanneer je een gloeiende grot vindt.

Wil je het verkennen?

[[Ja, ga naar binnen|grot]]
[[Nee, ga naar huis|huis]]

---

[[grot]]

Binnen in de grot zie je een **vriendelijke draak** slapen op een stapel goud!

De draak wordt wakker en glimlacht naar je. "Hallo, dappere ontdekkingsreiziger!"

[[Praat met de draak]]
[[Neem wat goud]]

---

[[Praat met de draak]]

De draak vertelt je geweldige verhalen over vliegen en schatzoeken.

Je hebt een magische vriend gemaakt!

**HET EINDE**

---

[[Neem wat goud]]

De draak laat je een klein handje vol gouden munten nemen.

"Gebruik het verstandig," zegt de draak vriendelijk.

**HET EINDE**

---

[[huis]]

Je besluit naar huis te gaan. Misschien ben je een andere dag moedig genoeg!

**HET EINDE**
```

### Je Verhaal Compileren

Zodra je verhaal geschreven is:

```bash
# Compileer en open automatisch in browser
python -m pick_a_page compileren mijn-verhaal.txt

# Compileer zonder browser te openen
python -m pick_a_page compileren mijn-verhaal.txt --no-open

# Controleer of je verhaal fouten heeft
python -m pick_a_page valideren mijn-verhaal.txt

# Maak een nieuw verhaal van een sjabloon
python -m pick_a_page initialiseren mijn-nieuwe-verhaal
```

### Tips voor Geweldige Verhalen

1. **Plan je avontuur** - Teken een kaart van je verhaalpaden!
2. **Geef keuzes betekenis** - Laat verschillende keuzes leiden tot verschillende eindes
3. **Houd secties kort** - Een paar zinnen per sectie is perfect
4. **Test je verhaal** - Klik door elk pad om te controleren of het werkt
5. **Veel plezier!** - Wees creatief en vertel het verhaal dat JIJ wilt vertellen!

---

## 🇮🇹 Italiano

### Cos'è Pick-a-Page?

Pick-a-Page ti aiuta a scrivere storie interattive dove **TU** scegli cosa succede dopo! Scrivi la tua storia in un semplice file di testo, e il programma la trasforma in una bellissima pagina web che puoi leggere nel tuo browser.

### Avvio Rapido (3 Semplici Passi!)

1. **Crea un file storia** - Crea un nuovo file chiamato `mia-storia.txt`
2. **Scrivi la tua storia** - Segui il formato semplice qui sotto
3. **Compilalo** - Esegui: `python -m pick_a_page compila mia-storia.txt`

La storia si aprirà automaticamente nel tuo browser! 🎉

### Scrivere la Tua Storia

Ogni storia ha bisogno di due parti:

#### 1. Informazioni sulla Storia (in cima)

```
---
title: La Mia Incredibile Avventura
author: Il Tuo Nome
---
```

#### 2. Sezioni della Storia

Ogni sezione inizia con `[[nome sezione]]` e contiene il testo della tua storia:

```
[[beginning]]

Ti svegli in un castello misterioso. Un drago sta dormendo nelle vicinanze!

Cosa fai?

[[Sveglia il drago]]
[[Passa di nascosto]]

---

[[Sveglia il drago]]

Il drago apre un occhio e sorride. "Ciao, amico!"

Hai fatto un nuovo amico!

---

[[Passa di nascosto]]

Passi in punta di piedi oltre il drago e trovi un baule del tesoro!

Hai vinto!
```

### Regole Importanti (Mantienilo Semplice!)

- ✅ Nomi sezioni: `[[nome sezione]]` (NESSUN due punti alla fine!)
- ✅ Scelte: `[[Testo scelta]]` crea un pulsante
- ✅ Pulsanti personalizzati: `[[Vai a casa|beginning]]` (il pulsante dice "Vai a casa" ma va a "beginning")
- ✅ Separa le sezioni con `---` (tre trattini)
- ✅ Sezioni senza scelte = finali della storia

### Aggiungere Immagini 🖼️

Vuoi aggiungere immagini? Facile!

1. Metti le tue immagini in una cartella (come `images/`)
2. Aggiungile alla tua storia così:

```
[[beginning]]

![Un castello spaventoso](images/castello.jpg)

Vedi un castello misterioso in lontananza...

[[Entra nel castello]]
```

### Formattazione Speciale

Rendi il tuo testo **grassetto** o *corsivo*:

```
Trovi una **spada magica**!

Il mago dice, *"Stai attento, giovane eroe!"*
```

### Esempio di Storia Completa

```
---
title: Il Segreto del Drago
author: Gaia
---

[[start]]

Stai esplorando una foresta misteriosa quando trovi una grotta luminosa.

Vuoi esplorarla?

[[Sì, entra|grotta]]
[[No, vai a casa|casa]]

---

[[grotta]]

Dentro la grotta, vedi un **drago amichevole** che dorme su un mucchio d'oro!

Il drago si sveglia e ti sorride. "Ciao, coraggioso esploratore!"

[[Parla con il drago]]
[[Prendi dell'oro]]

---

[[Parla con il drago]]

Il drago ti racconta storie incredibili su volare e cacciare tesori.

Hai fatto un amico magico!

**LA FINE**

---

[[Prendi dell'oro]]

Il drago ti lascia prendere una piccola manciata di monete d'oro.

"Usale saggiamente," dice gentilmente il drago.

**LA FINE**

---

[[casa]]

Decidi di andare a casa. Forse un altro giorno sarai abbastanza coraggioso!

**LA FINE**
```

### Compilare la Tua Storia

Una volta scritta la tua storia:

```bash
# Compila e apri automaticamente nel browser
python -m pick_a_page compila mia-storia.txt

# Compila senza aprire il browser
python -m pick_a_page compila mia-storia.txt --no-open

# Controlla se la tua storia ha errori
python -m pick_a_page valida mia-storia.txt

# Crea una nuova storia da un modello
python -m pick_a_page inizializza mia-nuova-storia
```

### Consigli per Grandi Storie

1. **Pianifica la tua avventura** - Disegna una mappa dei percorsi della tua storia!
2. **Dai significato alle scelte** - Fai in modo che scelte diverse portino a finali diversi
3. **Mantieni le sezioni brevi** - Alcune frasi per sezione sono perfette
4. **Testa la tua storia** - Clicca attraverso ogni percorso per assicurarti che funzioni
5. **Divertiti!** - Sii creativo e racconta la storia che TU vuoi raccontare!

---

## 🎨 Need Help?

- **Check your story for errors**: `python -m pick_a_page validate my-story.txt`
- **Start with an example**: Look at `examples/dragon_quest_en.txt` (or `_nl.txt` or `_it.txt`)
- **Get help**: `python -m pick_a_page --help`

## 🚀 Have Fun Creating Stories!

Remember: there are no wrong stories, only different adventures! Be creative, try new things, and most importantly, have fun! 🌟
