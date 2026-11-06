import os
import sqlite3


CALE_BAZA_DATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "diagnoza_auto.db")


def conectare_baza_date():
    conexiune = sqlite3.connect(CALE_BAZA_DATE)
    conexiune.execute("PRAGMA foreign_keys = ON")
    return conexiune


def creare_tabele():
    conexiune = conectare_baza_date()
    cursor = conexiune.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS masini (
            id_masina INTEGER PRIMARY KEY AUTOINCREMENT,
            vin TEXT NOT NULL UNIQUE,
            marca TEXT NOT NULL,
            model TEXT NOT NULL,
            an INTEGER,
            motorizare TEXT,
            combustibil TEXT,
            transmisie TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS module_auto (
            id_modul INTEGER PRIMARY KEY AUTOINCREMENT,
            nume_modul TEXT NOT NULL UNIQUE,
            descriere TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS coduri_eroare (
            id_cod INTEGER PRIMARY KEY AUTOINCREMENT,
            cod TEXT NOT NULL UNIQUE,
            descriere TEXT NOT NULL,
            sistem TEXT,
            gravitate TEXT,
            cauze_posibile TEXT,
            simptome TEXT,
            recomandare TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scanari (
            id_scanare INTEGER PRIMARY KEY AUTOINCREMENT,
            id_masina INTEGER NOT NULL,
            data_scanare TEXT NOT NULL,
            status_scanare TEXT,
            FOREIGN KEY (id_masina) REFERENCES masini(id_masina)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scanari_coduri (
            id_scanare INTEGER NOT NULL,
            id_modul INTEGER NOT NULL,
            id_cod INTEGER NOT NULL,
            status_cod TEXT,
            PRIMARY KEY (id_scanare, id_modul, id_cod),
            FOREIGN KEY (id_scanare) REFERENCES scanari(id_scanare),
            FOREIGN KEY (id_modul) REFERENCES module_auto(id_modul),
            FOREIGN KEY (id_cod) REFERENCES coduri_eroare(id_cod)
        )
    """)

    conexiune.commit()
    conexiune.close()


def inserare_date_initiale():
    conexiune = conectare_baza_date()
    cursor = conexiune.cursor()

    masini = [
        ("WVWZZZ1KZBW123456", "Volkswagen", "Golf 6", 2011, "2.0 TDI", "Diesel", "Manuală"),
        ("WBAVC31080A123456", "BMW", "Seria 3 E90", 2008, "2.0 Diesel", "Diesel", "Automată"),
        ("WAUZZZ8K9CA123456", "Audi", "A4 B8", 2012, "2.0 TDI", "Diesel", "Manuală"),
        ("WDD2040081A123456", "Mercedes-Benz", "C-Class W204", 2010, "2.2 CDI", "Diesel", "Automată"),
        ("VF1BZ1A0541234567", "Renault", "Megane 3", 2011, "1.5 dCi", "Diesel", "Manuală"),
        ("WF0EXXGCDEAB12345", "Ford", "Focus MK3", 2013, "1.6 TDCi", "Diesel", "Manuală"),
        ("JTDBR32E530123456", "Toyota", "Corolla", 2006, "1.6 VVT-i", "Benzină", "Manuală"),
        ("ZFA19900001234567", "Fiat", "Grande Punto", 2009, "1.3 Multijet", "Diesel", "Manuală"),
        ("TMBJG7NE6E0123456", "Skoda", "Octavia 3", 2014, "2.0 TDI", "Diesel", "Manuală"),
        ("W0L0AHL3552123456", "Opel", "Astra H", 2005, "1.7 CDTI", "Diesel", "Manuală")
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO masini
        (vin, marca, model, an, motorizare, combustibil, transmisie)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, masini)

    module = [
        ("ECU Motor", "Unitatea electronică de control a motorului"),
        ("ABS/ESP", "Sistem antiblocare roți și control stabilitate"),
        ("Airbag/SRS", "Sistem de siguranță pasivă și airbaguri"),
        ("Cutie viteze", "Modul electronic transmisie automată/manuală robotizată"),
        ("Climatizare", "Sistem climatizare și distribuție aer habitaclu"),
        ("Confort", "Modul confort, închidere centralizată, geamuri, caroserie"),
        ("Direcție asistată", "Sistem servodirecție electrică/electrohidraulică"),
        ("Instrumente bord", "Ceasuri de bord și martori avertizare")
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO module_auto
        (nume_modul, descriere)
        VALUES (?, ?)
    """, module)

    coduri = [
        (
            "P0300",
            "Rateuri de aprindere multiple sau aleatorii detectate",
            "Motor / Aprindere",
            "Ridicată",
            "Bujii uzate, bobine de inducție defecte, injectoare cu debit neuniform, compresie scăzută, amestec aer-combustibil incorect.",
            "Motorul funcționează neregulat, tremură la ralanti, pierde putere la accelerație, consumul crește, martorul Check Engine poate clipi.",
            "Se recomandă verificarea bujiilor, bobinelor de inducție, injectorilor, compresiei cilindrilor și parametrilor de amestec în timp real."
        ),
        (
            "P0171",
            "Amestec prea sărac pe banca 1",
            "Motor / Alimentare",
            "Medie",
            "Aer fals pe admisie, furtun vacuum fisurat, debitmetru MAF contaminat, presiune combustibil scăzută, injector parțial înfundat.",
            "Ralanti instabil, pornire dificilă la rece, lipsă de putere, corecții mari de combustibil, consum anormal.",
            "Verificați etanșeitatea admisiei, valorile MAF/MAP, presiunea combustibilului și corecțiile Short Term/Long Term Fuel Trim."
        ),
        (
            "P0420",
            "Eficiența catalizatorului sub limita admisă, banca 1",
            "Evacuare / Emisii",
            "Medie",
            "Catalizator uzat, sondă lambda post-catalizator defectă, scurgeri pe evacuare, amestec incorect sau rateuri care au afectat catalizatorul.",
            "Martor Check Engine aprins, emisii crescute, uneori consum mărit sau miros neplăcut pe evacuare.",
            "Se recomandă verificarea sondelor lambda, testarea catalizatorului, verificarea eventualelor scurgeri pe evacuare și eliminarea rateurilor înainte de înlocuire."
        ),
        (
            "P0101",
            "Debitmetru aer MAF - semnal în afara domeniului de funcționare",
            "Admisie / Management motor",
            "Medie",
            "Debitmetru murdar sau defect, filtru de aer colmatat, furtun admisie crăpat, depuneri pe clapeta de accelerație.",
            "Accelerație ezitantă, lipsă de putere, ralanti oscilant, consum ridicat, fum negru la diesel.",
            "Verificați valorile debitmetrului în live data, curățați sau înlocuiți MAF-ul și inspectați traseul de admisie."
        ),
        (
            "P0113",
            "Senzor temperatură aer admisie - semnal prea mare",
            "Admisie / Senzori",
            "Scăzută",
            "Senzor IAT defect, circuit întrerupt, mufă oxidată, cablaj deteriorat.",
            "Pornire greoaie, consum ușor crescut, funcționare neregulată la rece.",
            "Verificați alimentarea, masa și semnalul senzorului IAT, apoi inspectați mufa și cablajul."
        ),
        (
            "P0299",
            "Presiune turbo insuficientă",
            "Supraalimentare / Turbo",
            "Ridicată",
            "Furtun intercooler fisurat, actuator turbo blocat, geometrie variabilă gripată, vacuum insuficient, senzor MAP defect.",
            "Lipsă de putere, intrare în limp mode, fum excesiv, accelerație slabă.",
            "Verificați presiunea de supraalimentare cerută vs. reală, furtunurile turbo, actuatorul, vacuumul și senzorul MAP."
        ),
        (
            "P0401",
            "Debit insuficient prin sistemul EGR",
            "Recirculare gaze / EGR",
            "Medie",
            "Supapă EGR blocată, galerie admisie colmatată, conducte EGR înfundate, senzor diferențial presiune defect.",
            "Martor motor aprins, fum, lipsă putere, uneori bătăi sau funcționare neregulată.",
            "Se recomandă verificarea și curățarea EGR-ului, verificarea conductelor și a parametrilor de comandă EGR."
        ),
        (
            "P2002",
            "Eficiență filtru de particule DPF sub prag",
            "Evacuare / DPF",
            "Ridicată",
            "DPF încărcat, regenerări incomplete, senzor presiune diferențială defect, trasee senzor înfundate.",
            "Martor DPF aprins, putere redusă, consum crescut, ventilatoare pornite frecvent.",
            "Verificați încărcarea DPF, presiunea diferențială, temperatura gazelor și istoricul regenerărilor."
        ),
        (
            "C0035",
            "Senzor viteză roată față stânga - semnal incorect",
            "ABS/ESP",
            "Medie",
            "Senzor ABS defect, cablaj întrerupt, inel magnetic deteriorat, conector oxidat.",
            "Martor ABS/ESP aprins, ABS dezactivat, controlul tracțiunii indisponibil.",
            "Verificați senzorul de roată, cablajul până la modulul ABS și semnalul senzorului în mers."
        ),
        (
            "C0040",
            "Senzor viteză roată față dreapta - semnal incorect",
            "ABS/ESP",
            "Medie",
            "Senzor ABS defect, cablaj deteriorat, rulment cu inel magnetic afectat, mufă oxidată.",
            "Martor ABS aprins, funcționare defectuoasă ABS/ESP, posibile intervenții false ale sistemului.",
            "Se recomandă citirea vitezelor roților în live data și verificarea senzorului față dreapta."
        ),
        (
            "B1000",
            "Defecțiune internă modul Airbag/SRS",
            "Airbag/SRS",
            "Ridicată",
            "Modul airbag defect, tensiune alimentare instabilă, eroare internă memorie, comunicație defectuoasă.",
            "Martor airbag aprins, sistemul SRS poate fi dezactivat parțial sau total.",
            "Verificați alimentările modulului SRS, masa, comunicația CAN și efectuați testare cu echipament dedicat."
        ),
        (
            "B1015",
            "Rezistență prea mare circuit airbag șofer",
            "Airbag/SRS",
            "Ridicată",
            "Spirală volan defectă, mufă slăbită, cablaj întrerupt, airbag șofer defect.",
            "Martor airbag aprins, airbagul șoferului poate să nu funcționeze la impact.",
            "Verificați spirala volanului, conectorii SRS și rezistența circuitului conform procedurilor de siguranță."
        ),
        (
            "U0101",
            "Comunicare pierdută cu modulul cutiei de viteze",
            "Rețea CAN / Transmisie",
            "Ridicată",
            "Lipsă alimentare TCM, siguranță arsă, cablaj CAN întrerupt, modul transmisie defect.",
            "Cutia poate intra în avarie, schimbări dure, imposibilitatea selectării treptelor, martor transmisie aprins.",
            "Verificați alimentările și masele modulului TCM, rețeaua CAN și siguranțele asociate transmisiei."
        ),
        (
            "P0700",
            "Sistem transmisie - defecțiune detectată",
            "Cutie viteze",
            "Medie",
            "ECU motor a primit solicitare de aprindere martor de la modulul cutiei, existând erori stocate în TCM.",
            "Martor motor aprins, schimbări întârziate sau dure, mod avarie transmisie.",
            "Scanați separat modulul cutiei de viteze pentru codurile specifice și verificați nivelul/starea uleiului."
        ),
        (
            "B10A9",
            "Motor clapetă climatizare blocat sau necalibrat",
            "Climatizare",
            "Scăzută",
            "Motoras clapetă defect, mecanism blocat, calibrare pierdută, potențiometru intern uzat.",
            "Aerul nu este direcționat corect, diferențe de temperatură stânga/dreapta, zgomote în bord.",
            "Efectuați calibrarea clapetelor, verificați motorasul și mecanismul de distribuție aer."
        ),
        (
            "B12E1",
            "Senzor temperatură habitaclu - semnal neplauzibil",
            "Climatizare",
            "Scăzută",
            "Senzor temperatură interior defect, ventilator senzor blocat, cablaj oxidat.",
            "Climatizarea reglează incorect temperatura, aer prea cald sau prea rece.",
            "Verificați senzorul de temperatură interior și valorile citite în diagnoză."
        ),
        (
            "U0140",
            "Comunicare pierdută cu modulul caroserie BCM",
            "Confort / Rețea CAN",
            "Medie",
            "Modul BCM fără alimentare, cablaj CAN întrerupt, siguranță arsă, modul defect.",
            "Probleme cu închiderea centralizată, lumini, geamuri electrice sau alte funcții de confort.",
            "Verificați alimentările BCM, siguranțele, masele și comunicația pe rețeaua CAN."
        ),
        (
            "B1325",
            "Tensiune alimentare scăzută în modulul de caroserie",
            "Confort / Alimentare",
            "Scăzută",
            "Baterie slabă, alternator cu încărcare insuficientă, contact imperfect pe alimentare sau masă.",
            "Erori multiple sporadice, funcții electrice instabile, pornire greoaie.",
            "Verificați tensiunea bateriei, încărcarea alternatorului și conexiunile principale de masă."
        ),
        (
            "C0545",
            "Senzor unghi volan - semnal necalibrat",
            "Direcție asistată / ESP",
            "Medie",
            "Senzor unghi volan necalibrat, baterie deconectată, defect senzor, probleme comunicație.",
            "Martor ESP sau servodirecție aprins, sistemele de stabilitate pot fi limitate.",
            "Efectuați calibrarea senzorului de unghi volan și verificați valorile live data."
        ),
        (
            "U0155",
            "Comunicare pierdută cu tabloul de instrumente",
            "Instrumente bord / Rețea CAN",
            "Medie",
            "Alimentare bord întreruptă, siguranță arsă, defect intern cluster, problemă CAN.",
            "Ceasuri de bord inactive, martori aprinși, afișaj nefuncțional.",
            "Verificați alimentările, siguranțele, masele și comunicația CAN către tabloul de bord."
        )
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO coduri_eroare
        (cod, descriere, sistem, gravitate, cauze_posibile, simptome, recomandare)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, coduri)

    conexiune.commit()
    conexiune.close()


def initializare_baza_date():
    creare_tabele()
    inserare_date_initiale()