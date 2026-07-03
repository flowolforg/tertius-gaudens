# Wo soll *The AI Scientist* landen — und wann?

*Der Titel spielt auf* The AI Scientist *[11] an; das Argument (§3.5) lautet, dass ein solches System nicht auf der richtungseröffnenden Rolle landen sollte, nach der es greift, sondern auf den verifizierbaren Rollen — und zu wissen,* wann*, ist die halbe Aufgabe.*

### Die Evolution neuronaler Scaling Laws als durchgearbeiteter Fall, und eine Methode zum Timing automatisierter Forschung

**Autor:** Philipp von Hilgers
**Begleit-Repository:** https://github.com/flowolforg/tertius-gaudens (alle Daten, Skripte, Zwischen-Dumps — §10)
**Datenstand:** Zitations-/Discourse-Snapshot co-datiert ~Januar 2025; Fallpaper 2020–2024.
*(English version: [PAPER.md](PAPER.md))*

---

## 1. Einleitung: ein Fall und eine Frage

Automatisierte Forschungssysteme werden schnell besser, aber die strategische Frage ist weniger „kann eine KI forschen?" als **„an welcher Stelle im Lebenszyklus einer Idee sollte sie ansetzen?"** Die Literatur eines Feldes ist eine Folge von Zügen — jemand eröffnet eine Richtung, jemand korrigiert sie, jemand auditiert die Korrektur, jemand löst sie ab. Diese Züge sind nicht gleich schwer, gleich riskant oder gleich automatisierbar. Den richtigen zu wählen ist das ganze Spiel.

Wir machen die Frage an einem Fall konkret, dessen Bogen nun vollständig sichtbar ist: **neuronale Scaling Laws.** Vier Paper definieren ihn.

- **Kaplan et al. [1]** — *Scaling Laws for Neural Language Models* (2020).
- **Hoffmann et al. [3]** — *Training Compute-Optimal LLMs* (Chinchilla; 2022).
- **Besiroglu et al. [4]** — *Chinchilla Scaling: A Replication Attempt* (2024).
- **DeepSeek-AI [5]** — *DeepSeek LLM* (2024).

Rückblickend: **an welcher dieser Stellen hätte ein KI-Wissenschaftler am besten beitragen können?** Wir argumentieren: bei Besiroglu und DeepSeek — der *Re-Analyse* und der *Re-Optimierung* — und *nicht* bei Kaplan oder Hoffmann, der *Richtungseröffnung* und der *Neue-Experimente-Korrektur*. §2 fasst zusammen, was jedes Paper tatsächlich beigetragen hat; §3 abstrahiert die vier Rollen zu einem übertragbaren Konzept und benennt die genaue Achse (verifizierbare vs. spekulative Neuheit); §4 zeigt, wie die Kette aus der Rohliteratur gewonnen wird — mit deterministischer Bibliometrie und *einem* gezielten KI-Schritt; §5 definiert die Schwellen, deren Überschreiten der *Startschuss* ist; §6 analysiert Rolle für Rolle, was in Reichweite liegt und was nicht; §7 skizziert die entstehende Forschungslandschaft; §8 wendet den Rahmen auf dieses Paper selbst an.

Der Sinn des Falls ist nicht der Fall. Es ist, dass dieselbe Struktur — Eröffner, Korrektor, Auditor, Optimierer — feldübergreifend wiederkehrt, sodass eine Methode, die diese Rollen bei den Scaling Laws lokalisiert, auf *aktive* Fronten gerichtet werden kann, um den Einstieg prospektiv zu timen.

---

## 2. Vier Erkenntnisse: was Kaplan, Hoffmann, Besiroglu und DeepSeek tatsächlich etabliert haben

| Paper (Jahr) | Erkenntnisgewinn | Rolle | Modus |
|---|---|---|---|
| **Kaplan** [1] (2020) | Der Loss fällt *vorhersagbar* mit Compute, Parametern und Daten als Potenzgesetz — Modellleistung wird *vor* dem Training prognostizierbar. | **A** — eröffnet die Richtung | spekulativ |
| **Hoffmann / Chinchilla** [3] (2022) | Kaplans Allokation war suboptimal; für ein festes Compute-Budget sollten Parameter und Trainings-Tokens *etwa gleich* skalieren. Belegt durch Training von 400+ Modellen. | **B-novel** — korrigiert die Formel | spekulativ |
| **Besiroglu** [4] (2024) | Re-analysierte Chinchillas *eigene publizierte Daten* und fand den berichteten parametrischen Fit statistisch inkonsistent (unplausibel enge Intervalle; nicht reproduzierbar). Kein neues Training. | **B-audit** — auditiert den Korrektor | verifizierbar |
| **DeepSeek** [5] (2024) | Basierte die Skalen-Variable auf *non-embedding FLOPs/Token* neu (statt Parameterzahl) → sauberere, übertragbarere Scaling-Fits und praktisches Hyperparameter-Scaling. | **C** — re-optimiert den Rahmen | verifizierbar |

Kaplan et al. (2020) [1] zeigten erstmals systematisch, dass der Loss von Sprachmodellen über mehrere Größenordnungen hinweg Potenzgesetzen folgt — in Modellgröße (Non-Embedding-Parameter), Datenmenge und Trainings-Compute. Daraus folgte: Modellleistung ist vor dem Training prognostizierbar, und für ein wachsendes Compute-Budget sollte man die Parameterzahl deutlich schneller skalieren als die Datenmenge (N_opt ∝ C^0.73). Das Paper eröffnete die Richtung: Leistung als berechenbare Funktion der Investition.

Hoffmann et al. (2022) [3] vermaßen die Frontier neu — mit über 400 trainierten Modellen und drei unabhängigen Schätzverfahren. Ergebnis: Kaplans Allokation war suboptimal; Parameter und Trainings-Tokens sollten etwa gleich skalieren (N_opt ∝ C^0.5). Der Beleg war Chinchilla (70 Mrd. Parameter), das bei gleichem Compute-Budget das viermal größere Gopher übertraf.

Besiroglu et al. (2024) [4] rekonstruierten die Datenpunkte aus Hoffmanns publizierten Abbildungen und versuchten, dessen drittes Schätzverfahren zu replizieren. Befund: Die berichteten Parameter sind mit den beiden anderen Verfahren inkonsistent, und die Konfidenzintervalle sind unplausibel eng (über 600.000 Experimente nötig, gelaufen wohl unter 500). Der eigene Re-Fit (α = 0,35, β = 0,37) versöhnt Verfahren 3 mit 1 und 2. Kein neues Training: ein Audit publizierter Zahlen.

DeepSeek-AI (2024) [5] untersuchte die Scaling Laws im Zuge des Trainings von DeepSeek LLM neu: Modellskala als Non-Embedding-FLOPs pro Token statt Parameterzahl, Neu-Fit der Allokation (Optimum hängt von der Datenqualität ab), Hyperparameter als Formeln des Compute-Budgets. Zugleich hält das Paper den fehlenden Konsens früherer Arbeiten fest — genau das Signal, das unser Diskursfilter aufgreift.

Von oben nach unten gelesen ist die Kette eine Dialektik: eine kühne Behauptung (A), eine bestätigende Korrektur, die „die richtige Formel" landet (B-novel), ein nüchterner Audit, der die Korrektur selbst als fehlerhaft entlarvt (B-audit), und eine Re-Optimierung, die den ganzen Aufbau von innen ablöst (C). Kaplan und Hoffmann greifen *über* den gesicherten Bestand hinaus; Besiroglu und DeepSeek arbeiten *innerhalb*. Dieser Unterschied ist der Angelpunkt des Papers.

---

## 3. Das Konzept: die *tertius-gaudens*-Triade und die verifizierbar/spekulativ-Achse

### 3.1 Die de-riskende Dialektik

Anleihe bei Simmels *tertius gaudens* [8] — dem „lachenden Dritten", der aus der Konstellation zweier anderer Nutzen zieht — lesen wir die Kette als strukturelle Gelegenheit (eng verwandt mit Burts Structural Holes [9]). Wird ein Landmark **A** von einem starken **B** *bestätigt und korrigiert*, ist die Richtung **de-riskt** (vom Risiko befreit): sie ist nun als bedeutsam erkannt *und* hat eine präzise, wohlgestellte Form. Ein dritter Akteur **C** kann dann die radikale Optimierung ausführen, zu der das formalisierte Problem einlädt. Anders als Simmels Rivalität ist dies dialektisch — A ist These, B die bestätigend-korrigierende Antithese, und die synthese-förmige Öffnung ist die Beute. Der Dritte ergreift keine Partei; er erntet die **Gewissheit**, die A und B gemeinsam erzeugt haben.

### 3.2 Die eigentliche Achse ist verifizierbare vs. spekulative Neuheit

Die naive Rahmung fragt „soll die KI A, B oder C spielen?" — eine Frage der Rolle. Die richtige Achse ist **nicht „wie kreativ", sondern „wie verifizierbar zum Zeitpunkt der Tat".** Die Behauptung ist *nicht*, dass die automatisierbaren Züge unkreativ seien: DeepSeeks Wahl eines non-embedding-FLOPs-Maßes war echt und nicht offensichtlich. Die Behauptung betrifft die erkenntnistheoretische Struktur:

- **Für C und B-audit existiert ein Orakel, für A und B-novel nicht.** Sobald B den Rahmen gelandet hat, ist die Zielfunktion formalisiert (Compute = f(Parameter, Tokens), eine explizite Frontier) und der Maßstab fixiert (Loss-Kurven). Cs Beitrag ist *im Moment des Versuchs prüfbar*; Besiroglus Audit ist gegen Hoffmanns publizierte Zahlen prüfbar. Kaplan musste den Maßstab erst erfinden — nichts zu prüfen; Hoffmanns Allokation entschied sich erst Jahre später. C und B-audit schaffen auf der *entscheidbaren* Seite der Linie; A und B-novel wetten auf unentschiedenem Terrain.
- **Suche ersetzt Einsicht nur, wo ein Orakel existiert.** Das ist der Kern. Cs schöpferische Wahl — welche Re-Parametrisierung man versucht — ist nicht mechanisch ableitbar, aber sie ist **durch Breite × Verifikation ersetzbar**: die natürlichen Compute-Maße durchprobieren, die Loss-Kurven entscheiden lassen. Wo ein Mensch Einsicht zum Raten brauchte, kann eine Maschine probieren-und-prüfen. A hat zu diesem Zeitpunkt keinen Prüfer; dort kann Suche die Einsicht nicht ersetzen.
- **Begrenztes vs. unbegrenztes Scheitern.** Ein falsches C gewinnt bloß nicht (lokal, behebbar). Ein falsches A kollabiert seine eigene Prämisse; ein falsches B-novel führt das ganze Feld in die Irre. Verifizierbare Neuheit hat einen begrenzten Nachteil; spekulative nicht.

Als Spektrum:

```
   A    ────────   B-novel   ────────   C    ────────   B-audit
postuliert         postuliert ein     optimiert       prüft
den Rahmen         Gesetz im Rahmen   im Rahmen        den Rahmen
kein Orakel        Orakel erst später Orakel jetzt     Orakel jetzt
└──── spekulativ: Einsicht nötig ─────┘└── verifizierbar: Suche ersetzt ───┘
```

**Ehrliche Grenze.** Das Argument beruht darauf, dass der Raum nützlicher Re-Parametrisierungen *klein und durchsuchbar genug* ist, damit das Orakel den Treffer findet. Für Skalen-*Maße* (endlich viele natürliche Compute-Definitionen) ist das plausibel; für einen wirklich nicht-durchsuchbaren architektonischen Sprung rückte C Richtung A und die Behauptung schwächte sich ab.

### 3.3 Das Warten kollabieren

Das löst „warum auf C warten?" auf. Das Warten war ein **Artefakt menschlicher Arbeitsteilung** — Kaplan→…→DeepSeek dauerte vier Jahre, weil vier Akteure nacheinander zogen. Aber B-audit und C sind **dieselbe Maschinen-Fähigkeit**: generieren-und-verifizieren gegen den vorhandenen Bestand. Ein Agent, der ein Landmark auditiert, kann den optimierten Nachfolger *im selben Zug* vorschlagen und die menschliche Lücke in eine Bewegung kollabieren. Er muss nicht auf einen Dritten warten, um die eben erzeugte Gewissheit zu ernten. Off-limits bleibt nur das spekulative Paar, A und B-novel.

### 3.4 Vom Fall zur Methode

Nichts davon ist spezifisch für Scaling Laws. Jedes Feld, das aufzeichnet, *wer wem widerspricht und wie substanziell*, legt dieselbe A→B→C-Struktur offen. Der Rest des Papers baut die Extraktions- und Timing-Methode (§4–§5) und fragt dann, welche Rollen ein automatisierter Agent tatsächlich ausfüllen kann (§6).

### 3.5 Verwandte Arbeit: autonome Ideengenerierung

Das nächstliegende Vorgänger-System ist *The AI Scientist* [11], die erste autonome Pipeline, die ein maschinengeneriertes Paper durch ein Blind-Peer-Review brachte — ein echter Engineering-Meilenstein. Seine **Ideengenerierung** ist jedoch strukturell anders, und der Kontrast schärft, was wir vorschlagen. Dort setzt ein menschliches Code-Template eine iterative Schleife in Gang, in der ein LLM als *Mutations-Operator* ein Archiv von Ideen wachsen lässt; jede Idee trägt *selbst-eingeschätzte* Scores für Interessantheit/Neuheit/Machbarkeit (1–10), und Neuheit wird *erzwungen*, indem Vorschläge verworfen werden, die vorhandener Arbeit zu **semantisch ähnlich** sind (via Semantic-Scholar-API), unter dem Prompt, ein „ambitionierter KI-PhD-Student … der signifikant zum Feld beitragen will" zu sein. Vier Unterschiede folgen:

- **Neuheit als Un-Ähnlichkeit vs. Standing als Disput.** The AI Scientist setzt Neuheit mit *semantischer Distanz* zu vorheriger Arbeit gleich. Aber Distanz ist ein schwacher Wert-Proxy — viel vom Besten liegt *nah* an einem Landmark und bestreitet es gerade deshalb (Chinchilla ist „nah" an Kaplan und zählt, *weil* es ihm widerspricht). Wir lesen das Standing einer Idee nicht aus Ähnlichkeit, sondern aus *wer wen substanziell bestreitet* — eine externe strukturelle Tatsache, keine Selbstauskunft und keine Distanz.
- **Gleiche Datenquelle, entgegengesetzte Nutzung.** Beide stützen sich auf Semantic Scholar. The AI Scientist fragt es nach *Un-Ähnlichkeit* (Overlap vermeiden); wir nutzen seine *In-Text-Zitationskontexte* für *Auseinandersetzung und Disput* — ein selteneres, schärferes Signal (§4.3), das die echten Kritiker eines Landmarks von seinen zeremoniellen Zitierern trennt.
- **Kein Timing.** Template-Mutation läuft im Zeitvakuum; kein Begriff davon, *wann* eine Richtung reif ist. Unsere Methode *ist* Timing — der velocity-basierte Startschuss *t_B* (§5.5), der Moment, in dem eine Richtung de-riskt wird. Eine Idee kann novel-und-machbar, aber verfrüht oder schon abgestanden sein; ein Ähnlichkeits-Check merkt das nicht.
- **Welche Rolle überhaupt automatisierbar ist.** Das Greifen nach „signifikanten, neuen Beiträgen" zielt implizit auf die **A**-Rolle — eine Richtung eröffnen — was *spekulative* Neuheit ohne Orakel ist (§3.2), der am wenigsten automatisierbare Akt. Wir argumentieren, die erreichbaren Rollen sind die *verifizierbaren*, **B-audit und C**, und dorthin sollte die Ideengenerierung gerichtet werden.

Nichts davon schmälert das Engineering; unsere Behauptung ist enger und orthogonal — dass *Ideen-Auswahl und Timing*, gelesen aus der Disput-Struktur des Feldes statt aus selbst-eingeschätzter Neuheit, der Ort ist, an dem ein automatisierter Wissenschaftler Traktion gewinnt. In diesem Sinn beantwortet der Titel des Papers [11]: er benennt, *wo* ein solches System landen sollte (die verifizierbaren Rollen, §6) und *wann* (der velocity-basierte Startschuss, §5.5).

---

## 4. Die Kette aus dem Literaturpool gewinnen

Die Kette wird von einem Such-und-Rangfolge-Algorithmus über dem Zitationsgraphen erzeugt: **deterministische Bibliometrie** (kein Modell, voll reproduzierbar) plus **ein eng begrenzter KI-Schritt** — die In-Text-Stance je Kante — beim Ingest vorberechnet. Die KI bewusst auf dieses eine Urteil zu beschränken ist Absicht: alles andere ist auditierbare Arithmetik. Eine Referenzimplementierung liegt dem Paper bei (§10).

### 4.1 Quellen

- **arXiv (Informatik).**[^arxiv] Kategorien `cs.CV, cs.LG, cs.CL, cs.AI, cs.NE, cs.RO` → **314.690 Paper** (`title, abstract, year, publicationdate, citationcount`). Tagesgenaues `publicationdate` zählt: in 49 unserer 100 Kandidaten-Triaden teilen A und B ein *Jahr*.
- **Semantic-Scholar-Zitationsgraph** [7]. **4.299.126 Zitationskanten** — und, entscheidend, **In-Text-Zitationskontexte**: `contextcount`, die Zahl der distinkten In-Text-Stellen, an denen ein zitierendes Paper das zitierte aufgreift, plus die rohen Kontext-Strings für eine 60.343-Kanten-Teilmenge.

### 4.2 Der Selektions-Algorithmus

Zwei Graph-Größen treiben den Algorithmus, und eine bloße Zitationszahl ist keine davon:

- **`contextcount`** — wie viele distinkte In-Text-Stellen ein zitierendes Paper dem zitierten widmet. Ein Paper einmal, im Vorbeigehen zu zitieren ist zeremoniell; es *wiederholt* zu zitieren ist anhaltende Auseinandersetzung.
- **stance** — ob diese In-Text-Stellen das zitierte Paper *bestreiten*. Dies ist die eine KI-beurteilte Größe (§4.7): eine reine Zählung kann „[KMH20] irrt bei X" nicht von „unter Verwendung der Exponenten von [KMH20]" unterscheiden.

Der Algorithmus hat drei Stufen:

1. **Landmark A gewinnen — durch Monitoring, nicht durch Suche.** Das autonome System sucht keinen Seed; es **überwacht den gesamten Korpus** und markiert jedes Paper, das die Landmark-Schwelle überschreitet — Rezeption `≥ θ_A` (prospektiv: Zitations-*Velocity* über dem Feld; §5.5). A wird *erkannt, wie es auftaucht*, nicht angefordert. (Will ein Mensch einen *bekannten* Seed inspizieren, funktioniert auch semantische Suche — Query einbetten und nach `0.7·cosine(query, paper) + 0.3·min(1, citationcount/1000)` ranken — aber das ist ein Komfort, nicht der Start des Algorithmus.) Hier ist der erkannte Seed Kaplan.
2. **Die substanziellen Kritiker auswählen.** Unter den *tausenden* Papern, die A zitieren, nur die behalten, die A sowohl **wiederholt aufgreifen** (`contextcount ≥ 3`) als auch **bestreiten** (`disagreement = true`). Die meisten Zitationen erfüllen keines von beidem, also ist dies ein harter Schnitt.
3. **Nach Reichweite ranken.** Die Überlebenden nach `citationcount` ordnen, `contextcount` als Tiebreaker: Das Fokus-Signal trägt bereits das Gate (Stufe 2); das Ranking fragt nur noch, wie breit der Kritiker selbst rezipiert wird.

Auf Kaplan angewendet, liefert Stufe 3 **Hoffmann auf Rang 1 und DeepSeek auf Rang 3** — nicht weil jemand kuratiert hätte, sondern weil beide Kaplan *viele Male* referenzieren (`contextcount` 10 und 7) *und* das tun, um *einen Fehler zu finden* (`disagreement = true`). Aus ~3.000 Kaplan-Zitierern hebt der Algorithmus den kanonischen Korrektor des Feldes (Hoffmann, B-novel) und einen späteren Re-Optimierer (DeepSeek, C); §4.4 prüft diese Ausgabe gegen den Enzyklopädie-Kanon und markiert, wo sie hält und wo nicht. Das Verfahren ist deterministisch bei gegebenem Encoder und Stance-Labels; §4.3 zeigt den Trichter numerisch.

Die Kette spannt jedoch **zwei Anker**. Kaplans Kritiker liefern Hoffmann *und* DeepSeek — beide zitieren und bestreiten Kaplan. Aber der Auditor **Besiroglu zitiert Kaplan gar nicht** (keine Kante im Graphen); es bestreitet *Hoffmann* (`contextcount = 10`). Also kann Besiroglu nicht in Kaplans Liste erscheinen; es taucht erst auf, wenn dieselben zwei Scores **mit Hoffmann als neuem Seed erneut angewendet** werden. Die Vier-Knoten-Kette ist daher eine *Traversierung mit Anker-Wechsel* — Kaplan → {Hoffmann, DeepSeek}, dann Re-Seed auf Hoffmann → {Besiroglu} — kein einzelnes Ranking (§4.5).

### 4.3 Der Score-Trichter: alle Paper überwachen, nicht nach einem suchen

Das autonome System beginnt nicht mit einer Query. Es **beobachtet den gesamten Korpus** und lässt ein A→B-Paar *emergieren*: ein Paper, das die Landmark-Schwelle überschreitet (ein *Kaplan-artiges* A), dann ein qualifiziertes Paper, das es bestreitet (ein *Hoffmann-artiges* B). Semantische Suche (§4.2) ist nur, wie ein Mensch einen *gewählten* Seed inspiziert; der Start des Monitors ist der volle 314.690-Paper-Pool. So gefasst ist die Kette die Ausgabe eines Trichters über alles:

| Stufe | Filter (Score / Gate) | Menge |
|---|---|---|
| Start | jedes Paper überwachen | **314.690** |
| ① Landmark-Kandidat-Detektion | Rezeption `≥ θ_A` (`citationcount ≥ 1000`; prospektiv: Velocity über dem Feld, §5.5) | **326** Landmark-Kandidaten — Kaplan darunter |
| — | einen Kandidaten wählen, A = Kaplan → seine Zitierer | **3.031** Paper zitieren Kaplan |
| ② Discourse-Gate | Kante *analysiert* **∧** `disagreement = true` **∧** `contextcount ≥ 3` | 3.031 → *322 analysiert (10,6 %)* → **28** qualifizierte Kritiker |
| ③ Salienz-Rang | `citationcount` (Reichweite; `contextcount` als Tiebreaker) | **Hoffmann #1**, Henighan #2, **DeepSeek #3** |

Dem System wird nie *gesagt*, auf Kaplan zu schauen: Kaplan taucht selbst auf, indem es ① überschreitet, und Hoffmann taucht auf, indem es ②–③ überschreitet. Zwei der Schnitte leisten die eigentliche Arbeit, und beide sind bibliometrisch, nicht semantisch:

- **Das Discourse-Gate ② ist der harte Filter — aber aus zwei verflochtenen Gründen, und einer ist eine Grenze, keine Tugend.** Der Kollaps 3.031 → 28 zerlegt sich: nur **322 (10,6 %)** von Kaplans Zitierern wurden vom Discourse-Durchlauf überhaupt je *analysiert*; von diesen tragen **36 (11,2 % der analysierten)** `disagreement = true`; `contextcount ≥ 3` lässt 32, und die im-Korpus-Rezeption, die die Rangfolge braucht, lässt **28**. Der ~100×-Schnitt ist also **Coverage × Seltenheit, nicht Seltenheit allein** — grob ein 10×-Faktor ist schlicht, dass ~89 % der Zitierer nie gelabelt wurden (§4.5, §5.3). Richtig gelesen ist die Basisrate Disagreement pro *analysierter* Kante — **5,2 % global, 11,2 % bei Kaplan** — nicht pro allen Kanten, da ~84 % überhaupt nie untersucht wurden: ungewöhnlich-aber-nicht-verschwindend *dort, wo das Feld tatsächlich hinschaut*. Zwei ehrliche Konsequenzen folgen: das Gate ist blind für jeden nie analysierten Disput, und die Analyse ist selbst zu prominenten Papern verzerrt (Label-Rate steigt 5,6 % → 30,9 % mit der Zitationszahl des zitierten Papers, §5.3), sodass die Methode bevorzugt *prominente* Dispute zutage fördert. Wo Disagreement *gelabelt* ist, ist es allerdings echt engagiert — nur **1,7 %** der Disagreement-Kanten sind Einzel-Kontext gegenüber **60,5 %** über alle Kanten, und `cc ≥ 3` behält 74,9 % von ihnen; dieser Teil des Filters ist sauber.
- **Der Salienz-Rang ③ ordnet, was übrig bleibt**, nach Reichweite — `citationcount`, mit `contextcount` als Tiebreaker; der Fokus hat seine Arbeit im Gate ② getan. Hoffmann führt (1.571 Zitationen) vor Henighan (345); DeepSeek (181) landet auf Rang 3 — noch vor stärker fokussierten, aber schmaler rezipierten Kritikern wie *Unified Scaling Laws for Routed Language Models* (148).

Also ist **Kaplan → Hoffmann → DeepSeek gleich A (①) → B (③#1) → C (③#3) einer deterministischen Kaskade** — kein Themen-Clustering, kein LLM im Ranking, keine Query. Die Verbindung dreier Paper, unsichtbar in einer 314.690-Zeilen-Tabelle, wird durch Monitoring plus drei Scores sichtbar gemacht. (Henighan sitzt auf #2 in einem *anderen* Thema; §5.2 kommt darauf zurück.) Ein zweiter, schärferer Grund als das Thema: Henighan ist gar kein *externer* Kritiker — [1] und [2] teilen sich die Kernautoren (Kaplan, Henighan), das gelabelte Disagreement ist eine Selbst-Verfeinerung von As eigenem Team. Simmels Triade braucht verschiedene Akteure; das Gate sollte einen Autoren-Disjunktheits-Filter erhalten (`authors(A) ∩ authors(B) = ∅`), deterministisch prüfbar, der Henighan regulär aussortierte.

Ein Vorbehalt rahmt alles Folgende: Stufe ① und der Salienz-Score ③ lesen *Lebenszeit*-Zitationszahlen, **eingefroren zum ~Januar-2025-Snapshot**. Diese Kaskade ist also **retrospektiv** — sie rekonstruiert eine abgeschlossene Episode aus dem Rückblick, wenn die Paper bereits berühmt sind. Sie zeigt die *Form* der Kette, nicht *wann* der Monitor gefeuert hätte. §5.5 tauscht Lebenszeit-Zahlen gegen Zitations-**Velocity**, um die prospektive Frage zu stellen: wie früh hätte ein Live-Monitor dieselbe Kette erkannt — das Kaplan-artige A, dann das Hoffmann-artige B?

### 4.4 Die Filter rekonstruieren die kanonische Wirbelsäule des Feldes

Erfindet dieses Scoring eine Verbindung, oder *findet* es eine reale? Der externe Check ist Wikipedias Artikel *Neural scaling law* [10], der unabhängig genau **Kaplan [1] → Hoffmann/Chinchilla [3] → Besiroglu [4]** kanonisiert — alle drei mit ihren konkurrierenden Exponenten behandelnd (Kaplan `N_opt ∝ C^0.73`; Chinchilla `α=0.34, β=0.28, N_opt ∝ C^0.5`; Besiroglus revidierte `α=0.35, β=0.37`). Das ist genau die **A → B-novel → B-audit-Wirbelsäule** unserer Kette, von den Filtern rekonstruiert, ohne Werkzeug im Loop. Starker Beleg, dass die Scores echte Relevanz treffen statt Verbindungen zu erfinden — und das rechtfertigt, dieselben Scores *prospektiv* anzuwenden.

**Bei C divergieren Werkzeug und Enzyklopädie — und die Divergenz ist aufschlussreich.** DeepSeek steht nicht in jenem Artikel, aber der Disput ist real in den Daten: `DeepSeek → Kaplan` ist ein *gelabelter* Disput über **7 distinkte In-Text-Stellen** (`contextcount = 7`) — eine substanzielle Auseinandersetzung, die der Algorithmus nicht erfunden hat. Die Lücke ist eine der **Linse, nicht der Fakten**. Wikipedia ordnet Scaling Laws nach der *Fit-Lineage* — dem parametrischen Modell `L = A/N^α + B/D^β` und seinen Exponenten — einem Faden, auf dem Kaplan, Chinchilla und Besiroglu eine geschlossene Linie bilden und DeepSeeks Beitrag (das non-embedding-FLOPs-*Maß*) auf einer anderen Achse sitzt. Der Algorithmus ordnet nach *Diskurs* — wer wen substanziell bestreitet — und auf dieser Achse gehört DeepSeek eindeutig dazu. Die Auslassung der Enzyklopädie ist also kein Beleg, dass die Verbindung falsch ist; es ist ein Fall einer Diskurs-Verbindung, die eine Themen-Lineage-Erzählung nicht erfasst. Das ist näher am *Sinn* des Werkzeugs als an seinem Versagen: reale Dispute sichtbar zu machen, die die kanonische Rahmung übersieht. Der ehrliche Rest ist nur, dass „gehört per Diskurs dazu" und „als Fit-Lineage-Landmark kanonisiert" verschiedene Bedeutungen von Dazugehören sind — wir beanspruchen die erste für C und merken an, dass das Feld die zweite (noch) nicht gewährt hat.

*Ehrlicher Geltungsbereich.* Dies ist ein einzelner bekannter Fall; dass die Filter-Ausgabe mit der Wirbelsäule der Enzyklopädie übereinstimmt, ist hier überzeugend, aber selbst die Hypothese, die eine breitere Mehr-Felder-Evaluation erst prüfen müsste.

### 4.5 Die Labels in den Daten — und wo die Coverage-Lücke beißt

Unter jener Rangfolge sind die Sentiment-Labels nur partiell. Wir haben die Vier-Knoten-Kette kantenweise gegen den Graphen verifiziert:

| Kante | In-Text `contextcount` | Sentiment-Label |
|---|---:|---|
| Kaplan → Hoffmann | 10 | **disagreement = true** |
| DeepSeek → Kaplan | 7 | **disagreement = true** |
| DeepSeek → Hoffmann | 7 | keines (unlabeled) |
| **Besiroglu → Hoffmann** | **10** | **keines (unlabeled)** |
| Besiroglu → Kaplan | — | **keine Kante** (Re-Ankerung nötig, §4.2) |

Die *strukturelle* Kette ist vollständig und ihr `contextcount`-Gate deterministisch — jede existierende Kante ist mit ihrem In-Text-Gewicht vorhanden, und die starke Auseinandersetzung (cc = 10) der Audit-Kante Besiroglu→Hoffmann ist klar sichtbar. Die letzte Zeile ist der Grund, warum die Kette Re-Ankerung braucht: ohne Besiroglu→Kaplan-Kante ist der Auditor vom Kaplan-Seed aus unsichtbar und erscheint erst, wenn Hoffmann zum Seed wird. Aber der Discourse-Layer (ein LLM-Durchlauf beim Ingest) annotierte nur ~16 % der Kanten (§5.3) und **labelte die zentrale B-audit-Kante nie**, trotz ihres cc = 10. Das ist die Methode im Kleinen: deterministische Bibliometrie fördert Skelett, Rangfolge und Gate zutage; der gezielte Klassifikator muss dann *auf den hoch-contextcount-unlabeled-Kanten laufen*, um die Labels zu vervollständigen. „Unlabeled" heißt „noch nicht analysiert", nicht „keine Kritik" — Besiroglu ist nachdrücklich eine Kritik.

### 4.6 Eine Markov-Formulierung der Verweiskette (Erweiterung)

Die greedy Traversierung aus §4.2 — nimm den obersten Bestreiter, dann re-ankere — lädt zu einer saubereren Formalisierung als **Markov-Kette auf dem Diskurs-Graphen** ein. Seien Zustände Paper, und sei die Übergangswahrscheinlichkeit von einem Paper *p* zu einem Kritiker *q* dessen normalisiertes Reichweiten-Gewicht (`citationcount`) über *p*s qualifizierten Bestreitern:

> P(*p* → *q*) = [contextcount(*q*→*p*) · citationcount(*q*)] ⁄ Σ über *p*s qualifizierte Bestreiter, für *q*, das *p* bestreitet (`disagreement`, `cc ≥ 3`).

Ein Random Walk unter P „schreitet zu dem, der das, wo er gerade steht, am substanziellsten bestreitet", und die implizierte Verweiskette ist ein **Pfad hoher Wahrscheinlichkeit** dieses Walks. Drei Dinge, die die greedy Variante von Hand erledigt, fallen nativ heraus:

- **Re-Ankerung wird automatisch.** Der Walk quert Kaplan → Hoffmann → Besiroglu ohne handkodierten Re-Seed; die fehlende Besiroglu→Kaplan-Kante ist schlicht ein Null-Wahrscheinlichkeits-Übergang, während der Zwei-Hop Kaplan → Hoffmann → Besiroglu Masse trägt.
- **Mehrschritt-Einfluss aggregiert.** Ein über mehrere Disput-Hops erreichbares Paper (DeepSeek bestreitet *beide*, Kaplan und Hoffmann) sammelt Wahrscheinlichkeit aus jeder Route, statt an einen Anker geheftet zu sein.
- **Die offene Front ist eine Menge fast-absorbierender Zustände.** Paper ohne qualifizierte Bestreiter *bisher* leiten wenig Wahrscheinlichkeit weiter — dort staut sich der Walk, d. h. die Kandidaten-C-/Einstiegs-Region, die ein prospektives System beobachten sollte.

Wir markieren dies als Modellierungsrichtung; die Ergebnisse hier nutzen die deterministische Traversierung, die genügt, um die Kette zu zeigen. Eine Markov-Behandlung zählte am meisten *prospektiv* — beim Ranken vieler teilweise überlappender Disput-Pfade über ein ganzes Feld zugleich.

### 4.7 Verwendete Modelle

| Stufe | Modell | Zweck |
|---|---|---|
| Embedding / Retrieval | `all-MiniLM-L6-v2` [6] (384-dim) | semantische Ähnlichkeit über dem Korpus |
| In-Text-Stance beim Ingest | **`gpt-4o-mini`** (OpenAI), via **Batch API**, JSON-Mode, Temperatur 0.1 | `agreement` / `disagreement`-Booleans je Kante + Summaries |
| Themen-Clustering; Per-Kontext-Typ | `claude-opus-4-8` | Kritiker nach Thema gruppieren; CRITICAL/SUPPORTIVE/NEUTRAL je In-Text-Kontext |

Man beachte, dass die selektive, prominenzverzerrte Abdeckung aus §4.3/§5.3 eine Eigenschaft *dieses Ingest-Laufs* ist — welche `(zitiertes Paper, zitierendes Zitat)`-Paare in den Batch-Input kamen — **nicht von `gpt-4o-mini` selbst.** Die 84 % der Kanten ohne Stance wurden schlicht nie in den Batch eingereicht, nicht vom Modell als neutral beurteilt. Eine vollständigere Labelung ist daher rein eine Frage, denselben Batch über die unlabeled hoch-`contextcount`-Kanten (§4.5) erneut laufen zu lassen, zu `gpt-4o-mini`-Batch-Preisen.

---

## 5. Signal-Schwellen: wann sie feuern und warum sie der Startschuss sind

### 5.1 Das Gate

Eine Kritik-Kante B→A wird nur zugelassen, wenn `disagreement = true`, Rezeption `R(A) ≥ θ_A`, `R(B) ≥ θ_R` und Auseinandersetzung `contextcount ≥ θ_C`. Schwellen sind **absolut, nicht relativ**, sodass „ist das schon ein Signal?" korpusweit und über die Zeit vergleichbar ist — die Eigenschaft, die *früh-aber-solide* Kritiken zünden lässt. Kalibrierung auf `papers.citationcount` gibt Perzentile **p90 = 36, p95 = 68, p99 = 223**; wir setzen `θ_A = 1000`, `θ_R = 300` (beide tief im Tail), `θ_C = 3` (behält 74,9 % der Disagreement-Kanten; Rückfall `θ_C = 2` behält 98,3 %).

Zwei weitere Gates, aus §5.4: ein **Typ-Gate** (nur `conceptual_correction` / `scope_limitation` zulassen, nie `benchmark_superiority`) und ein billiger **Genre-Vorfilter** auf As Titel+Abstract. Beide sind Negativ-Screens; keiner ersetzt das Disagreement-Signal.

### 5.2 B auswählen: welche Rangfolge hebt Hoffmann hervor?

Welcher von As qualifizierten Kritikern wird B? Die Wahl der Rangfolge zählt, und es ist aufschlussreich, dass *zwei* deterministische Rangfolgen bereits funktionieren, während eine dritte, verlockende scheitert:

- **Das Reichweiten-Ranking (`citationcount`, `contextcount` als Tiebreaker)** — der Stufe-3-Rang (§4.3) — setzt **Hoffmann an die Spitze** (1.571) und DeepSeek auf Platz drei (181). Die Kette fällt direkt heraus; kein Clustering nötig.
- **Ein naiver Zeit-Selektor** („frühester qualifizierter Kritiker wird B") *scheitert*: er liefert Henighan et al. [2] (2020, Aspect-Ratio), weil ein Landmark an mehreren distinkten Themen angegriffen wird und die global früheste Kritik eine enge Verfeinerung an einem *Neben*-Thema ist.

Themen-Clustering ist also **nicht nötig, um Hoffmann in diesem Fall hervorzuheben** — die Produkt-Rangfolge genügt. Sein Wert ist zweifach und *prospektiv*: (i) es trennt die *Allokations*-Debatte (Hoffmann #1, DeepSeek #3) von Henighans unverwandter *Aspect-Ratio*-Kritik dazwischen, sodass die Kette als *ein* Thema statt drei gelesen wird; und (ii) es tauscht Lebenszeit-`citationcount` gegen **Velocity** (alters-normalisierte Rezeption), das Signal, das ein *Live*-System braucht, bevor Lebenszeit-Zahlen existieren:

| Datum | Kritiker von Kaplan | Velocity (/Jahr, Bezug 2025-01-01) | Thema |
|---|---|---:|---|
| 2022-03-29 | **Hoffmann / Chinchilla** | **569** | Compute/Token-Allokation |
| 2024-01-05 | DeepSeek | 183 | Compute/Token-Allokation |
| 2020-10-28 | Henighan (frühester überhaupt) | 83 | Aspect-Ratio |

Das Allokations-Thema ist das umkämpfteste (~10 von Kaplans 28 qualifizierten Kritikern) und das schnellste, sodass Hoffmann sowohl unter Produkt-der-Reichweite (retrospektiv) als auch unter Thema×Velocity (prospektiv) führt — und nur der reine Zeit-Selektor lässt sich täuschen.

### 5.3 Disagreement ist selten und selektiv gelabelt

Disagreement ist eine *Nadel* — aber der richtige Nenner zählt (§4.3). **Aus Kostengründen labelte der Ingest-Batch (§4.7) nicht den ganzen Graphen:** nur die Beziehungen von Papern mit mindestens einem Minimalmaß an Zitierungen wurden eingereicht, sodass von 4,3 Mio. Kanten gerade **15,8 % (680.392) je analysiert wurden**; 35.389 davon tragen `disagreement = true` — **5,2 % der *analysierten* Kanten** (11,2 % bei Kaplan), die ehrliche Basisrate. Die ungelabelten ~84 % defaulten auf keine Stance, ohne je untersucht worden zu sein. Weil der Batch zu gut zitierten Papern gewichtet war, steigt die Label-Rate mit der Zitationszahl des zitierten Papers (5,6 % unter 10 Zitaten → 30,9 % über 1000) und mit der Auseinandersetzung (`contextcount` 1 → 10+: 1,5 % → 42,1 %) — die Abdeckung ist nicht zufällig, sondern *prominenzverzerrt*. Die operative Konsequenz, die durchgehend wiederkehrt: ein *fehlendes* Label heißt meist „nie analysiert", nicht „keine Kritik" (vgl. Besiroglu→Hoffmann, §4.5), und die Methode sieht nur die analysierte Scheibe. Wir behandeln Abdeckung als **Konfidenz-Abschlag** und führen die Prominenz-Verzerrung als Limitation (§9).

### 5.4 Das Typ-Gate: konzeptionelle Korrektur, nicht Benchmark-Überlegenheit

Zitationszahl — sogar Velocity — vermischt *konzeptionelle* Neuheit (eine bestreitbare Behauptung) mit *Artefakt*-Neuheit (ein Survey, Benchmark, Toolkit oder Modell-Release, per Adoption zitiert). Und das Disagreement-Signal filtert Genres **nicht** automatisch: Artefakt-Releases ziehen qualifizierten Disput in Raten *gleich hoch oder höher* als konzeptionelle Landmarks an —

| Paper | Zitationen | Disagreements (`cc ≥ 3`) | pro 1k Zitationen |
|---|---:|---:|---:|
| GPT-3 (konzeptionell+Artefakt) | 34.493 | 369 | 10,7 |
| Kaplan (konzeptionell) | 3.567 | 32 | 9,0 |
| LLaMA (Artefakt) | 9.681 | 109 | 11,3 |
| GPT-4 Technical Report (Artefakt) | 9.377 | 156 | 16,6 |

— weil SOTA-Baseline-Sein zum Widerspruch einlädt. Aber der *Typ* unterscheidet sich: LLaMAs Dispute lauten „Modell X übertrifft LLaMA auf Benchmark Y" (ein Ranking-Rennen); Kaplans lauten „die Potenzgesetz-Werte sind falsch" (eine Korrektur des Mechanismus). Der einzelne `disagreement`-Boolean vermischt sie, also ist ein **Typ-Label** — `{conceptual_correction, scope_limitation, benchmark_superiority}` — tragend: nur die ersten beiden eröffnen eine A→B→C-Dialektik. (Grobes Titel-Regex-Genre-Filtern ist zu leck — `"A Framework for …"` erwischt Methodenpaper — Genre-Screening braucht also einen semantischen Klassifikator, keine Muster; unter 218 Korrektoren tauchen Genre-Paper zu 9,6 % auf, ≈ der 11,0 %-Baseline, d. h. *keine* Selbstfilterung auch auf der Aussteller-Seite.)

### 5.5 Von der retrospektiven Kette zum frühestmöglichen Einstieg: die Velocity-Reformulierung

Die Kette aus §4 ist **retrospektiv**: ihr Salienz-Rang (`citationcount`, `contextcount` als Tiebreaker) liest *Lebenszeit*-Zitationszahlen, eingefroren zum Januar-2025-Snapshot. Aus dem Rückblick von 2025 sind die Paper bereits kanonisch — die Kaskade zeigt die *Form* einer abgeschlossenen Episode, nicht *wann* zu handeln war. Die operative Frage ist die umgekehrte: **was ist der frühestmögliche Moment, einen KI-Wissenschaftler ins Feld zu schicken?**

Ersetzt man Lebenszeit-Zahlen durch Zitations-**Velocity** — Zitationen pro Zeiteinheit — wird das statische Gate zu einem *zeitlichen*:

- **Landmark-Kandidat-Bedingung auf A (notwendig, nicht hinreichend).** A ist ein Landmark-*Kandidat* ab dem ersten Moment, in dem seine Zitations-Velocity die des Feldes übersteigt — ein hohes Perzentil seiner Zeitgenossen. *Schneller als Peers pro Zeiteinheit* zitiert zu werden ist das notwendige Frühzeichen; es garantiert noch keinen Landmark (das Paper kann verpuffen). Das macht die Frage präzise: *ab wann* überschritt Kaplan diese Schwelle? Dieser Zeitstempel **t_A** ist, wann Kaplan zuerst wie ein Landmark *aussieht* — potenziell Jahre bevor seine Lebenszeit-Zahl den Status offensichtlich macht.
- **Dasselbe Maß auf B.** Ab wann überschreitet Hoffmanns Velocity die Qualifizierter-Kritiker-Schwelle, während sein konzeptioneller Disput mit Kaplan registriert wird? Nenne es **t_B**.
- **Frühester Einstieg ≈ t_B.** Nicht As Publikation (t_A ist nur Kandidaten-Signal — die Richtung ist noch spekulativ), und nicht der 2025-Rückblick — sondern der erste Moment, in dem ein velocity-qualifizierter Landmark auf einen velocity-qualifizierten, konzeptionell widersprechenden Kritiker trifft. Das ist, wann die Richtung *in Echtzeit de-riskt* ist (§3.1): das Orakel existiert nun, und verifizierbare Arbeit — Audit, Optimierung — wird möglich. Das ist der wahre **Startschuss**; As Publikation ist es nicht.

**Was das ehrlich voraussetzt.** Velocity als *Rate* braucht zeitaufgelöste Zitations-Historien — Zitationen in den ersten *k* Jahren — wohingegen der Januar-2025-Snapshot eine einzige *Lebenszeit*-Zahl pro Paper trägt. Die Velocities in §5.2 (`citationcount / age`) sind daher ein grober Proxy, und t_A, t_B sind aus diesem Dump allein nicht bestimmbar. Die Velocity-Reformulierung wird also als **Live-Form** der Methode angegeben; das Backtesting, *wann* der Startschuss gefallen wäre, braucht longitudinale Zitationsdaten (z. B. Semantic Scholars Jahres-Zähler) und ist Future Work. Was der Snapshot *doch* belegt, ist die retrospektive Kette plus ein suggestiver Fakt: selbst alters-normalisiert dominiert Hoffmanns Velocity alle Kritiker Kaplans (§5.2) — ein Hinweis, dass das prospektive Signal tatsächlich früh gefeuert hätte.

---

## 6. Was in Reichweite eines KI-Wissenschaftlers liegt — und was nicht

Zwei Achsen entscheiden über Erreichbarkeit: **existiert zum Zeitpunkt ein Orakel?** und **braucht der Zug Ressourcen, die dem Agenten fehlen?** Compute-Cluster sind knapp und teuer; vorhandene Datensätze und publizierte Ergebnisse sind billig.

| Paper | Rolle | Orakel zum Zeitpunkt? | Ressourcenbedarf | In Reichweite? |
|---|---|---|---|---|
| Kaplan | A | Nein — postuliert den Rahmen | moderat Compute | **Nein** — braucht Geschmack, kein Prüfer |
| Hoffmann | B-novel | Nein — entscheidet sich Jahre später | **400+ Modelle — ein großer Cluster** | **Nein** — spekulativ *und* compute-gebunden |
| Besiroglu | B-audit | Ja — Hoffmanns eigene Daten | **ein Laptop** (Re-Analyse) | **Ja** — billig, verifizierbar |
| DeepSeek | C | Ja — vorhandene Loss-Kurven | moderat (Suche + Prüfung) | **Ja\*** — verifizierbar; *Vorbehalt §3.2* |

- **Kaplan (A) ist außer Reichweite.** Kein Orakel: der Wert von „Loss ist aus Compute vorhersagbar" war nicht prüfbar, bis das Feld den Apparat zum Prüfen gebaut hatte. Das ist der menschenförmige Akt des *Geschmacks* — eine Wette auf eine unentschiedene Frage.
- **Hoffmann (B-novel) ist doppelt außer Reichweite.** Es ist spekulativ (die Allokations-Behauptung entschied sich erst später — und war selbst fehlerhaft, s. u.), *und* es verlangte das Training von 400+ Modellen im Maßstab — empirisches Compute, über das der Agent nicht verfügt. Neue-Experimente-Korrektur ist die teuerste und riskanteste Rolle.
- **Besiroglu (B-audit) ist die beste Passung.** Es re-analysierte Chinchillas *publizierte* Daten auf Commodity-Hardware und fand einen statistischen Fehler — pure Interpolation über vorhandenen Zahlen, sofort prüfbar. Landmark-Ergebnisse im Maßstab zu auditieren ist genau das, worin ein unermüdlicher, breiter Agent gut ist, und der Input (Datensätze, berichtete Fits) ist billig.
- **DeepSeek (C) ist in Reichweite, mit dem §3.2-Vorbehalt.** Sein Beitrag ist gegen den vorhandenen Maßstab verifizierbar, und seine schöpferische Wahl ist durch Suche × Verifikation erreichbar, *sofern* der Maß-Raum durchsuchbar ist; bei einem nicht-durchsuchbaren architektonischen Sprung rückt es Richtung A.

**Empirische Stütze für „B-novel ist riskant".** Über 218 „Korrektoren" (Paper, die einem Landmark qualifiziert widersprechen) vs. 1.818 gleich stark zitierte Nicht-Korrektoren werden Korrektoren selbst zu **86,2 %** korrigiert vs. 81,0 %, und ziehen **~23 % mehr Disagreement pro Zitation** an. Hoffmann ist ein Musterfall: es ist Ziel von 7 qualifizierten Disputen, und Besiroglus Audit ist einer davon. *Der Korrektor wird korrigiert* — weshalb die spekulative Korrektur die zu meidende Rolle ist und der Audit die zu besetzende.

---

## 7. Ausblick: eine Landschaft, in der KI C und B-audit übernimmt

Angenommen, automatisierte Agenten besetzen zuverlässig die zwei verifizierbaren Rollen. Vier Dynamiken folgen.

1. **Audit wird kontinuierlich und sofortig.** Jedes Landmark wird gegen seine eigenen Daten re-abgeleitet, sobald es erscheint. Fehler wie Chinchillas Fit tauchen in Wochen auf, nicht in den zwei Jahren, die Besiroglu brauchte. Das Feld verbringt weniger Zeit damit, auf falschen Formeln aufzubauen; die *Kosten, öffentlich falsch zu liegen*, steigen scharf.
2. **Optimierungs-Fenster komprimieren.** Der Tertius-Vorteil — einen de-riskten Rahmen vor dem offensichtlichen Spieler zu betreten — erodiert, wenn ein Agent jedes Fenster erntet, sobald B das Gate überschreitet. Erträge eines *einzelnen* C kollabieren Richtung Wettbewerbsfront; der Burggraben wandert von der Idee zu **Geschwindigkeit und Monitoring-Infrastruktur**.
3. **Die Arbeitsteilung schärft sich entlang der verifizierbar/spekulativ-Naht.** Maschinen besitzen Interpolation (Audit + Optimierung); Menschen werden zur Extrapolation gedrängt — Richtungen eröffnen (A) und neue experimentelle Behauptungen wagen (B-novel), die Rollen, die Geschmack und großes Compute brauchen. Der Engpass *invertiert*: verifizierbare Optimierung wird reichlich und billig, sodass der knappe, wertvolle Input **originäre Richtungssetzung** wird.
4. **Ein selbstkorrigierendes Gleichgewicht.** Ist Audit gratis, werden spekulative Behauptungen sofort druckgeprüft — schlampiges B-novel entmutigt, solides A belohnt. Ist Optimierung gratis und überfüllt, driftet der Preis zurück zu dem, der die *nächste* Richtung eröffnet. Die Ökonomie der Wissenschaft bepreist menschliche Originalität nach oben, gerade weil die verifizierbare Arbeit wegautomatisiert wurde.

Das benennenswerte Risiko: ein Agenten-Ökosystem, das brillant auditiert und optimiert, aber keine Richtungen eröffnen kann, polierte im Grenzfall eine immer feinere Menge *vorhandener* Rahmen, während der Nachschub neuer Rahmen vollständig von Menschen abhängt. Überfluss an C ist kein Ersatz für Knappheit an A.

---

## 8. Coda: hat *dieses* Paper Landmark-Qualität?

Der Rahmen wendet sich gegen sich selbst. Dieses Paper ist ein **A-Typ-Akt**: es postuliert einen Rahmen (die verifizierbar/spekulativ-Achse; die Vier-Rollen-Lesart wissenschaftlichen Fortschritts), für den **heute kein Orakel existiert**. Seine zentralen Behauptungen sind nicht gegen den gegenwärtigen Bestand prüfbar — sie sind eine Wette auf unentschiedenes Terrain. Nach seiner eigenen These macht ihn das zu *spekulativer Neuheit*, dem einen, das ein automatisierter Wissenschaftler nicht hätte hervorbringen und jetzt nicht zertifizieren können.

Also: ist es ein Landmark? Nach genau der Struktur, die es vorschlägt, **kann das Paper nicht antworten.** Es wird nur eines, wenn (a) es Rezeption erfährt und (b) mindestens ein Mensch die Rolle **B-novel** übernimmt — es mit dem neuen Argument oder Beleg bestätigt-und-korrigiert, den das Paper selbst nicht hat (wonach ein B-audit jene Korrektur nachprüfen und ein C die Methode operationalisieren könnte). Und — das ist der ehrliche, unvermeidliche Punkt — **ob das geschieht, lässt sich nicht vorhersagen**, weil es für ein A zum Zeitpunkt der Tat keinen Prüfer gibt. Das Paper erzeugt keine Gewissheit über sich selbst; nur das Feld, später, kann das.

Und der Test ist nicht einmal sauber — wo die Ehrlichkeit enden muss. **Rezeption ist durch Marke konfundiert.** Kaplan trug OpenAI, Chinchilla trug Google DeepMind, DeepSeek trug DeepSeek: jedes kam mit institutioneller Anerkennung und der Vermutung elitärer, hochselektierter Expertise, die Zitation *vorbahnt*, unabhängig vom Inhalt. Die Signale, denen diese Methode vertraut — Zitationszahl, Velocity — messen daher Qualität *verwoben mit* Prestige, und genau die Landmarks, gegen die validiert wird, waren teils durch Marke vorselektiert. Dieses Paper trägt keine solche Marke. Bleibt es also unzitiert, ist die Ursache echt mehrdeutig: geringe Qualität, oder bloß das Fehlen der Voraussetzung, die jedes Paper der Kette genoss. Und die Mehrdeutigkeit ist **asymmetrisch — die Gründe, warum ein Paper *nicht* rezipiert wird, sind weit zahlreicher als die, warum es rezipiert wird** (Obskurität, falscher Ort, kein Netzwerk, schlechtes Timing, keine Marke — und, ja, geringe Qualität), während starke Rezeption sich auf wenige konzentriert (echter Wert, verstärkt durch Prestige). Nicht-Rezeption ist somit schwacher Beleg für irgendetwas; starke Rezeption ist das informativere Ereignis. Der reflexive Test, den der Rahmen vorschlägt, ist damit gerade gegen die Art unmarkierten A-Akts verzerrt, der dieses Paper ist.

Was das ganze Argument reflexiv ist: hätte eine KI dies schreiben können, wäre es kein Landmark. Dass es einen spekulativen Sprung verlangte, ist genau das, was es außer Reichweite des Agenten setzt — und in die des Lesers, es zu erhärten oder zu widerlegen.

---

## 9. Limitationen

1. **Selektive, prominenzverzerrte Abdeckung (§4.3, §5.3).** Nur 15,8 % der Kanten wurden je analysiert, ein fehlendes Label heißt also meist „nie analysiert", nicht „keine Kritik" (Besiroglu→Hoffmann, cc = 10, ist der Warnfall). Der Batch war aus Kostengründen auf Paper mit einem Minimalmaß an Zitierungen beschränkt (§5.3), mit zwei Effekten: (i) die Reduktion des Trichters ist *Coverage × Seltenheit*, und die ehrliche Disagreement-Rate ist 5,2 % der *analysierten* Kanten, nicht aller Kanten; (ii) die Analyse ist zu prominenten zitierten Papern verzerrt (Label-Rate 5,6 % → 30,9 % mit der Zitationszahl), sodass die Methode bevorzugt *prominente* Dispute zutage fördert und substanzielle auf weniger zitierten Arbeiten verpassen kann. Abdeckung ist ein Konfidenz-Abschlag, keine Garantie.
2. **Live-C-Detektion ist eine Wette.** Die Methode behauptet die *Abwesenheit* eines Auflösers; nur die Zeit bestätigt es. Der Backtest validiert das Konzept, nicht jeden prospektiven Aufruf.
3. **Lebenszeit- vs. Früh-Fenster-Zitationen (§5.5).** Die extrahierte Kette nutzt Lebenszeit-Zitationszahlen zum Jan-2025-Snapshot, ist also retrospektiv; die prospektive, velocity-basierte Form, die den Einstieg timen würde (t_A, t_B), braucht Erste-`k`-Jahre-Zitationshistorien, die dem Snapshot fehlen. Das Backtesting, *wann* der Startschuss fällt, ist Future Work.
4. **Ein einzelner Disagreement-Boolean (§5.4).** Er trennt weder bestätigenden-Korrektor von Total-Verwerfer noch konzeptionelle-Korrektur von Benchmark-Überlegenheit. `scripts/classify_disagreement_contexts.py` prototypisiert das Per-Kontext-Heilmittel; eine Summary-Ebene-Typ-Dimension erweitert es.
5. **Genre-Confounder werden nicht auto-gefiltert.** Zitations-/Velocity-Signale lassen Surveys, Benchmarks, Toolkits und Modell-Releases auf beiden Seiten A und B zu; die Methode hängt an einem zusätzlichen semantischen Genre-Vorfilter und dem Typ-Gate, beide hier nicht im Maßstab getestet.
6. **Durchsuchbarkeits-Annahme (§3.2).** Die „C ist in Reichweite"-Behauptung hält nur, wo der Optimierungsraum durchsuchbar genug ist, dass ein Orakel den Treffer findet.
7. **Rezeption ist durch institutionelle Marke konfundiert (§8).** Zitationszahl und Velocity — die Landmark-Signale der Methode — verweben intrinsische Qualität mit dem Prestige der publizierenden Institution (OpenAI, DeepMind, DeepSeek in unserer Kette), das Zitation vorbahnt. Die Methode kann beides nicht trennen, wird also systematisch markierte Arbeit über-ranken und gleich gute unmarkierte unter-detektieren. Nicht-Rezeption ist ein schwaches, vieldeutiges Signal und darf nicht als geringe Qualität gelesen werden.

---

## 10. Daten- & Code-Verfügbarkeit (Reproduzierbarkeit)

```
tertius-gaudens/
├── PAPER.md                     # englische Fassung
├── PAPER.de.md                  # dieses Paper (deutsch)
├── README.md                    # Setup, Herkunft, genaue Aufrufe
├── data/
│   ├── top100.json              # 100 gerankte A→B-Triaden (Gate-Ausgabe)
│   └── kaplan_critics.json      # alle 28 qualifizierten Kritiker Kaplans + Summaries
└── scripts/                     # read-only gegen den Quell-Graphen
    ├── poc_research_ideas.py    # Gate + Selektor (top100 / validate / calibrate)
    ├── diag_contextcount.py     # §4.3 / §5.3 Seltenheit & contextcount-Verteilungen
    ├── classify_disagreement_contexts.py  # §5.4 Per-Kontext CRITICAL/SUPPORTIVE/NEUTRAL
    └── show_disagreeing.py      # Disagreeing-Menge eines Papers inspizieren
```

Jede quantitative Aussage ist reproduzierbar: §4.3/§5.3 aus `diag_contextcount.py`; §5.1-Kalibrierung und §5.2-Triaden aus `poc_research_ideas.py`; die Velocity-Tabellen aus `data/kaplan_critics.json`; die §4.5-Kettenkanten und §6-Korrektor-Statistiken aus direkten read-only-Abfragen (dokumentiert in `README.md`). Der Graph stammt aus öffentlichen Quellen (arXiv-Metadaten; Semantic-Scholar-Zitationsgraph mit In-Text-Kontexten); der Discourse-Layer wurde von den Modellen in §4.7 erzeugt.

---

### Referenzen

[1] J. Kaplan, S. McCandlish, T. Henighan, et al., "Scaling Laws for Neural Language Models," arXiv:2001.08361 [cs.LG], 2020.

[2] T. Henighan, J. Kaplan, M. Katz, et al., "Scaling Laws for Autoregressive Generative Modeling," arXiv:2010.14701 [cs.LG], 2020.

[3] J. Hoffmann, S. Borgeaud, A. Mensch, et al., "Training Compute-Optimal Large Language Models," arXiv:2203.15556 [cs.CL], 2022.

[4] T. Besiroglu, E. Erdil, M. Barnett, and J. You, "Chinchilla Scaling: A Replication Attempt," arXiv:2404.10102 [cs.LG], 2024.

[5] DeepSeek-AI, "DeepSeek LLM: Scaling Open-Source Language Models with Longtermism," arXiv:2401.02954 [cs.CL], 2024.

[6] W. Wang, F. Wei, L. Dong, et al., "MiniLM: Deep Self-Attention Distillation for Task-Agnostic Compression of Pre-Trained Transformers," arXiv:2002.10957 [cs.CL], 2020.

[7] R. Kinney, C. Anastasiades, R. Authur, et al., "The Semantic Scholar Open Data Platform," arXiv:2301.10140 [cs.DL], 2023.

[8] G. Simmel, *Soziologie: Untersuchungen über die Formen der Vergesellschaftung.* Duncker & Humblot, 1908.

[9] R. S. Burt, *Structural Holes: The Social Structure of Competition.* Harvard University Press, 1992.

[10] "Neural scaling law," Wikipedia. https://en.wikipedia.org/wiki/Neural_scaling_law (Abruf 2026).

[11] C. Lu et al., "Towards end-to-end automation of AI research" (The AI Scientist), *Nature*, Bd. 651, Nr. 8107, S. 914–919, 2026. doi:10.1038/s41586-026-10265-5.

[12] A. Karpathy, Interview, *Lex Fridman Podcast* #333, "Tesla AI, Self-Driving, Optimus, Aliens, and AGI," 2022 (arXiv-Segment ≈ 2:36:37).

---

[^arxiv]: **Warum KI-auf-arXiv eine besonders passende Arena ist.** Karpathy [12] fasst arXiv weniger als Website denn als Publikations-*Modell*: man lädt hoch, und binnen Minuten liest, tweetet und zitiert die Community — den monatelangen Journal-Loop umgehend, während ein arXiv-Paper dennoch ein halb-offizielles Gewicht trägt, das ein Blogpost nicht hat. Zwei Merkmale dieses Modells machen KI zu einer ungewöhnlich guten Passung für diese Methode. **Verifizierbarkeit** — ML-Ergebnisse sind billig reproduzierbar, sodass eine heute hochgeladene Behauptung morgen von anderen ausprobiert wird, die zu ihrem Schiedsrichter werden; Community-Review ist schnell und empirisch, und das Feld bewegt sich entsprechend. Das ist genau die *Orakel*-Voraussetzung (§3.2), die die verifizierbaren Rollen — B-audit und C — automatisierbar macht, und sie hält in KI weit besser als in Feldern, wo Reproduktion langsam oder teuer ist. **Kumulativität** — Karpathys Bild wissenschaftlicher Paper als kleine, schnelle „Blockchains", jede auf ihren Vorgängern aufbauend und ihnen widersprechend — ist genau der dichte, aktuelle Disput-Record, den die Methode liest. (Sein Seitenhieb, dass Prestige-Orte das Feld bremsen — Konferenz-Arbeit ist „drei Generationen" alt, und *Nature* liefert Details ein Jahr später — steht pointiert neben unserer eigenen *Nature*-Referenz [11] und dem Marken-Vorbehalt aus §8.)
