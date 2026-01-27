# Prosjektbeskrivelse – IT-utviklingsprosjekt (2IMI)

##  Prosjekttittel
**Bibliotek database**

---

## Individuelt prosjekt

---

## 1. Prosjektidé og problemstilling

### Beskrivelse
Beskriv kort hva dere skal lage.

- Dette prosjektet er en simulert database av et bibliotek.
- Det er mulig å bestille og låne bøker og levere de.
- Dette viser kompetansen min i databaser og tabeller.

### Målgruppe
Hvem er løsningen laget for? (idk)

---

## 2. Funksjonelle krav

Systemet skal minst ha følgende funksjoner:

1. Logg in for bruker 
2. Logg in for admin
3. Låne/bestille bøker  
4. Se logg av tidligere lånte bøker (bruker)
5. Se logg av alle lånte bøker (admin) 

*(Legg til flere hvis nødvendig)*

---

## 3. Teknologivalg

### Programmeringsspråk
- Python / HTML / CSS

### Rammeverk / Plattform / Spillmotor
- Eksempel: Flask / Unity / Godot / .NET

### Database
- MariaDB

### Verktøy
- GitHub
- GitHub Projects (Kanban)
- Eventuelle andre verktøy (no)

---

## 4. Datamodell

### Oversikt over tabeller

**Tabell 1:**
- Navn:
- Beskrivelse:

**Tabell 2:**
- Navn:
- Beskrivelse:

*(Minst 2–4 tabeller)*

### Eksempel på tabellstruktur
```sql
User(
  id INT PRIMARY KEY,
  username VARCHAR(50),
  email VARCHAR(100),
  password VARCHAR(255)
)
