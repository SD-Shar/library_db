# --Opprett kunder med id som primærnøkkel
CREATE TABLE brukere (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    fornavn VARCHAR(50) NOT NULL,
    etternavn VARCHAR(50) NOT NULL,
    epost VARCHAR(100) NOT NULL,
    telefonnummer VARCHAR (15),
    passord_hash VARCHAR(255) NOT NULL,
    rolle VARCHAR(10) NOT NULL DEFAULT 'bruker'
);

# --Opprett bøker med id nummer som primærnøkkel
CREATE TABLE boker (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    bok_navn VARCHAR(50) NOT NULL,
    bok_forfatter VARCHAR(50) NOT NULL
);

# --Lage låne/bestillinger med id som primærnøkkel
CREATE TABLE bestilling (
    bruker_id INT NOT NULL,
    bok_id INT NOT NULL,
    FOREIGN KEY (bruker_id) REFERENCES brukere(id),
    FOREIGN KEY (bok_id) REFERENCES boker(id),
    tid_av_bestilling TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


INSERT INTO brukere (fornavn, etternavn, epost, telefonnummer, passord_hash) VALUES 
( 'First', 'Customer', 'first@customer.com',  '12345678', 'password'),
( 'Hans', 'Holm', 'hans@epost.no', '91234567', 'hanshans'),
( 'Sofie', 'Olsen', 'book@lover.com', '47382910', 'mylittlepony'),
( 'Jonas', 'Berg', 'jonas@epost.com', '99887766', '12345'),
( 'Lisa', 'Karlsen', 'lisa.er@best.no', '45678901', 'lisaerbest'),
( 'Ole', 'Nilsen', 'ole@epost.no', '92345678', 'norge123'),

--(for admin/ibrarian - gonna have "librarian" as default )
( 'New', 'Admin', 'librarian@access.com', '48711508', 'library1');



INSERT INTO boker (bok_navn, bok_forfatter) VALUES
('Book1', 'Author1'),
('Bible',  'Ibel. B.'),
('Mental Health 101',  'Your Mom'),
('Book2',  'Author2'),
('History of knitting',  'Your Mom'),
('top 10 reasons why you are broke',  'Alyssa Gray');


INSERT INTO bestilling (bruker_id, bok_id, tid_av_bestilling) VALUES
( 1, 2, '2026-01-21'),
( 5, 1, '2026-01-29'),
( 3, 6, '2026-02-14'),
( 1, 4, '2026-02-18'),
( 7, 2, '2026-02-19'),
( 4, 5, '2026-02-27'),
( 6, 3, '2026-03-10');



ALTER TABLE boker ADD antall_boker VARCHAR(255);

UPDATE boker SET antall_boker = '100' WHERE id = 2,
UPDATE boker SET antall_boker = '15' WHERE id = 3,
UPDATE boker SET antall_boker = '20' WHERE id = 4,
UPDATE boker SET antall_boker = '12' WHERE id = 5,
UPDATE boker SET antall_boker = '30' WHERE id = 6,
UPDATE boker SET antall_boker = '6' WHERE id = 7,
UPDATE boker SET antall_boker = '1' WHERE id = 8,
UPDATE boker SET antall_boker = '3072' WHERE id = 9,
UPDATE boker SET antall_boker = '10' WHERE id = 10,
UPDATE boker SET antall_boker = '13' WHERE id = 11,
UPDATE boker SET antall_boker = '2' WHERE id = 12,
UPDATE boker SET antall_boker = '8' WHERE id = 13,
UPDATE boker SET antall_boker = '5' WHERE id = 14;
