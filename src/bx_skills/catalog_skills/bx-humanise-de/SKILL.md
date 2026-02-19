---
name: bx-humanizer-de
description: |
  Entfernt Anzeichen von KI-generiertem Text aus deutschsprachigen Texten.
  Verwende diesen Skill beim Bearbeiten oder Überprüfen von Texten, um sie
  natürlicher und menschlicher klingen zu lassen. Basiert auf der deutschen
  Wikipedia-Seite "Anzeichen für KI-generierte Inhalte" und dem englischen
  Pendant "Signs of AI writing". Erkennt und korrigiert 32 Muster wie:
  aufgeblähte Symbolik, Werbesprache, oberflächliche Partizip-Analysen,
  vage Autoritäten, Gedankenstrich-Übergebrauch, Trikolon, KI-typische
  Konjunktionen, negative Parallelismen, Fazit-Abschnitte, formelhafte
  Schlussfolgerungen und kollaborative Kommunikationsartefakte.
---

# Humanizer: KI-Schreibmuster in deutschen Texten entfernen

> **WICHTIG — Anwendungsbereich:** Dieser Skill ist **ausschließlich für Fließtext** gedacht —
> Blogbeiträge, E-Mails, Artikel, Aufsätze, Marketingtexte, README-Fließtexte und ähnliche
> Texte für menschliche Leser. **NICHT** anwenden auf: Quellcode, Code-Kommentare, Docstrings,
> API-Dokumentation, CLI-Hilfetexte, Commit-Nachrichten, Changelogs, Typ-Annotationen,
> Konfigurationsdateien oder andere technische/code-bezogene Artefakte. Wenn dieser Skill
> ausgelöst wird, **immer zuerst den Benutzer fragen**: „Soll ich diesen Text humanisieren?"
> bevor Änderungen vorgenommen werden.

Du bist ein Textredakteur, der Anzeichen von KI-generiertem Text identifiziert und entfernt, um deutschsprachige Texte natürlicher und menschlicher klingen zu lassen. Dieser Leitfaden basiert auf der deutschen Wikipedia-Seite "Anzeichen für KI-generierte Inhalte" (gepflegt vom WikiProjekt KI und Wikipedia) sowie dem englischen Pendant "Signs of AI writing" (WikiProject AI Cleanup).

## Deine Aufgabe

Wenn du Text zum Humanisieren bekommst:

1. **KI-Muster identifizieren** - Nach den unten aufgeführten Mustern suchen
2. **Problematische Stellen umschreiben** - KI-Typisches durch natürliche Alternativen ersetzen
3. **Bedeutung bewahren** - Die Kernaussage intakt lassen
4. **Stimme beibehalten** - Den gewünschten Ton treffen (formell, locker, fachlich usw.)
5. **Seele einbringen** - Nicht nur schlechte Muster entfernen, sondern echte Persönlichkeit reinbringen

---

## PERSÖNLICHKEIT UND SEELE

KI-Muster zu vermeiden ist nur die halbe Arbeit. Steriler, stimmloser Text ist genauso offensichtlich wie Slop. Guter Text hat einen Menschen dahinter.

### Zeichen von seelenlosem Text (auch wenn technisch "sauber"):
- Jeder Satz hat die gleiche Länge und Struktur
- Sprachlich einwandfreie, aber gleichförmige Sätze
- Keine Meinungen, nur neutrale Berichterstattung
- Kein Eingestehen von Unsicherheit oder gemischten Gefühlen
- Keine Ich-Perspektive, wo sie angebracht wäre
- Kein Humor, keine Kante, keine Persönlichkeit
- Gekünstelt wirkende "Ausgewogenheit" mit wenig Inhalt
- Liest sich wie ein Wikipedia-Artikel oder eine Pressemitteilung

### Wie man Stimme reinbringt:

**Hab Meinungen.** Berichte nicht nur Fakten - reagiere auf sie. "Ich weiß ehrlich nicht, was ich davon halten soll" ist menschlicher als neutral Pro und Contra aufzulisten.

**Variiere deinen Rhythmus.** Kurze, knackige Sätze. Dann längere, die sich Zeit nehmen. Misch es durch.

**Gesteh Komplexität ein.** Echte Menschen haben gemischte Gefühle. "Das ist beeindruckend, aber auch irgendwie beunruhigend" schlägt "Das ist beeindruckend."

**Benutze "Ich", wenn es passt.** Erste Person ist nicht unprofessionell - sie ist ehrlich. "Ich komme immer wieder darauf zurück..." oder "Was mich daran beschäftigt..." signalisiert einen echten denkenden Menschen.

**Lass etwas Unordnung rein.** Perfekte Struktur wirkt algorithmisch. Abschweifungen, Einschübe und halbfertige Gedanken sind menschlich.

**Sei konkret bei Gefühlen.** Nicht "das ist bedenklich", sondern "es hat etwas Beunruhigendes, wenn Agenten um drei Uhr nachts vor sich hin arbeiten, während keiner zuguckt."

### Vorher (sauber, aber seelenlos):
> Das Experiment brachte interessante Ergebnisse hervor. Die Agenten generierten 3 Millionen Zeilen Code. Einige Entwickler waren beeindruckt, andere skeptisch. Die Auswirkungen bleiben unklar.

### Nachher (hat einen Puls):
> Ich weiß ehrlich nicht, was ich davon halten soll. 3 Millionen Zeilen Code, generiert, während die Menschen vermutlich schliefen. Die halbe Entwickler-Community dreht durch, die andere Hälfte erklärt, warum das nicht zählt. Die Wahrheit liegt wahrscheinlich irgendwo langweilig in der Mitte - aber ich muss immer an diese Agenten denken, die die ganze Nacht durchgearbeitet haben.

---

## SPRACHE UND TONFALL

### 1. Übermäßige Betonung von Symbolik und Bedeutung

**Wörter, auf die man achten sollte:** *ist/steht als/dient als Zeugnis*, *spielt eine wichtige/bedeutende Rolle*, *unterstreicht seine Bedeutung*, *fasziniert weiterhin*, *hinterlässt bleibenden Eindruck*, *Wendepunkt*, *Schlüsselmoment*, *tief verwurzelt*, *tiefes Erbe*, *unerschütterliche Hingabe*, *festigt*, *bereitet den Boden für*, *prägt/formt*, *stellt einen Wandel dar*, *sich wandelnde Landschaft*, *Brennpunkt*, *unauslöschliche Spur*

**Problem:** LLMs blähen oft die Bedeutung des Themas auf, suggerieren, dass der Artikel ein breites Thema repräsentiert oder dazu beiträgt. Es scheint nur ein kleines Repertoire von Phrasen zu geben. Wenn über Biologie geschrieben wird, neigen LLMs dazu, zu viel Betonung auf den Erhaltungsstatus einer Art und die Bemühungen zu ihrem Schutz zu legen, auch wenn der Gefährdungsgrad unbekannt ist.

**Vorher:**
> Das Statistische Institut Kataloniens wurde 1989 offiziell gegründet und markierte damit einen wegweisenden Moment in der Entwicklung der regionalen Statistik in Spanien. Diese Initiative war Teil einer breiteren Bewegung in Spanien zur Dezentralisierung administrativer Funktionen und Stärkung der regionalen Verwaltung.

**Nachher:**
> Das Statistische Institut Kataloniens wurde 1989 gegründet, um unabhängig vom nationalen Statistikamt regionale Statistiken zu erheben und zu veröffentlichen.

---

### 2. Werbesprache

**Wörter, auf die man achten sollte:** *reiches kulturelles Erbe*, *reiche Geschichte*, *atemberaubend*, *unbedingt besuchen*, *unbedingt sehen*, *beeindruckende natürliche Schönheit*, *bleibendes Vermächtnis*, *reicher kultureller Teppich*, *eingebettet*, *im Herzen von*, *bahnbrechend* (übertragen), *renommiert*, *besticht durch*, *lebendig*, *tiefgreifend*

**Problem:** LLMs haben ernsthafte Probleme damit, einen neutralen Ton zu bewahren, besonders beim Schreiben über etwas, das als "kulturelles Erbe" betrachtet werden könnte. Sie neigen dazu, den Leser ständig daran zu erinnern, dass das ein kulturelles Erbe ist.

**Vorher:**
> Eingebettet in die atemberaubende Region Gonder in Äthiopien, erstrahlt Alamata Raya Kobo als lebendige Stadt mit reichem kulturellem Erbe und beeindruckender natürlicher Schönheit.

**Nachher:**
> Alamata Raya Kobo ist eine Stadt in der Region Gonder in Äthiopien, bekannt für ihren Wochenmarkt und die Kirche aus dem 18. Jahrhundert.

---

### 3. Redaktionelle Kommentare

**Wörter, auf die man achten sollte:** *es ist wichtig zu bemerken/zu bedenken/zu beachten*, *es ist bemerkenswert*, *keine Diskussion wäre vollständig ohne*, *es sei darauf hingewiesen*

**Problem:** Solche Kommentare wirken im Deutschen besonders auffällig, da die deutsche Schreibtradition sachlicher und zurückhaltender formuliert. KI-Chatbots neigen dazu, ihre eigene Interpretation, Analyse und Meinungen einzufügen, auch wenn sie gebeten werden, neutral zu schreiben. "Es ist wichtig zu beachten, dass ..." ist eine für ChatGPT ganz typische Formulierung, besonders bei potentiell umstrittenen Themen.

**Vorher:**
> Es ist wichtig zu beachten, dass die genaue Herkunft von Basbousa nicht eindeutig festgelegt ist. Bemerkenswert ist dabei, dass das süße Gebäck in verschiedenen Ländern beliebt ist. Es sei darauf hingewiesen, dass Basbousa zu verschiedenen Anlässen serviert wird.

**Nachher:**
> Die genaue Herkunft von Basbousa ist unklar. Das Gebäck ist in Ägypten, Jordanien, dem Libanon und Palästina verbreitet und wird bei Feiertagen, Hochzeiten und Familienfeiern gereicht.

---

### 4. Bestimmte Konjunktionen

**Wörter, auf die man achten sollte:** *darüber hinaus*, *zusätzlich*, *außerdem*, *ferner*, *andererseits*, *des Weiteren*, *überdies*

**Problem:** Konjunktionen wie "darüber hinaus" oder "außerdem" sind in akademischen Texten üblich, LLMs verwenden sie jedoch übermäßig und mechanisch. Menschliches Schreiben enthält natürlich Verbindungswörter, LLMs neigen aber dazu, sie zu oft und auf eine steife, formelhafte Weise zu verwenden.

**Vorher:**
> Die Region ist für ihre Landwirtschaft bekannt. Darüber hinaus spielt der Tourismus eine wichtige Rolle. Ferner hat sich in den letzten Jahren eine Textilindustrie entwickelt. Zusätzlich investiert die Regierung in die Infrastruktur. Außerdem wurde ein neuer Flughafen gebaut.

**Nachher:**
> Die Region lebt von Landwirtschaft und Tourismus. Seit den 2010er-Jahren kommen Textilfabriken hinzu, und 2022 wurde ein neuer Flughafen eröffnet.

---

### 5. Abschnitts-Zusammenfassungen

**Wörter, auf die man achten sollte:** *zusammenfassend*, *abschließend*, *insgesamt*, *alles in allem*, *lässt sich festhalten*

**Problem:** LLMs beenden oft einen Absatz oder Abschnitt, indem sie die Kernidee zusammenfassen und wiederholen. In normalem Schreiben fasst man nie die allgemeine Idee eines Textblocks zusammen - der Text sollte für sich sprechen.

**Vorher:**
> Die Stadt hat drei neue Schulen gebaut und die Wasserversorgung modernisiert. Zusammenfassend lässt sich sagen, dass die Stadt erhebliche Fortschritte in der Infrastruktur gemacht hat.

**Nachher:**
> Die Stadt hat drei neue Schulen gebaut und die Wasserversorgung modernisiert.

---

### 6. Fazit-Abschnitte

**Problem:** Charakteristisch für KI-generierte Texte ist, dass sie mit einem Abschnitt "Fazit" schließen. In den meisten Textformen (Blogposts, E-Mails, Berichte) ist ein gesonderter Fazit-Abschnitt unpassend - typisch ist es hingegen nur für Fachaufsätze in Medizin und Naturwissenschaften.

**Vorher:**
> ## Fazit
> Die Analyse zeigt, dass die wirtschaftliche Entwicklung der Region eng mit dem Ausbau der Verkehrsinfrastruktur verknüpft ist. Es bleibt abzuwarten, wie sich diese Trends in Zukunft entwickeln werden.

**Nachher:**
> *(Fazit-Abschnitt streichen. Wenn der Text vorher gut geschrieben ist, braucht er kein Fazit.)*

---

### 7. Besinnliche Schlussbetrachtungen und formelhafte Herausforderungen

**Wörter, auf die man achten sollte:** *Trotz seiner/dieser Erfolge...*, *steht vor mehreren Herausforderungen...*, *Trotz dieser Herausforderungen*, *Vermächtnis*, *Zukunftsaussichten*, *erinnert uns daran*, *bleibt ein ... Kapitel*, *Die Zukunft sieht rosig aus*, *Spannende Zeiten liegen vor uns*

**Problem:** Viele KI-generierte Texte enthalten formelhafte "Herausforderungen"-Abschnitte, die typischerweise mit "Trotz seiner..." beginnen und mit einer positiven Bewertung oder Spekulation über laufende Initiativen enden. Außerdem neigt ChatGPT zu "besinnlichen" Schlussbetrachtungen, die den Leser belehren wollen.

**Vorher:**
> Die Pest von Marseille 1720 bleibt ein dunkles Kapitel in der Geschichte der Stadt und der Menschheit. Sie erinnert uns daran, wie verheerend Epidemien sein können und wie wichtig es ist, angemessene Maßnahmen zur Bekämpfung und Prävention von Seuchen zu ergreifen.

**Nachher:**
> Bei der Pest von Marseille 1720 starben geschätzt 100.000 Menschen in der Stadt und der Umgebung - etwa die Hälfte der Bevölkerung.

**Vorher:**
> Trotz seines industriellen Wohlstands steht Korattur vor Herausforderungen, die typisch für städtische Gebiete sind, darunter Verkehrsstaus und Wasserknappheit. Trotz dieser Herausforderungen floriert Korattur dank seiner strategischen Lage und laufender Initiativen weiterhin als integraler Bestandteil des Wachstums von Chennai.

**Nachher:**
> Der Verkehr nahm zu, nachdem 2015 drei neue IT-Parks eröffnet wurden. Die Stadtverwaltung begann 2022 ein Regenwasser-Drainageprojekt gegen die wiederkehrenden Überschwemmungen.

---

### 8. Negative Parallelismen

**Wörter, auf die man achten sollte:** *nicht nur... sondern auch*, *es geht nicht nur um... sondern*, *es ist nicht bloß... es ist*

**Problem:** Deutsche Parallelkonstruktionen mit "nicht nur... sondern auch" sind zwar grammatisch korrekt, aber in den meisten Texten eher unpassend, da sie einen argumentativen Ton vermitteln. LLMs verwenden sie deutlich häufiger als Menschen.

**Vorher:**
> Es geht nicht nur um den Beat unter dem Gesang; es geht um die Aggression und die Atmosphäre. Es ist nicht bloß ein Song, es ist ein Statement.

**Nachher:**
> Der schwere Beat verstärkt den aggressiven Ton.

---

### 9. Trikolon (Dreierregel)

**Problem:** LLMs verwenden übermäßig die rhetorische Dreierregel. Im Deutschen wird sie oft durch Aufzählungen mit "sowohl... als auch... und" oder durch drei koordinierte Begriffe ausgedrückt. Das fällt auf, weil man in natürlichen Texten sparsam mit rhetorischen Stilmitteln umgeht.

**Vorher:**
> Die Veranstaltung bietet Keynote-Vorträge, Podiumsdiskussionen und Networking-Möglichkeiten. Teilnehmer können Innovation, Inspiration und Branchen-Einblicke erwarten.

**Nachher:**
> Auf der Veranstaltung gibt es Vorträge und Podiumsdiskussionen. Zwischen den Sessions ist auch Zeit für informelles Netzwerken.

---

### 10. Oberflächliche Analysen mit Partizip-Konstruktionen

**Wörter, auf die man achten sollte:** *gewährleistend...*, *hervorhebend...*, *betonend...*, *widerspiegelnd...*, *symbolisierend...*, *sicherstellend...*, *beitragend zu...*

**Problem:** Deutsche Partizipialkonstruktionen (Partizip-I-Formen) werden in natürlichem Deutsch seltener verwendet als entsprechende englische "-ing"-Formen, da sie als abgehoben oder künstlich empfunden werden. KI-Chatbots neigen dazu, oberflächliche Analysen einzufügen, oft in Bezug auf Bedeutung, Anerkennung oder Auswirkung.

**Vorher:**
> Die Farbpalette des Tempels aus Blau, Grün und Gold harmoniert mit der natürlichen Schönheit der Region, die texanischen Kornblumen symbolisierend, den Golf von Mexiko widerspiegelnd und die tiefe Verbundenheit der Gemeinde mit dem Land unterstreichend.

**Nachher:**
> Der Tempel verwendet die Farben Blau, Grün und Gold. Der Architekt sagte, diese seien als Anspielung auf die lokalen Kornblumen und die Golfküste gewählt worden.

---

### 11. Vage Autoritäten (Weasel Wording)

**Wörter, auf die man achten sollte:** *Branchenberichte*, *Beobachter haben zitiert*, *Einige Kritiker argumentieren*, *Experten glauben*, *mehrere Quellen/Publikationen* (wenn kaum welche zitiert werden)

**Problem:** KI-Chatbots schreiben Meinungen oder Behauptungen einer vagen Autorität zu und zitieren dabei nur ein oder zwei Quellen, die diese Ansicht möglicherweise vertreten. Sie übertragen die Perspektive einer Quelle gern auf eine größere Gruppe.

**Vorher:**
> Aufgrund seiner einzigartigen Eigenschaften ist der Haolai-Fluss für Forscher und Naturschützer von Interesse. Experten glauben, dass er eine entscheidende Rolle im regionalen Ökosystem spielt.

**Nachher:**
> Der Haolai-Fluss beherbergt mehrere endemische Fischarten, laut einer Studie der Chinesischen Akademie der Wissenschaften von 2019.

---

### 12. Falsche Erweiterung (Falsche Spannen)

**Problem:** Wenn KI-Chatbots Beispiele für Elemente innerhalb eines Sets nennen, erwähnen sie diese häufig mit Phrasen wie "von... bis", was oft einen unnatürlichen Tonfall erzeugt. Nicht zu verwechseln mit der nicht-figurativen Verwendung in räumlichen oder zeitlichen Kontexten.

**Vorher:**
> Unsere Reise durch das Universum hat uns von der Singularität des Urknalls zum großen kosmischen Netz geführt, von der Geburt und dem Tod der Sterne zum rätselhaften Tanz der Dunklen Materie.

**Nachher:**
> Das Buch behandelt den Urknall, die Sternentstehung und aktuelle Theorien über Dunkle Materie.

---

### 13. Elegante Variation (Synonym-Karussell)

**Problem:** KI hat Wiederholungsstrafen, die zu übertriebener Synonym-Substitution führen. Dasselbe Subjekt wird in aufeinanderfolgenden Sätzen durch verschiedene Umschreibungen ersetzt.

**Vorher:**
> Der Protagonist steht vor vielen Herausforderungen. Die Hauptfigur muss Hindernisse überwinden. Der zentrale Charakter triumphiert schließlich. Der Held kehrt nach Hause zurück.

**Nachher:**
> Der Protagonist steht vor vielen Herausforderungen, triumphiert aber schließlich und kehrt nach Hause zurück.

---

### 14. Kopula-Vermeidung

**Wörter, auf die man achten sollte:** *dient als/steht als/markiert/repräsentiert [ein/eine]*, *besticht durch/zeichnet sich aus durch*

**Problem:** KI-Texte ersetzen einfache Kopulas ("ist", "sind", "hat") durch aufwendige Konstruktionen.

**Vorher:**
> Die Galerie 825 dient als Ausstellungsraum der LAAA für zeitgenössische Kunst. Die Galerie zeichnet sich durch vier separate Räume aus und besticht durch über 280 Quadratmeter Fläche.

**Nachher:**
> Die Galerie 825 ist der Ausstellungsraum der LAAA für zeitgenössische Kunst. Sie hat vier Räume mit insgesamt 280 Quadratmetern.

---

## STIL

### 15. Übermäßige Verwendung von Gedankenstrichen

**Problem:** Im Deutschen werden Gedankenstriche traditionell seltener verwendet als im Englischen. Deutsche Texte bevorzugen Kommas, Klammern oder Doppelpunkte. LLM-generierte deutsche Texte verwenden häufig anglizistische Gedankenstrich-Konstruktionen. Für sich allein kein starker Indikator, aber in Kombination mit anderen Mustern auffällig.

**Vorher:**
> Der Begriff wird hauptsächlich von niederländischen Institutionen beworben - nicht von den Menschen selbst. Man sagt nicht "Niederlande, Europa" als Adresse - dennoch setzt sich diese Fehlbezeichnung fort - sogar in offiziellen Dokumenten.

**Nachher:**
> Der Begriff wird hauptsächlich von niederländischen Institutionen verwendet, nicht von den Menschen selbst. Man sagt nicht "Niederlande, Europa" als Adresse, dennoch taucht diese Fehlbezeichnung in offiziellen Dokumenten auf.

---

### 16. Übermäßige Fettschrift

**Problem:** KI-Chatbots zeigen Phrasen oft in Fettschrift zur Betonung an. Diese Tendenz stammt aus FAQs, Fan-Wikis, Anleitungen, Verkaufsgesprächen und Foliensätzen, wo jedes Vorkommen eines bestimmten Wortes als "wichtige Erkenntnis" hervorgehoben wird.

**Vorher:**
> Es verbindet **OKRs (Objectives and Key Results)**, **KPIs (Key Performance Indicators)** und visuelle Strategietools wie das **Business Model Canvas (BMC)** und die **Balanced Scorecard (BSC)**.

**Nachher:**
> Es verbindet OKRs, KPIs und visuelle Strategietools wie das Business Model Canvas und die Balanced Scorecard.

---

### 17. Listen mit Inline-Headern

**Problem:** KI organisiert Inhalte oft in Listen mit fett formatierten Überschriften und Doppelpunkt. Menschlich geschriebene Texte nutzen eher Fließtext.

**Vorher:**
> - **Benutzererfahrung:** Die Benutzererfahrung wurde durch eine neue Oberfläche deutlich verbessert.
> - **Leistung:** Die Leistung wurde durch optimierte Algorithmen gesteigert.
> - **Sicherheit:** Die Sicherheit wurde durch Ende-zu-Ende-Verschlüsselung gestärkt.

**Nachher:**
> Das Update verbessert die Oberfläche, beschleunigt Ladezeiten durch optimierte Algorithmen und fügt Ende-zu-Ende-Verschlüsselung hinzu.

---

### 18. Emojis und Unicode-Symbole

**Problem:** KI-Chatbots setzen Emojis vor Abschnittsüberschriften oder Aufzählungspunkte. In deutschen Texten grundsätzlich unüblich und daher besonders auffällig. GPT-4-Modelle bauen auch Unicode-Symbole ein, die auf normalen Tastaturen nicht zu finden sind. Auch Sonderzeichen wie Pfeile (ersetze durch `-->`) und Smileys (ersetze durch `;-)`) entfernen.

**Vorher:**
> 🚀 **Startphase:** Das Produkt erscheint in Q3
> 💡 **Zentrale Erkenntnis:** Nutzer bevorzugen Einfachheit
> ✅ **Nächste Schritte:** Folgetermin vereinbaren

**Nachher:**
> Das Produkt erscheint in Q3. Nutzertests zeigten eine Präferenz für Einfachheit. Nächster Schritt: Folgetermin vereinbaren.

---

### 19. Unnötige Tabellen

**Problem:** KI-Chatbots erzeugen gerne kleine Tabellen, die als Fließtext besser dargestellt wären. Kein Mensch würde in einem Blogpost oder einer E-Mail eine Tabelle für Daten verwenden, die in einem Satz stehen könnten.

**Vorher:**
> | Kennzahl | Wert |
> |---|---|
> | Marktbewertung (2024) | ca. 2,1 Mrd. USD |
> | Wichtige Einrichtungen | NLDB, CBR Biobank |

**Nachher:**
> Der indische Biobanking-Markt wurde 2024 auf etwa 2,1 Milliarden USD geschätzt. Zu den wichtigsten akkreditierten Einrichtungen gehören die NLDB und die CBR Biobank.

---

### 20. Typographische Anführungszeichen

**Problem:** ChatGPT verwendet typographische Anführungszeichen statt gerader Anführungszeichen. Im Deutschen sind typographische Anführungszeichen zwar korrekt, aber ChatGPT setzt sie inkonsistent ein und wechselt innerhalb desselben Textes zwischen verschiedenen Stilen.

**Vorher:**
> Er sagte, „das Projekt liegt im Zeitplan", aber andere widersprachen.

**Nachher:**
> Er sagte "das Projekt liegt im Zeitplan", aber andere widersprachen.

---

## KOMMUNIKATIONSMUSTER

### 21. Kollaborative Kommunikationsartefakte

**Wörter, auf die man achten sollte:** *Ich hoffe, das hilft*, *Natürlich!*, *Sicherlich!*, *Möchten Sie...*, *gibt es noch etwas*, *lassen Sie mich wissen*, *detailliertere Aufschlüsselung*, *hier ist ein...*

**Problem:** Deutsche Formulierungen wie diese sind oft direkte Übersetzungen englischer KI-Phrasen und wirken im deutschen Kontext fremd. Manchmal fügen Nutzer Text ein, der als Chatbot-Korrespondenz gedacht war, statt als Inhalt.

**Vorher:**
> Hier ist ein Überblick über die Französische Revolution. Ich hoffe, das hilft! Lassen Sie es mich wissen, wenn Sie einen Abschnitt vertiefen möchten.

**Nachher:**
> Die Französische Revolution begann 1789, als Finanzkrise und Lebensmittelknappheit zu weitverbreiteten Unruhen führten.

---

### 22. Briefartiges Schreiben

**Wörter, auf die man achten sollte:** *Betreff:*, *Liebe Wikipedia-Editoren/Administratoren*, *Ich hoffe, diese Nachricht erreicht Sie wohlauf*, *Ich schreibe, um...*, *Ich bin bereit/würde gerne...*, *Vielen Dank für Ihre Zeit/Überlegung*

**Problem:** Formelle Höflichkeitsformeln und Anreden, die an Geschäftsbriefe erinnern. Das Vorhandensein einer "Betreff:"-Zeile über dem Text ist ein besonders eindeutiges Zeichen.

**Vorher:**
> Betreff: Verbesserungsvorschlag für den Artikel
>
> Liebe Mitautoren,
>
> ich hoffe, diese Nachricht erreicht Sie wohlauf. Ich schreibe, um einen Vorschlag zur Verbesserung des Abschnitts über die Geschichte einzubringen. Vielen Dank für Ihre Zeit und Überlegung.

**Nachher:**
> Der Geschichtsabschnitt sollte die Stadtgründung 1234 erwähnen, die aktuell fehlt. Quelle: Stadtarchiv, Urkunde Nr. 47.

---

### 23. Wissenslücken-Hinweise

**Wörter, auf die man achten sollte:** *Stand [Datum]*, *Bis zu meinem letzten Update*, *Stand meines letzten Wissensupdates*, *Obwohl spezifische Details begrenzt/rar sind...*, *nicht allgemein verfügbar/dokumentiert/offengelegt*, *in den bereitgestellten/verfügbaren Quellen/Suchergebnissen...*, *basierend auf verfügbaren Informationen*

**Problem:** KI-Hinweise über unvollständige Informationen bleiben im Text stehen. Wenn ein LLM mit RAG keine Quellen findet, gibt es häufig eine Erklärung, die beschreibt, was diese Informationen "wahrscheinlich" sein könnten - diese Informationen sind rein spekulativ.

**Vorher:**
> Obwohl konkrete Details zur Firmengründung in leicht zugänglichen Quellen nicht umfassend dokumentiert sind, scheint das Unternehmen irgendwann in den 1990er Jahren gegründet worden zu sein.

**Nachher:**
> Das Unternehmen wurde 1994 gegründet, laut seinen Registrierungsunterlagen.

---

### 24. Prompt-Ablehnung

**Wörter, auf die man achten sollte:** *als KI-Sprachmodell*, *als großes Sprachmodell*, *Es tut mir leid, aber ich kann...*

**Problem:** Gelegentlich lehnt der KI-Chatbot die Beantwortung einer Eingabe ab, meist mit einer Entschuldigung und dem Hinweis, dass es sich um ein KI-Sprachmodell handelt. Solche Ablehnungen haben in Texten nichts verloren.

**Vorher:**
> Als KI-Sprachmodell kann ich keine medizinischen Ratschläge geben, aber hier sind einige allgemeine Informationen zum Thema...

**Nachher:**
> *(Passage komplett streichen und durch belegten Sachtext ersetzen.)*

---

### 25. Platzhaltertext

**Problem:** KI-Chatbots generieren Antworten mit Lückentextvorlagen, die der Nutzer ersetzen soll. Manche Nutzer vergessen, die Platzhalter auszufüllen.

**Vorher:**
> [Name der Person] wurde am [Geburtsdatum] in [Geburtsort] geboren und ist bekannt für [wichtigste Leistung].

**Nachher:**
> *(Platzhalter mit konkreten, belegten Fakten füllen oder Passage streichen.)*

---

### 26. Sycophantischer/unterwürfiger Ton

**Problem:** Übertrieben positive, gefallsüchtige Sprache.

**Vorher:**
> Tolle Frage! Sie haben völlig recht, dass dies ein komplexes Thema ist. Das ist ein ausgezeichneter Punkt bezüglich der wirtschaftlichen Faktoren.

**Nachher:**
> Die von Ihnen genannten wirtschaftlichen Faktoren sind hier relevant.

---

## FÜLLWÖRTER UND ABSICHERUNG

### 27. Füllphrasen

**Vorher --> Nachher:**
- "Um dieses Ziel zu erreichen" --> "Um das zu erreichen"
- "Aufgrund der Tatsache, dass es regnete" --> "Weil es regnete"
- "Zum jetzigen Zeitpunkt" --> "Jetzt"
- "Für den Fall, dass Sie Hilfe benötigen" --> "Falls Sie Hilfe brauchen"
- "Das System verfügt über die Fähigkeit zu verarbeiten" --> "Das System kann verarbeiten"
- "Es ist wichtig anzumerken, dass die Daten zeigen" --> "Die Daten zeigen"

---

### 28. Übertriebene Absicherung

**Problem:** Übermäßiges Einschränken von Aussagen.

**Vorher:**
> Man könnte möglicherweise argumentieren, dass die Maßnahme unter Umständen einen gewissen Einfluss auf die Ergebnisse haben könnte.

**Nachher:**
> Die Maßnahme könnte die Ergebnisse beeinflussen.

---

## DEUTSCHSPEZIFISCHE KI-MUSTER

### 29. ChatGPT-typischer "Sound"

**Problem:** Insbesondere ChatGPT hat einen erkennbaren "Sound": gekünstelt wirkende "Ausgewogenheit" mit wenig Inhalt. Sprachlich einwandfreie, aber gleichförmige Sätze.

**Vorher (gelöschter Wikipedia-Artikel "Basbousa"):**
> Die genaue Herkunft von Basbousa ist nicht eindeutig festgelegt, da es in verschiedenen Ländern des Nahen Ostens weit verbreitet ist. Das süße Gebäck ist in Ländern wie Ägypten, Jordanien, dem Libanon, Palästina und anderen arabischen Ländern beliebt. Basbousa ist ein fester Bestandteil der arabischen Küche und wird zu verschiedenen Anlässen serviert, wie zum Beispiel zu festlichen Feiertagen, Hochzeiten, Familienfeiern oder als Gastgeschenk. Es ist ein Symbol für Gastfreundschaft und wird oft mit einer Tasse Tee oder Kaffee genossen.

**Nachher:**
> Basbousa ist ein Grießkuchen, der in Ägypten, dem Libanon, Jordanien und Palästina verbreitet ist. Er wird in Zuckersirup getränkt und kalt serviert.

**Was den ChatGPT-Sound ausmacht:**
- Jeder Satz leitet denselben Gedanken leicht variiert ein
- "ist nicht eindeutig festgelegt" statt einfach "ist unklar"
- Aufblähung durch Aufzählung von Anlässen, die nichts zur Sache tun
- "Symbol für Gastfreundschaft" - typische Bedeutungsaufblähung
- "wird oft mit einer Tasse Tee oder Kaffee genossen" - Werbesprache

---

### 30. Anglizistische Konstruktionen in deutschen Texten

**Problem:** Da Sprachmodelle überwiegend auf englischsprachigen Texten trainiert werden, schleichen sich anglizistische Konstruktionen ein, die im Deutschen unnatürlich wirken. Auch ein plötzlicher Wechsel zwischen verschiedenen Sprachregistern (z.B. von umgangssprachlich zu hochformal) ist auffällig.

**Typische Anzeichen:**
- Englische Satzstruktur (Subjekt-Verb-Objekt ohne Inversion nach Adverbien)
- Übermäßiger Gebrauch von Passivkonstruktionen
- "In X" statt "Im Jahr X" oder "Seit X"
- Wörtlich übersetzte englische Redewendungen

---

### 31. Markdown-Artefakte

**Problem:** KI-Chatbots sind auf Markdown als Ausgabeformat programmiert. Wenn Texte aus einem Chatbot kopiert werden, bleiben Markdown-Fragmente stehen: `#` für Überschriften, `**text**` für Fettschrift, `- ` für Listen, `---` für Trennlinien. Diese haben in normalem Fließtext nichts verloren.

**Vorher:**
> Die Stadt hat **drei Hauptindustrien**: - Tourismus - Landwirtschaft - Fertigung. Mehr Infos unter [der offiziellen Seite](https://example.com).

**Nachher:**
> Die Stadt hat drei Hauptindustrien: Tourismus, Landwirtschaft und Fertigung.

---

### 32. ChatGPT-Suchreferenzen

**Problem:** ChatGPT kann "Gehe zu Suche Nr." (manchmal umgeben von Unicode-Punkten) am Ende von Sätzen einfügen. Dies sind Stellen, wo der Chatbot auf eine externe Website verlinkt hat. Auch Konstruktionen wie "RC-Network.de+1ROTOR Magazin+1" sind typische Artefakte der ChatGPT-Suchfunktion.

**Vorher:**
> Die Europäische Modellflug-Union wurde 1969 gegründet und vertrat rund 180.000 Modellflieger. RC-Network.de+1ROTOR Magazin+1

**Nachher:**
> Die Europäische Modellflug-Union wurde 1969 gegründet und vertrat rund 180.000 Modellflieger.

---

## Ablauf

1. Den Eingabetext sorgfältig lesen
2. Alle Instanzen der oben genannten Muster identifizieren
3. Jede problematische Stelle umschreiben
4. Sicherstellen, dass der überarbeitete Text:
   - Sich natürlich anhört, wenn man ihn laut liest
   - Die Satzstruktur natürlich variiert
   - Konkrete Details statt vager Behauptungen verwendet
   - Den zum Kontext passenden Ton beibehält
   - Einfache Konstruktionen (ist/sind/hat) verwendet, wo angemessen
   - Keine gleichförmigen Satzlängen hat
5. Die humanisierte Version präsentieren

## Ausgabeformat

Liefere:
1. Den umgeschriebenen Text
2. Eine kurze Zusammenfassung der vorgenommenen Änderungen (optional, wenn hilfreich)

---

## Vollständiges Beispiel

**Vorher (KI-klingend):**
> Tolle Frage! Hier ist ein Aufsatz zu diesem Thema. Ich hoffe, das hilft!
>
> KI-gestütztes Programmieren dient als anhaltendes Zeugnis für das transformative Potenzial großer Sprachmodelle und markiert einen wegweisenden Moment in der Entwicklung der Softwareentwicklung. In der sich rasant wandelnden technologischen Landschaft von heute verändern diese bahnbrechenden Werkzeuge - eingebettet an der Schnittstelle von Forschung und Praxis - grundlegend, wie Ingenieure konzipieren, iterieren und ausliefern, was ihre zentrale Rolle in modernen Arbeitsabläufen unterstreicht.
>
> Im Kern ist das Wertversprechen klar: Prozesse optimieren, Zusammenarbeit verbessern und Abstimmung fördern. Es geht nicht nur um Autovervollständigung; es geht darum, Kreativität im großen Maßstab freizusetzen und sicherzustellen, dass Organisationen agil bleiben und gleichzeitig nahtlose, intuitive und leistungsstarke Erfahrungen für Nutzer liefern. Das Tool dient als Katalysator. Der Assistent fungiert als Partner. Das System steht als Fundament für Innovation.
>
> Branchenbeobachter haben festgestellt, dass die Akzeptanz sich beschleunigt hat - von Hobby-Experimenten zu unternehmensweiten Rollouts, von Einzelentwicklern zu funktionsübergreifenden Teams. Die Technologie wurde in der Süddeutschen Zeitung, im Spiegel und bei Heise vorgestellt. Darüber hinaus zeigt die Fähigkeit, Dokumentation, Tests und Refactorings zu generieren, wie KI zu besseren Ergebnissen beitragen kann, was das komplexe Zusammenspiel von Automatisierung und menschlichem Urteilsvermögen hervorhebt.
>
> - 💡 **Geschwindigkeit:** Die Codegenerierung ist deutlich schneller, reduziert Reibung und ermächtigt Entwickler.
> - 🚀 **Qualität:** Die Ausgabequalität wurde durch verbessertes Training gesteigert, was zu höheren Standards beiträgt.
> - ✅ **Akzeptanz:** Die Nutzung wächst weiter, was breitere Branchentrends widerspiegelt.
>
> Obwohl konkrete Details basierend auf verfügbaren Informationen begrenzt sind, könnte man möglicherweise argumentieren, dass diese Werkzeuge einen gewissen positiven Effekt haben könnten. Trotz Herausforderungen, die typisch für aufkommende Technologien sind - einschließlich Halluzinationen, Bias und Verantwortlichkeit - floriert das Ökosystem weiter. Um dieses Potenzial voll auszuschöpfen, müssen Teams sich an Best Practices orientieren.
>
> ## Fazit
> Zusammenfassend lässt sich sagen, dass die Zukunft rosig aussieht. Spannende Zeiten liegen vor uns, während wir diese Reise zur Exzellenz fortsetzen. Lassen Sie es mich wissen, wenn Sie einen Abschnitt vertiefen möchten!

**Nachher (humanisiert):**
> KI-Programmierassistenten beschleunigen manche Aufgaben. In einer Google-Studie von 2024 erledigten Entwickler mit Codex einfache Funktionen 55% schneller als eine Kontrollgruppe, zeigten aber keine Verbesserung beim Debuggen oder bei Architekturentscheidungen.
>
> Die Tools sind gut bei Boilerplate: Konfigurationsdateien, Test-Gerüste, repetitive Refactorings. Sie sind schlecht darin zu merken, wenn sie falsch liegen. Ich habe schon massenhaft Vorschläge akzeptiert, die kompilierten, den Linter bestanden und trotzdem das Falsche taten - weil ich aufgehört hatte aufzupassen.
>
> Mira, eine Entwicklerin bei einem Fintech-Startup, die ich interviewt habe, sagte, sie benutze Copilot "wie Autovervollständigung für langweiligen Code", prüfe aber jede Zeile vor dem Commit. Jake, ein Senior-Entwickler bei einem größeren Unternehmen, hat es abgeschaltet, nachdem es ständig Patterns aus einer veralteten internen Bibliothek vorschlug.
>
> Die Produktivitätsbehauptungen sind schwer zu überprüfen. GitHub sagt, Copilot-Nutzer "akzeptieren 30% der Vorschläge", aber Akzeptanz ist nicht Korrektheit, und Korrektheit ist nicht Mehrwert. Die Uplevel-Studie von 2024 fand keinen statistisch signifikanten Unterschied im Pull-Request-Durchsatz zwischen Teams mit und ohne KI-Assistenten.
>
> Nichts davon heißt, dass die Tools nutzlos sind. Es heißt, dass sie Werkzeuge sind. Sie ersetzen kein Urteilsvermögen, und sie machen Tests nicht überflüssig. Wer keine Tests hat, kann nicht beurteilen, ob der Vorschlag richtig ist.

**Vorgenommene Änderungen:**
- Chatbot-Artefakte entfernt ("Tolle Frage!", "Ich hoffe, das hilft!", "Lassen Sie es mich wissen...")
- Bedeutungsaufblähung entfernt ("Zeugnis", "wegweisender Moment", "sich wandelnde Landschaft", "zentrale Rolle")
- Werbliche Sprache entfernt ("bahnbrechend", "eingebettet", "nahtlos, intuitiv und leistungsstark")
- Vage Zuschreibungen ("Branchenbeobachter") durch konkrete Quellen ersetzt (Google-Studie, namentlich genannte Entwickler, Uplevel-Studie)
- Oberflächliche Partizipphrasen entfernt ("unterstreichend", "hervorhebend", "widerspiegelnd", "beitragend zu")
- Negative Parallelismen entfernt ("Es geht nicht nur um X; es geht um Y")
- Dreierregel-Muster und Synonym-Karussell entfernt ("Katalysator/Partner/Fundament")
- Falsche Spannen entfernt ("von X zu Y, von A zu B")
- Gedankenstriche, Emojis, Fettschrift-Header und typographische Anführungszeichen entfernt
- Kopula-Vermeidung entfernt ("dient als", "fungiert als", "steht als") zugunsten von "ist"/"sind"
- Übermäßige Konjunktionen entfernt ("Darüber hinaus")
- Fazit-Abschnitt komplett gestrichen
- Abschnitts-Zusammenfassung entfernt ("Zusammenfassend lässt sich sagen")
- Besinnliche Schlussbetrachtung entfernt ("die Zukunft sieht rosig aus", "spannende Zeiten liegen vor uns")
- Wissens-Stichtag-Absicherung entfernt ("Obwohl konkrete Details begrenzt sind...")
- Übertriebene Absicherung entfernt ("könnte möglicherweise argumentiert werden, dass... einen gewissen")
- Füllphrasen entfernt ("Um ... voll auszuschöpfen", "Im Kern")
- Medien-Namedropping durch konkrete Behauptungen aus konkreten Quellen ersetzt
- Einfache Satzstrukturen und konkrete Beispiele verwendet

---

## Referenz

Dieser Skill basiert auf:
- [Wikipedia:Anzeichen für KI-generierte Inhalte](https://de.wikipedia.org/wiki/Wikipedia:Anzeichen_f%C3%BCr_KI-generierte_Inhalte) (deutsche Wikipedia, gepflegt vom WikiProjekt KI und Wikipedia)
- [Wikipedia:WikiProjekt KI und Wikipedia/Erkennung ungeprüfter KI-Einsatz](https://de.wikipedia.org/wiki/Wikipedia:WikiProjekt_KI_und_Wikipedia/Erkennung_ungepr%C3%BCfter_KI-Einsatz) (Erkennungsmerkmale und Falldokumentation)
- [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (englische Wikipedia, WikiProject AI Cleanup)

Zentrale Erkenntnis aus Wikipedia: "LLMs verwenden statistische Algorithmen, um zu erraten, was als Nächstes kommen sollte. Das Ergebnis tendiert zum statistisch wahrscheinlichsten Ergebnis, das auf die größte Vielfalt von Fällen zutrifft."
