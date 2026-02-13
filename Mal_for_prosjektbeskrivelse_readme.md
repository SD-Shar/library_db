# Prosjektbeskrivelse – IT-utviklingsprosjekt (2IMI)

##  Prosjekttittel
**Bibliotek database**

---

## Individuelt prosjekt

---

## 1. Prosjektidé og problemstilling

### Beskrivelse

- Dette prosjektet er en simulert database av et bibliotek.
- Det er mulig å bestille og låne bøker for kunder, og å se bestillinger via admin.
- Dette viser kompetansen min i databaser og tabeller.

---

## 2. Funksjonelle krav

Systemet skal minst ha følgende funksjoner:

1. Logg in for kunde & bibliotekar
2. Hjemme side for kunde
3. Hjemme side for bibliotekar
4. Se bøker både fo rkunder og for bibliotekar
5. Låne/bestille bøker (kunde) 
6. Se logg av tidligere lånte bøker (kunde)
7. Se logg av alle bestillinger (bibliotekar) 
8. Legge til flere bøker (bibliotekar)


---

## 3. Teknologivalg

### Programmeringsspråk
- Python / HTML / CSS

### Rammeverk / Plattform / Spillmotor
Flask / 

### Database
- MariaDB

### Verktøy
- GitHub
- GitHub Projects (Kanban)
---

## 4. Datamodell

### Oversikt over tabeller

**Tabell 1:**
- Navn: brukere
- Beskrivelse:
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


**Tabell 2:**
- Navn: boker
- Beskrivelse:
+---------------+-------------+------+-----+---------+----------------+
| Field         | Type        | Null | Key | Default | Extra          |
+---------------+-------------+------+-----+---------+----------------+
| id            | int(11)     | NO   | PRI | NULL    | auto_increment |
| bok_navn      | varchar(50) | NO   |     | NULL    |                |
| bok_forfatter | varchar(50) | NO   |     | NULL    |                |
+---------------+-------------+------+-----+---------+----------------+



**Tabell 3:**
- Navn: bestilling
- Beskrivelse:
+-------------------+-----------+------+-----+---------------------+-------+
| Field             | Type      | Null | Key | Default             | Extra |
+-------------------+-----------+------+-----+---------------------+-------+
| bruker_id         | int(11)   | NO   | MUL | NULL                |       |
| bok_id            | int(11)   | NO   | MUL | NULL                |       |
| tid_av_bestilling | timestamp | YES  |     | current_timestamp() |       |
+-------------------+-----------+------+-----+---------------------+-------+

### Eksempel på tabellstruktur
```sql
CREATE TABLE bestilling (
    bruker_id INT NOT NULL,
    bok_id INT NOT NULL,
    FOREIGN KEY (bruker_id) REFERENCES brukere(id),
    FOREIGN KEY (bok_id) REFERENCES boker(id),
    tid_av_bestilling TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
