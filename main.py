import random

import sqlite3
from datetime import datetime, date

conn = sqlite3.connect("resor.db")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON")

cursor.execute("""
CREATE TABLE IF NOT EXISTS personer (
    id INTEGER PRIMARY KEY,
    fornamn TEXT,
    efternamn TEXT,
    fodelsedatum TEXT,
    personnummer TEXT,
    alder INTEGER
)
""")

print("Tabellen personer är skapad.")

cursor.execute("""
CREATE TABLE IF NOT EXISTS resor (
    id INTEGER PRIMARY KEY,
    flygbolag TEXT,
    bokningsnummer TEXT,
    person_id INTEGER,
    FOREIGN KEY (person_id) REFERENCES personer(id)
)
""")

print("Tabellen resor är skapad.")

for i in range(3):
    print(f"\nPerson {i + 1}")

    fornamn = input("Ange förnamn: ")
    efternamn = input("Ange efternamn: ")
    fodelsedatum = input("Ange födelsedatum (ÅÅÅÅ-MM-DD): ")

    print("\nPersonens uppgifter:")
    print("Namn:", fornamn, efternamn)
    print("Födelsedatum:", fodelsedatum)

    fodd = datetime.strptime(fodelsedatum, "%Y-%m-%d").date()

    idag = date.today()

    alder = idag.year - fodd.year

    if (idag.month, idag.day) < (fodd.month, fodd.day):
        alder -= 1

    print("Ålder:", alder)

    datum = fodd.strftime("%y%m%d")
    slumpnummer = random.randint(0, 9999)

    personnummer = datum + "-" + f"{slumpnummer:04d}"

    print("Personnummer:", personnummer)

    cursor.execute("""
    INSERT INTO personer
    (fornamn, efternamn, fodelsedatum, personnummer, alder)
    VALUES (?, ?, ?, ?, ?)
    """, (fornamn, efternamn, fodelsedatum, personnummer, alder))

    conn.commit()

    print("Personen har sparats i databasen.")

    person_id = cursor.lastrowid

    flygbolag = input("Ange flygbolag: ")
    bokningsnummer = input("Ange bokningsnummer: ")

    cursor.execute("""
    INSERT INTO resor (flygbolag, bokningsnummer, person_id)
    VALUES (?, ?, ?)
    """, (flygbolag, bokningsnummer, person_id))

    conn.commit()

    print("Sommarresan har sparats.")

cursor.execute("""
SELECT personer.fornamn, personer.efternamn,
       personer.personnummer, personer.alder,
       resor.flygbolag, resor.bokningsnummer
FROM personer
JOIN resor ON personer.id = resor.person_id
ORDER BY personer.id
LIMIT 3
""")

resultat = cursor.fetchall()

print("\nDe tre första personerna:")

for person in resultat:
    print("\nNamn:", person[0], person[1])
    print("Personnummer:", person[2])
    print("Ålder:", person[3])
    print("Flygbolag:", person[4])
    print("Bokningsnummer:", person[5])

conn.close()
