
# --Opprett kunder med id som primærnøkkel
CREATE TABLE kunder (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fornavn VARCHAR(50) NOT NULL,
    etternavn VARCHAR(50) NOT NULL
    epost VARCHAR(100) NOT NULL,
    telefonnummer VARCHAR (15)
);

# --Opprett bøker med id nummer som primærnøkkel
CREATE TABLE boker (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bok_navn VARCHAR(50) NOT NULL,
    bok_id INT NOT NULL,
    FOREIGN KEY (bok_id) REFERENCES kunder(id)
);


# --Lage låne/bestillinger med id som primærnøkkel
CREATE TABLE bestilling (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bok_id INT,
    FOREIGN KEY (bok_id) REFERENCES boker(id),
    tid_av_bestilling DATE
);