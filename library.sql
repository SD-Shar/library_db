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


CREATE TABLE folk (
    id INT AUTO_INCREMENT PRIMARY KEY NOT  NULL,
    navn VARCHAR(50) NOT NULL,
    tlf VARCHAR(15) NOT NULL,
    rolle VARCHAR(10) NOT NULL DEFAULT 'lever'
);

INSERT INTO folk (navn, tlf) VALUES ('aaaa', '1234');

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




-- [LEGG TIL LEVERINGSFRIST] (prøveeksamen)

ALTER TABLE bestilling ADD leveringsfrist DATE;

-- INSERT INTO bestilling (bruker_id, bok_id, leveringsfrist) VALUES (%s, %s, %s)", (bruker_id, bok_id, leveringsfrist);

CREATE TABLE ny_faq (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    bruker_id INT NOT  NULL,
    sporsmal TEXT NOT NULL,
    opprettet DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (bruker_id) REFERENCES brukere(id) ON DELETE CASCADE
);


INSERT INTO ny_faq (bruker_id, sporsmal, opprettet) VALUES (%s, %s, %s), (bruker_id, sporsmal, opprettet);

INSERT INTO ny_faq (bruker_id, sporsmal, opprettet) VALUES
( 1, 'Hvordan logger jeg inn?', '2026-01-01'),
( 1, 'Hvordan endrer jeg passord?', '2026-01-01'),
( 1, 'Hvordan sletter jeg kontoen min?', '2026-01-01'),
( 1, 'Hvordan kontakter jeg support?', '2026-01-01'),
( 1, 'Hvordan behandles persondata?', '2026-01-01');

-- for raspberry pi
INSERT INTO ny_faq (bruker_id, sporsmal, opprettet) VALUES
( 1, 'How do I borrow a book?', '2026-01-01'),
( 1, 'How do I return a book?', '2026-01-01'),
( 1, 'How do I delete my account?', '2026-01-01'),
( 1, 'Where can I contact customer service?', '2026-01-01'),
( 1, 'How is my data stored?', '2026-01-01');
( 1, 'What if my question is not here?', '2026-01-01');

ALTER TABLE ny_faq ADD COLUMN svar TEXT VARCHAR(100);


INSERT INTO ny_faq (svar) VALUES
('You can borrow a book by pressing the "Borrow Book" button beside the book.'),
('You can return a book by going to your "borrowed books" page and clicking "Return Book".'),
('You can request to have your account deleted by emailing us at 'library@notascam.com.''),
('You can request to have your account deleted by emailing us at 'library@notascam.com',MAKE SURE to return all books before requesting to delete your account.'),
('You can contact us on 'library@notascam.com'.'),
('Your personal data is stored safely in a database with limited access, passwords are securely hashed and private, and all your personal records and data will be removed upon delete of an account'),
('If your question is not here, please feel free to ask us here below, an administrator will contact you on mail as soon as possible.');


