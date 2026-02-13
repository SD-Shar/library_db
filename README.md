# Prosjektbeskrivelse av library_db – IT-utviklingsprosjekt (2IMI)

##  Bibliotek prosjekt
**Bibliotek database:**\
**Rebecca:**\
**2IMI:**\
**lagd uke 5-7 2026:**

---

### Individuelt prosjekt

---

## 1. Prosjektidé og problemstilling

### Beskrivelse
```markdown
- Dette prosjektet er en simulert database av et bibliotek.
- Det er mulig å bestille og låne bøker for kunder, og å se bestillinger,
både personlige bestillinger fra kunder og alle bestillinger for bibliotekaren.

Spørsmål og problem:
"Hvilket problem løser løsningen?"
- Her er spørsmålet hvordan kan jeg bestille bøker på det bibliotek?
Og løsningen har jeg laget med alle sidene og deler av kode som lar en
bruker se og låne bøker.
"Hvem er målgruppen?"
- På denne nettsiden er målgruppen yngre folk som liker å lese,
og de som har tilgang til nett og liker å bruke nettbaserte bestillinger.
```

**Installasjon og kjøring av prosjektet:**

1. **Klon prosjektet:**
```markdown
    git clone https://github.com/SD-Shar/library_db.git
```
2. **Installasjons krav:**
    ```mardown
    ```bash
    pip install flask
    pip install mysql.connector
    .env - (med eget passord)


3. **Kjøring av prosjekt:**
```markdown
   aktiver terminal med 'source venv/Scripts/activate'
   kjør med 'python -m flask run' eller 'flask run'
```
---

## 2. Funksjonalitet i biblioteket

1. Sign up (lage ny bruker, med default rolle 'bruker')
2. Logg in til biblioteket
3. Hjemme side for kunde
4. Hjemme side for bibliotekar
5. Se bøker både for kunder og for bibliotekar
6. Låne/bestille bøker (kunde) 
7. Se logg av tidligere lånte bøker (kunde)
8. Se logg av alle bestillinger og lånte bøker (bibliotekar) 
9. Legge til flere bøker (bibliotekar)
10. (Data lagres i MariaDB)

---

## 3. Teknologivalg

### Programmeringsspråk
 ```markdown
- Python / HTML / CSS\
 ```
### Rammeverk 
 ```markdown
Flask / Python\
 ```
### Database
 ```markdown
- MariaDB / Raspberry PI\
 ```
### Servermiljø
 ```markdown
 *Ubuntu v.25, Mariadb, Raspberry pi*
  ```

### Verktøy
 ```markdown
- GitHub
- GitHub Projects (Kanban)
 ```

---

## 4. Datamodell

### Oversikt over tabeller

**Bruker tabell**

- Navn i databasen: brukere
- Beskrivelse: Denne tabellen er for brukerene (kundene) i biblioteket.
Denne dataen blir lagret etter at en kunde lager en ny bruker i 'Sign up'.
Default rollen til en som registrerer en ny bruker er alltid 'bruker'
med mindre det blir endringer i databasen.
(Bibliotekarer må få rollen sin via en manuelle endringer,
det går ikke an å velge det ved registrering.)
 ```markdown
+---------------+--------------+------+-----+---------+----------------+
| Field         | Type         | Null | Key | Default | Extra          |
+---------------+--------------+------+-----+---------+----------------+
| id            | int(11)      | NO   | PRI | NULL    | auto_increment |
| fornavn       | varchar(50)  | NO   |     | NULL    |                |
| etternavn     | varchar(50)  | NO   |     | NULL    |                |
| epost         | varchar(100) | NO   |     | NULL    |                |
| telefonnummer | varchar(15)  | YES  |     | NULL    |                |
| passord_hash  | varchar(255) | NO   |     | NULL    |                |
| rolle         | varchar(10)  | NO   |     | bruker  |                |
+---------------+--------------+------+-----+---------+----------------+
 ```

**Bok tabell**

- Navn i databasen: boker
- Tabellen for bøker inneholder en ID til hver bok,
bokens tittel (navn) og bokens forfatter.
Navnet til boken og forfatteren blir lagret i "Add books"
siden til bibliotekaren og blir automatisk oppdatert.
Det går ikke an å endre informasjonen til bøker gjennom nettsiden.
 ```markdown
+---------------+-------------+------+-----+---------+----------------+
| Field         | Type        | Null | Key | Default | Extra          |
+---------------+-------------+------+-----+---------+----------------+
| id            | int(11)     | NO   | PRI | NULL    | auto_increment |
| bok_navn      | varchar(50) | NO   |     | NULL    |                |
| bok_forfatter | varchar(50) | NO   |     | NULL    |                |
+---------------+-------------+------+-----+---------+----------------+
 ```

**Bestillings tabell**

- Navn i databasen: bestilling
- Bestillingstabellen er det som binder sammen kundene og bøkene de bestiller.
Den har 'bruker_id' og 'bok_id' som python koden lenker til brukerene sin id og bok id.
'tid_av_bestilling' oppdateres på live tid når en kunde låner en bok,
dette er mulig med default kommandoen 'current_timestamp(). 
 ```markdown
+-------------------+-----------+------+-----+---------------------+-------+
| Field             | Type      | Null | Key | Default             | Extra |
+-------------------+-----------+------+-----+---------------------+-------+
| bruker_id         | int(11)   | NO   | MUL | NULL                |       |
| bok_id            | int(11)   | NO   | MUL | NULL                |       |
| tid_av_bestilling | timestamp | YES  |     | current_timestamp() |       |
+-------------------+-----------+------+-----+---------------------+-------+
 ```


### Eksempel på tabellstruktur
 ```markdown
```sql
CREATE TABLE bestilling (
    bruker_id INT NOT NULL,
    bok_id INT NOT NULL,
    FOREIGN KEY (bruker_id) REFERENCES brukere(id),
    FOREIGN KEY (bok_id) REFERENCES boker(id),
    tid_av_bestilling TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

```
```
---

## 5. Refleksjon

**Feil eller mangler i biblioteket**
 ```markdown
Med tidsrammen var det ikke alt jeg fikk tid til å gjøre,
så måten biblioteket funker nå er veldig enkelt.
Det første store problemet er at det ikke er en grense på hvor mange
kan låne en bok, og flere brukere kan låne den samme boken uten en ventetid.
Det er også ingen leveringsfunksjon for å levere tilbake lånte bøker på nettsiden.
Dette hadde jeg tenkt på når jeg startet biblioteks prosjektet
men visste at det ville blitt et uferdig prosjekt om jeg hadde lagt til
mer arbeid enn jeg visste jeg kunne få til.

Visuelt så er det et sentreringsproblem jeg ikke har funnet ut av
i oversikten av bøker og bestillinger.
Dette er et css problem og kan fikses kjapt,
men siden finpussing av hvordan nettsiden ser ut ikke
er det viktigste prioriterte jeg å bli ferdig med dokumentasjonen i tide.
 ```

**Problemer jeg møtte**
 ```markdown
Å lage selve databasen gikk helt greit og jeg skrev av
tidligere koder som lignet for å lage biblioteket.
Å legge til farger og rammer på slutten synes jeg også var
gøy og uten problemer (med unntak av et sentreringsproblem for tabeller.)
Det som gav meg litt problemer var små skrivefeil, linking med sider,
og informasjonen som skulle vises på nettsiden. 
Det meste av hvor jeg har fått koden og informasjonen min
er basert på tidligere prosjekter og egen kunnskap fra før,
men til en del av kode der bestillingene skulle vises og ha med id-er
fra 2 forskjellige tabeller, måtte jeg spørre chatGPT med innslag fra lærer. 
Jeg foretrekker å ikke bruke KI, men informasjonen jeg fikk var en sql
kommando som jeg ikke visste om fra før og jeg kan bruke denne informasjonen
senere i livet eller til ting jeg jobber med i fremtidige prosjekter.
 ```

**Til fremtidige prosjekter**
 ```markdown
Til fremtiden, om jeg skal jobbe videre med dette prosjektet,
ville jeg lagt til en leverings funksjon til bibilioteket.
Da ville jeg trengt en tabell til, som skal kunne lenke til bestillingene,
bruker id, bok id, bestillings tid og oppdatere når en bok ble gitt tilbake.
Med en lånefrist må jeg også legge til en variabel for når boken skal
bli levert basert på når den var lånt. 

Med tanke på fremtidige prosjekter kan jeg lære av slurvefeil
eller lignende ting jeg hadde problemer med
```


---

## 6. Kildeliste
 ```markdown
 - Tidligere oppgaver og utviklingsprosjekter
 - w3schools
 - ChatGPT (for rydding opp i kode, skrivefeil og en del av kode for bestilling)
  ```

### Laget av 
Rebecca 2IMI