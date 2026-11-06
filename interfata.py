import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import random
import webbrowser
from urllib.parse import quote_plus

from database import initializare_baza_date, CALE_BAZA_DATE


CATALOG_AUTO = {
    "Volkswagen": {
        "Golf 5": [2004, 2005, 2006, 2007, 2008],
        "Golf 6": [2009, 2010, 2011, 2012, 2013],
        "Passat B6": [2005, 2006, 2007, 2008, 2009, 2010],
        "Passat B7": [2011, 2012, 2013, 2014],
        "Tiguan": [2008, 2009, 2010, 2011, 2012, 2013, 2014]
    },
    "Audi": {
        "A3 8P": [2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
        "A4 B7": [2005, 2006, 2007, 2008],
        "A4 B8": [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015],
        "A6 C6": [2005, 2006, 2007, 2008, 2009, 2010, 2011],
        "Q5": [2009, 2010, 2011, 2012, 2013, 2014]
    },
    "BMW": {
        "Seria 1 E87": [2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011],
        "Seria 3 E90": [2005, 2006, 2007, 2008, 2009, 2010, 2011],
        "Seria 5 E60": [2004, 2005, 2006, 2007, 2008, 2009, 2010],
        "X3 E83": [2004, 2005, 2006, 2007, 2008, 2009, 2010],
        "X5 E70": [2007, 2008, 2009, 2010, 2011, 2012, 2013]
    },
    "Mercedes-Benz": {
        "A-Class W169": [2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
        "C-Class W204": [2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014],
        "E-Class W211": [2003, 2004, 2005, 2006, 2007, 2008, 2009],
        "E-Class W212": [2009, 2010, 2011, 2012, 2013, 2014, 2015],
        "ML W164": [2006, 2007, 2008, 2009, 2010, 2011]
    },
    "Renault": {
        "Clio 3": [2006, 2007, 2008, 2009, 2010, 2011, 2012],
        "Clio 4": [2013, 2014, 2015, 2016, 2017, 2018],
        "Megane 2": [2003, 2004, 2005, 2006, 2007, 2008],
        "Megane 3": [2009, 2010, 2011, 2012, 2013, 2014, 2015],
        "Laguna 3": [2008, 2009, 2010, 2011, 2012, 2013]
    },
    "Ford": {
        "Fiesta MK6": [2008, 2009, 2010, 2011, 2012],
        "Fiesta MK7": [2013, 2014, 2015, 2016, 2017],
        "Focus MK2": [2005, 2006, 2007, 2008, 2009, 2010],
        "Focus MK3": [2011, 2012, 2013, 2014, 2015, 2016, 2017],
        "Mondeo MK4": [2008, 2009, 2010, 2011, 2012, 2013, 2014]
    },
    "Opel": {
        "Astra H": [2004, 2005, 2006, 2007, 2008, 2009],
        "Astra J": [2010, 2011, 2012, 2013, 2014, 2015],
        "Insignia A": [2009, 2010, 2011, 2012, 2013, 2014],
        "Corsa D": [2007, 2008, 2009, 2010, 2011, 2012, 2013],
        "Zafira B": [2006, 2007, 2008, 2009, 2010, 2011]
    },
    "Toyota": {
        "Yaris": [2006, 2007, 2008, 2009, 2010, 2011],
        "Corolla": [2004, 2005, 2006, 2007, 2008, 2009],
        "Auris": [2007, 2008, 2009, 2010, 2011, 2012],
        "Avensis": [2009, 2010, 2011, 2012, 2013, 2014],
        "RAV4": [2006, 2007, 2008, 2009, 2010, 2011, 2012]
    },
    "Skoda": {
        "Fabia 2": [2007, 2008, 2009, 2010, 2011, 2012, 2013],
        "Octavia 2": [2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
        "Octavia 3": [2013, 2014, 2015, 2016, 2017],
        "Superb 2": [2009, 2010, 2011, 2012, 2013, 2014],
        "Yeti": [2010, 2011, 2012, 2013, 2014, 2015]
    },
    "Fiat": {
        "Grande Punto": [2006, 2007, 2008, 2009, 2010, 2011],
        "Punto Evo": [2010, 2011, 2012],
        "Bravo": [2007, 2008, 2009, 2010, 2011, 2012],
        "500": [2008, 2009, 2010, 2011, 2012, 2013, 2014],
        "Doblo": [2010, 2011, 2012, 2013, 2014]
    }
}


MOTORIZARI = {
    "Diesel": ["1.5 dCi", "1.6 TDI", "1.6 TDCi", "1.7 CDTI", "1.9 TDI", "2.0 TDI", "2.0 Diesel", "2.2 CDI", "3.0 Diesel"],
    "Benzină": ["1.2 MPI", "1.4 TSI", "1.6 MPI", "1.6 VVT-i", "1.8 TFSI", "2.0 TFSI"],
    "Hibrid": ["1.8 Hybrid", "2.0 Hybrid"]
}


MODULE_CONECTARE = [
    "Scanare completă",
    "ECU Motor",
    "ABS/ESP",
    "Airbag/SRS",
    "Cutie viteze",
    "Climatizare",
    "Confort",
    "Direcție asistată",
    "Instrumente bord"
]


CULORI = {
    "bg": "#0B0F19",
    "panel": "#111827",
    "panel2": "#172033",
    "text": "#E5E7EB",
    "muted": "#9CA3AF",
    "accent": "#38BDF8",
    "accent2": "#22C55E",
    "danger": "#EF4444",
    "warning": "#F59E0B",
    "border": "#263244"
}


def conectare_baza_date():
    conexiune = sqlite3.connect(CALE_BAZA_DATE)
    conexiune.execute("PRAGMA foreign_keys = ON")
    return conexiune


def cauta_masina_dupa_vin(vin):
    conexiune = conectare_baza_date()
    cursor = conexiune.cursor()

    cursor.execute("""
        SELECT id_masina, vin, marca, model, an, motorizare, combustibil, transmisie
        FROM masini
        WHERE vin = ?
    """, (vin,))

    masina = cursor.fetchone()
    conexiune.close()
    return masina


def cauta_sau_creeaza_masina(marca, model, an, motorizare, combustibil, transmisie, vin=None):
    conexiune = conectare_baza_date()
    cursor = conexiune.cursor()

    if vin:
        cursor.execute("""
            SELECT id_masina, vin, marca, model, an, motorizare, combustibil, transmisie
            FROM masini
            WHERE vin = ?
        """, (vin,))
        masina = cursor.fetchone()
        if masina:
            conexiune.close()
            return masina

    vin_generat = vin if vin else f"SIM{marca[:3].upper()}{model[:3].upper()}{an}{random.randint(10000, 99999)}"
    vin_generat = vin_generat.replace(" ", "").replace("-", "")

    cursor.execute("""
        INSERT OR IGNORE INTO masini
        (vin, marca, model, an, motorizare, combustibil, transmisie)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (vin_generat, marca, model, an, motorizare, combustibil, transmisie))

    conexiune.commit()

    cursor.execute("""
        SELECT id_masina, vin, marca, model, an, motorizare, combustibil, transmisie
        FROM masini
        WHERE vin = ?
    """, (vin_generat,))

    masina = cursor.fetchone()
    conexiune.close()
    return masina


def obtine_cod_dupa_nume(cod):
    conexiune = conectare_baza_date()
    cursor = conexiune.cursor()

    cursor.execute("""
        SELECT id_cod, cod, descriere, sistem, gravitate, cauze_posibile, simptome, recomandare
        FROM coduri_eroare
        WHERE cod = ?
    """, (cod,))

    rezultat = cursor.fetchone()
    conexiune.close()
    return rezultat


def obtine_modul_dupa_nume(nume_modul):
    conexiune = conectare_baza_date()
    cursor = conexiune.cursor()

    cursor.execute("""
        SELECT id_modul
        FROM module_auto
        WHERE nume_modul = ?
    """, (nume_modul,))

    rezultat = cursor.fetchone()
    conexiune.close()

    if rezultat:
        return rezultat[0]
    return None


def salveaza_scanare(id_masina, rezultate_scanare):
    conexiune = conectare_baza_date()
    cursor = conexiune.cursor()

    data_scanare = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO scanari (id_masina, data_scanare, status_scanare)
        VALUES (?, ?, ?)
    """, (id_masina, data_scanare, "Finalizată"))

    id_scanare = cursor.lastrowid

    for nume_modul, coduri in rezultate_scanare.items():
        id_modul = obtine_modul_dupa_nume(nume_modul)

        if id_modul is not None:
            for cod in coduri:
                cod_info = obtine_cod_dupa_nume(cod)

                if cod_info:
                    id_cod = cod_info[0]

                    cursor.execute("""
                        INSERT OR IGNORE INTO scanari_coduri
                        (id_scanare, id_modul, id_cod, status_cod)
                        VALUES (?, ?, ?, ?)
                    """, (id_scanare, id_modul, id_cod, "Activ"))

    conexiune.commit()
    conexiune.close()
    return id_scanare


def genereaza_rezultate_scanare(modul_selectat, combustibil):
    toate_variantele = {
        "ECU Motor": ["P0300", "P0171", "P0101", "P0113", "P0299", "P0401"],
        "ABS/ESP": ["C0035", "C0040", "C0545"],
        "Airbag/SRS": ["B1000", "B1015"],
        "Cutie viteze": ["U0101", "P0700"],
        "Climatizare": ["B10A9", "B12E1"],
        "Confort": ["U0140", "B1325"],
        "Direcție asistată": ["C0545"],
        "Instrumente bord": ["U0155"]
    }

    if combustibil == "Diesel":
        toate_variantele["ECU Motor"].extend(["P2002", "P0401", "P0299"])

    rezultate = {}

    module_de_scanat = list(toate_variantele.keys())

    if modul_selectat != "Scanare completă":
        module_de_scanat = [modul_selectat]

    for modul in module_de_scanat:
        sansa_eroare = random.randint(1, 100)

        if sansa_eroare <= 70:
            numar_coduri = random.randint(1, min(3, len(toate_variantele[modul])))
            rezultate[modul] = random.sample(toate_variantele[modul], numar_coduri)
        else:
            rezultate[modul] = []

    return rezultate


def deschide_in_browser(cod):
    cautare = quote_plus(f"{cod} OBD2 code definition causes symptoms")
    webbrowser.open(f"https://www.google.com/search?q={cautare}")


def toggle_fullscreen():
    global fullscreen_activ
    fullscreen_activ = not fullscreen_activ
    fereastra.attributes("-fullscreen", fullscreen_activ)


def iesire_fullscreen(event=None):
    global fullscreen_activ
    fullscreen_activ = False
    fereastra.attributes("-fullscreen", False)


def actualizeaza_modele(event=None):
    marca = combo_marca.get()

    if marca in CATALOG_AUTO:
        modele = list(CATALOG_AUTO[marca].keys())
        combo_model["values"] = modele
        combo_model.set(modele[0])
        actualizeaza_ani()


def actualizeaza_ani(event=None):
    marca = combo_marca.get()
    model = combo_model.get()

    if marca in CATALOG_AUTO and model in CATALOG_AUTO[marca]:
        ani = CATALOG_AUTO[marca][model]
        combo_an["values"] = ani
        combo_an.set(ani[-1])


def actualizeaza_motorizari(event=None):
    combustibil = combo_combustibil.get()

    if combustibil in MOTORIZARI:
        combo_motorizare["values"] = MOTORIZARI[combustibil]
        combo_motorizare.set(MOTORIZARI[combustibil][0])


def completeaza_dupa_vin():
    vin = entry_vin.get().upper().strip()

    if not vin:
        messagebox.showwarning("VIN lipsă", "Introdu un VIN sau selectează manual marca, modelul și anul.")
        return

    masina = cauta_masina_dupa_vin(vin)

    if masina is None:
        messagebox.showinfo(
            "VIN negăsit",
            "VIN-ul nu există în baza de date locală.\n"
            "Poți continua prin selectarea manuală a mărcii, modelului și anului."
        )
        return

    _, vin_db, marca, model, an, motorizare, combustibil, transmisie = masina

    combo_marca.set(marca)
    actualizeaza_modele()
    combo_model.set(model)
    actualizeaza_ani()
    combo_an.set(an)
    combo_combustibil.set(combustibil)
    actualizeaza_motorizari()
    combo_motorizare.set(motorizare)
    combo_transmisie.set(transmisie)

    afiseaza_date_masina(masina)


def afiseaza_date_masina(masina):
    _, vin, marca, model, an, motorizare, combustibil, transmisie = masina

    label_vin_val.config(text=vin)
    label_marca_val.config(text=marca)
    label_model_val.config(text=model)
    label_an_val.config(text=str(an))
    label_motor_val.config(text=motorizare)
    label_combustibil_val.config(text=combustibil)
    label_transmisie_val.config(text=transmisie)


def reseteaza_afisare():
    progress_bar["value"] = 0
    label_status.config(text="Status: așteptare comandă diagnoză")
    label_spinner.config(text="○")

    label_vin_val.config(text="-")
    label_marca_val.config(text="-")
    label_model_val.config(text="-")
    label_an_val.config(text="-")
    label_motor_val.config(text="-")
    label_combustibil_val.config(text="-")
    label_transmisie_val.config(text="-")

    text_rezultate.config(state="normal")
    text_rezultate.delete("1.0", tk.END)
    text_rezultate.config(state="disabled")


def porneste_animatie_spinner():
    global animatie_activa, spinner_index

    if not animatie_activa:
        return

    simboluri = ["◐", "◓", "◑", "◒"]
    label_spinner.config(text=simboluri[spinner_index % len(simboluri)])
    spinner_index += 1
    fereastra.after(120, porneste_animatie_spinner)


def porneste_scanare():
    marca = combo_marca.get()
    model = combo_model.get()
    an = combo_an.get()
    combustibil = combo_combustibil.get()
    motorizare = combo_motorizare.get()
    transmisie = combo_transmisie.get()
    modul_selectat = combo_modul.get()
    vin = entry_vin.get().upper().strip()

    if not marca or not model or not an or not combustibil or not motorizare or not transmisie:
        messagebox.showwarning("Date incomplete", "Selectează marca, modelul, anul, combustibilul, motorizarea și transmisia.")
        return

    masina = cauta_sau_creeaza_masina(
        marca=marca,
        model=model,
        an=int(an),
        motorizare=motorizare,
        combustibil=combustibil,
        transmisie=transmisie,
        vin=vin if vin else None
    )

    reseteaza_afisare()
    afiseaza_date_masina(masina)

    buton_scanare.config(state="disabled")
    buton_vin.config(state="disabled")

    global animatie_activa, spinner_index
    animatie_activa = True
    spinner_index = 0
    porneste_animatie_spinner()

    etape_scanare = [
        "Inițializare interfață diagnoză...",
        "Verificare tensiune alimentare vehicul...",
        "Citire identificare vehicul și date ECU...",
        "Stabilire comunicație pe rețeaua CAN...",
        "Interogare module electronice instalate...",
        f"Conectare la: {modul_selectat}...",
        "Citire memorie defecte DTC...",
        "Interpretare coduri conform bazei de date locale...",
        "Salvare raport în istoricul scanărilor...",
        "Diagnoză finalizată."
    ]

    ruleaza_etapa_scanare(0, etape_scanare, masina, modul_selectat, combustibil)


def ruleaza_etapa_scanare(index, etape_scanare, masina, modul_selectat, combustibil):
    if index < len(etape_scanare):
        label_status.config(text=f"Status: {etape_scanare[index]}")
        progress_bar["value"] = int(((index + 1) / len(etape_scanare)) * 100)
        fereastra.after(550, lambda: ruleaza_etapa_scanare(index + 1, etape_scanare, masina, modul_selectat, combustibil))
    else:
        global animatie_activa
        animatie_activa = False
        label_spinner.config(text="●")

        rezultate = genereaza_rezultate_scanare(modul_selectat, combustibil)
        id_scanare = salveaza_scanare(masina[0], rezultate)
        afiseaza_rezultate_scanare(rezultate, id_scanare)

        buton_scanare.config(state="normal")
        buton_vin.config(state="normal")


def afiseaza_rezultate_scanare(rezultate_scanare, id_scanare):
    text_rezultate.config(state="normal")
    text_rezultate.delete("1.0", tk.END)

    text_rezultate.insert(tk.END, "RAPORT DIAGNOZĂ AUTO\n", "titlu")
    text_rezultate.insert(tk.END, "============================================\n")
    text_rezultate.insert(tk.END, f"ID scanare: {id_scanare}\n")
    text_rezultate.insert(tk.END, f"Data scanării: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n")

    total_erori = 0

    for modul, coduri in rezultate_scanare.items():
        text_rezultate.insert(tk.END, f"MODUL: {modul}\n", "modul")
        text_rezultate.insert(tk.END, "--------------------------------------------\n")

        if not coduri:
            text_rezultate.insert(tk.END, "Status: fără coduri de eroare active în memoria modulului.\n\n", "ok")
        else:
            total_erori += len(coduri)

            for cod in coduri:
                cod_info = obtine_cod_dupa_nume(cod)

                if cod_info:
                    _, cod_db, descriere, sistem, gravitate, cauze, simptome, recomandare = cod_info

                    tag_cod = f"cod_{cod_db}_{id_scanare}_{random.randint(1000, 9999)}"

                    text_rezultate.insert(tk.END, "Cod DTC: ", "normal")
                    text_rezultate.insert(tk.END, f"{cod_db}\n", tag_cod)

                    text_rezultate.tag_config(tag_cod, foreground=CULORI["accent"], underline=True)
                    text_rezultate.tag_bind(tag_cod, "<Button-1>", lambda event, c=cod_db: deschide_in_browser(c))
                    text_rezultate.tag_bind(tag_cod, "<Enter>", lambda event: text_rezultate.config(cursor="hand2"))
                    text_rezultate.tag_bind(tag_cod, "<Leave>", lambda event: text_rezultate.config(cursor=""))

                    text_rezultate.insert(tk.END, f"Descriere tehnică: {descriere}\n")
                    text_rezultate.insert(tk.END, f"Sistem afectat: {sistem}\n")

                    if gravitate == "Ridicată":
                        text_rezultate.insert(tk.END, f"Nivel gravitate: {gravitate}\n", "grav_ridicata")
                    elif gravitate == "Medie":
                        text_rezultate.insert(tk.END, f"Nivel gravitate: {gravitate}\n", "grav_medie")
                    else:
                        text_rezultate.insert(tk.END, f"Nivel gravitate: {gravitate}\n", "grav_scazuta")

                    text_rezultate.insert(tk.END, f"Cauze posibile: {cauze}\n")
                    text_rezultate.insert(tk.END, f"Simptome raportate: {simptome}\n")
                    text_rezultate.insert(tk.END, f"Recomandare service: {recomandare}\n\n")

        text_rezultate.insert(tk.END, "\n")

    text_rezultate.insert(tk.END, "============================================\n")
    text_rezultate.insert(tk.END, f"Total coduri detectate: {total_erori}\n")

    if total_erori == 0:
        text_rezultate.insert(tk.END, "Concluzie: vehiculul nu prezintă erori active pe modulele scanate.\n", "ok")
    else:
        text_rezultate.insert(tk.END, "Concluzie: se recomandă verificarea modulelor care au coduri DTC active.\n", "warning")

    text_rezultate.config(state="disabled")


def afiseaza_istoric_scanari():
    conexiune = conectare_baza_date()
    cursor = conexiune.cursor()

    cursor.execute("""
        SELECT 
            s.id_scanare,
            s.data_scanare,
            m.vin,
            m.marca,
            m.model,
            m.an,
            COUNT(sc.id_cod) AS numar_erori
        FROM scanari s
        JOIN masini m ON s.id_masina = m.id_masina
        LEFT JOIN scanari_coduri sc ON s.id_scanare = sc.id_scanare
        GROUP BY s.id_scanare
        ORDER BY s.data_scanare DESC
    """)

    scanari = cursor.fetchall()
    conexiune.close()

    fereastra_istoric = tk.Toplevel(fereastra)
    fereastra_istoric.title("Istoric scanări")
    fereastra_istoric.geometry("1000x520")
    fereastra_istoric.configure(bg=CULORI["bg"])

    tk.Label(
        fereastra_istoric,
        text="ISTORIC SCANĂRI AUTO",
        font=("Arial", 20, "bold"),
        fg=CULORI["text"],
        bg=CULORI["bg"]
    ).pack(pady=15)

    coloane = ("ID Scanare", "Data scanării", "VIN", "Marcă", "Model", "An", "Nr. erori")

    tabel = ttk.Treeview(
        fereastra_istoric,
        columns=coloane,
        show="headings",
        height=15
    )

    for coloana in coloane:
        tabel.heading(coloana, text=coloana)
        tabel.column(coloana, width=130)

    tabel.column("Data scanării", width=170)
    tabel.column("VIN", width=190)
    tabel.column("Nr. erori", width=90)

    for scanare in scanari:
        tabel.insert("", tk.END, values=scanare)

    tabel.pack(pady=10, padx=15, fill="both", expand=True)

    if not scanari:
        messagebox.showinfo("Istoric scanări", "Nu există scanări salvate încă.")


def stilizare_widgeturi():
    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "TCombobox",
        fieldbackground=CULORI["panel2"],
        background=CULORI["panel2"],
        foreground=CULORI["text"],
        arrowcolor=CULORI["accent"],
        bordercolor=CULORI["border"],
        lightcolor=CULORI["border"],
        darkcolor=CULORI["border"]
    )

    style.configure(
        "TProgressbar",
        troughcolor=CULORI["panel2"],
        background=CULORI["accent"],
        bordercolor=CULORI["border"],
        lightcolor=CULORI["accent"],
        darkcolor=CULORI["accent"]
    )

    style.configure(
        "Treeview",
        background=CULORI["panel"],
        foreground=CULORI["text"],
        fieldbackground=CULORI["panel"],
        rowheight=28
    )

    style.configure(
        "Treeview.Heading",
        background=CULORI["panel2"],
        foreground=CULORI["text"],
        font=("Arial", 10, "bold")
    )


initializare_baza_date()

fullscreen_activ = False
animatie_activa = False
spinner_index = 0

fereastra = tk.Tk()
fereastra.title("Sistem Premium Diagnoză Auto")
fereastra.geometry("1250x780")
fereastra.configure(bg=CULORI["bg"])
fereastra.minsize(1100, 700)

stilizare_widgeturi()

fereastra.bind("<F11>", lambda event: toggle_fullscreen())
fereastra.bind("<Escape>", iesire_fullscreen)

header = tk.Frame(fereastra, bg=CULORI["bg"])
header.pack(fill="x", padx=20, pady=15)

tk.Label(
    header,
    text="SISTEM DIAGNOZĂ AUTO",
    font=("Arial", 26, "bold"),
    fg=CULORI["text"],
    bg=CULORI["bg"]
).pack(side="left")

tk.Label(
    header,
    text="OBD-II / DTC / Scanare module",
    font=("Arial", 12),
    fg=CULORI["muted"],
    bg=CULORI["bg"]
).pack(side="left", padx=20)

buton_fullscreen = tk.Button(
    header,
    text="Full screen F11",
    font=("Arial", 11, "bold"),
    bg=CULORI["panel2"],
    fg=CULORI["text"],
    activebackground=CULORI["accent"],
    activeforeground="#000000",
    relief="flat",
    padx=12,
    pady=7,
    command=toggle_fullscreen
)
buton_fullscreen.pack(side="right")

container = tk.Frame(fereastra, bg=CULORI["bg"])
container.pack(fill="both", expand=True, padx=20, pady=5)

panou_stanga = tk.Frame(container, bg=CULORI["panel"], highlightbackground=CULORI["border"], highlightthickness=1)
panou_stanga.pack(side="left", fill="y", padx=(0, 12), pady=5)

panou_dreapta = tk.Frame(container, bg=CULORI["bg"])
panou_dreapta.pack(side="right", fill="both", expand=True, pady=5)

tk.Label(
    panou_stanga,
    text="Configurare vehicul",
    font=("Arial", 16, "bold"),
    fg=CULORI["text"],
    bg=CULORI["panel"]
).pack(anchor="w", padx=15, pady=(15, 5))

tk.Label(
    panou_stanga,
    text="Poți introduce VIN-ul sau poți selecta manual vehiculul.",
    font=("Arial", 10),
    fg=CULORI["muted"],
    bg=CULORI["panel"],
    wraplength=310,
    justify="left"
).pack(anchor="w", padx=15, pady=(0, 15))


def label_form(text):
    tk.Label(
        panou_stanga,
        text=text,
        font=("Arial", 10, "bold"),
        fg=CULORI["text"],
        bg=CULORI["panel"]
    ).pack(anchor="w", padx=15, pady=(8, 2))


label_form("VIN")
entry_vin = tk.Entry(
    panou_stanga,
    font=("Arial", 11),
    bg=CULORI["panel2"],
    fg=CULORI["text"],
    insertbackground=CULORI["text"],
    relief="flat",
    width=32
)
entry_vin.pack(anchor="w", padx=15, pady=3)
entry_vin.insert(0, "WVWZZZ1KZBW123456")

buton_vin = tk.Button(
    panou_stanga,
    text="Identifică după VIN",
    font=("Arial", 10, "bold"),
    bg=CULORI["accent"],
    fg="#000000",
    relief="flat",
    padx=10,
    pady=6,
    command=completeaza_dupa_vin
)
buton_vin.pack(anchor="w", padx=15, pady=(5, 12))

label_form("Marcă")
combo_marca = ttk.Combobox(panou_stanga, values=list(CATALOG_AUTO.keys()), state="readonly", width=30)
combo_marca.pack(anchor="w", padx=15, pady=3)
combo_marca.bind("<<ComboboxSelected>>", actualizeaza_modele)

label_form("Model")
combo_model = ttk.Combobox(panou_stanga, state="readonly", width=30)
combo_model.pack(anchor="w", padx=15, pady=3)
combo_model.bind("<<ComboboxSelected>>", actualizeaza_ani)

label_form("An fabricație")
combo_an = ttk.Combobox(panou_stanga, state="readonly", width=30)
combo_an.pack(anchor="w", padx=15, pady=3)

label_form("Combustibil")
combo_combustibil = ttk.Combobox(panou_stanga, values=list(MOTORIZARI.keys()), state="readonly", width=30)
combo_combustibil.pack(anchor="w", padx=15, pady=3)
combo_combustibil.bind("<<ComboboxSelected>>", actualizeaza_motorizari)

label_form("Motorizare")
combo_motorizare = ttk.Combobox(panou_stanga, state="readonly", width=30)
combo_motorizare.pack(anchor="w", padx=15, pady=3)

label_form("Transmisie")
combo_transmisie = ttk.Combobox(panou_stanga, values=["Manuală", "Automată"], state="readonly", width=30)
combo_transmisie.pack(anchor="w", padx=15, pady=3)

label_form("Modul pentru conectare")
combo_modul = ttk.Combobox(panou_stanga, values=MODULE_CONECTARE, state="readonly", width=30)
combo_modul.pack(anchor="w", padx=15, pady=3)

combo_marca.set("Volkswagen")
actualizeaza_modele()
combo_combustibil.set("Diesel")
actualizeaza_motorizari()
combo_transmisie.set("Manuală")
combo_modul.set("Scanare completă")

frame_butoane = tk.Frame(panou_stanga, bg=CULORI["panel"])
frame_butoane.pack(anchor="w", padx=15, pady=20)

buton_scanare = tk.Button(
    frame_butoane,
    text="PORNEȘTE DIAGNOZA",
    font=("Arial", 11, "bold"),
    bg=CULORI["accent2"],
    fg="#000000",
    relief="flat",
    padx=12,
    pady=9,
    command=porneste_scanare
)
buton_scanare.grid(row=0, column=0, columnspan=2, sticky="ew", pady=4)

buton_reset = tk.Button(
    frame_butoane,
    text="Resetare",
    font=("Arial", 10, "bold"),
    bg=CULORI["panel2"],
    fg=CULORI["text"],
    relief="flat",
    padx=12,
    pady=7,
    command=reseteaza_afisare
)
buton_reset.grid(row=1, column=0, padx=(0, 6), pady=4)

buton_istoric = tk.Button(
    frame_butoane,
    text="Istoric",
    font=("Arial", 10, "bold"),
    bg=CULORI["panel2"],
    fg=CULORI["text"],
    relief="flat",
    padx=12,
    pady=7,
    command=afiseaza_istoric_scanari
)
buton_istoric.grid(row=1, column=1, pady=4)

frame_top = tk.Frame(panou_dreapta, bg=CULORI["bg"])
frame_top.pack(fill="x")

frame_masina = tk.Frame(frame_top, bg=CULORI["panel"], highlightbackground=CULORI["border"], highlightthickness=1)
frame_masina.pack(side="left", fill="both", expand=True, padx=(0, 8))

frame_status = tk.Frame(frame_top, bg=CULORI["panel"], highlightbackground=CULORI["border"], highlightthickness=1)
frame_status.pack(side="right", fill="both", expand=True, padx=(8, 0))

tk.Label(
    frame_masina,
    text="Date vehicul detectat",
    font=("Arial", 15, "bold"),
    fg=CULORI["text"],
    bg=CULORI["panel"]
).grid(row=0, column=0, columnspan=2, sticky="w", padx=15, pady=(15, 10))


def rand_date(parent, rand, titlu):
    tk.Label(parent, text=titlu, font=("Arial", 10, "bold"), fg=CULORI["muted"], bg=CULORI["panel"]).grid(row=rand, column=0, sticky="w", padx=15, pady=3)
    val = tk.Label(parent, text="-", font=("Arial", 10), fg=CULORI["text"], bg=CULORI["panel"])
    val.grid(row=rand, column=1, sticky="w", padx=15, pady=3)
    return val


label_vin_val = rand_date(frame_masina, 1, "VIN:")
label_marca_val = rand_date(frame_masina, 2, "Marcă:")
label_model_val = rand_date(frame_masina, 3, "Model:")
label_an_val = rand_date(frame_masina, 4, "An:")
label_motor_val = rand_date(frame_masina, 5, "Motorizare:")
label_combustibil_val = rand_date(frame_masina, 6, "Combustibil:")
label_transmisie_val = rand_date(frame_masina, 7, "Transmisie:")

tk.Label(
    frame_status,
    text="Proces scanare",
    font=("Arial", 15, "bold"),
    fg=CULORI["text"],
    bg=CULORI["panel"]
).pack(anchor="w", padx=15, pady=(15, 10))

label_spinner = tk.Label(
    frame_status,
    text="○",
    font=("Arial", 42, "bold"),
    fg=CULORI["accent"],
    bg=CULORI["panel"]
)
label_spinner.pack(pady=(0, 5))

label_status = tk.Label(
    frame_status,
    text="Status: așteptare comandă diagnoză",
    font=("Arial", 11),
    fg=CULORI["text"],
    bg=CULORI["panel"],
    wraplength=430,
    justify="left"
)
label_status.pack(anchor="w", padx=15, pady=5)

progress_bar = ttk.Progressbar(frame_status, orient="horizontal", length=430, mode="determinate")
progress_bar.pack(anchor="w", padx=15, pady=15)

tk.Label(
    frame_status,
    text="Sistemul simulează conectarea la modulele electronice și interpretează codurile DTC folosind baza de date SQLite.",
    font=("Arial", 10),
    fg=CULORI["muted"],
    bg=CULORI["panel"],
    wraplength=430,
    justify="left"
).pack(anchor="w", padx=15, pady=(0, 15))

frame_rezultate = tk.Frame(panou_dreapta, bg=CULORI["panel"], highlightbackground=CULORI["border"], highlightthickness=1)
frame_rezultate.pack(fill="both", expand=True, pady=(16, 0))

tk.Label(
    frame_rezultate,
    text="Rezultate diagnoză",
    font=("Arial", 15, "bold"),
    fg=CULORI["text"],
    bg=CULORI["panel"]
).pack(anchor="w", padx=15, pady=(15, 5))

text_rezultate = tk.Text(
    frame_rezultate,
    font=("Consolas", 10),
    bg="#050816",
    fg=CULORI["text"],
    insertbackground=CULORI["text"],
    relief="flat",
    wrap="word",
    height=20
)
text_rezultate.pack(side="left", fill="both", expand=True, padx=(15, 0), pady=(5, 15))

scrollbar = tk.Scrollbar(frame_rezultate, command=text_rezultate.yview)
scrollbar.pack(side="right", fill="y", padx=(0, 15), pady=(5, 15))

text_rezultate.config(yscrollcommand=scrollbar.set)
text_rezultate.tag_config("titlu", foreground=CULORI["accent"], font=("Consolas", 13, "bold"))
text_rezultate.tag_config("modul", foreground=CULORI["accent2"], font=("Consolas", 11, "bold"))
text_rezultate.tag_config("ok", foreground=CULORI["accent2"])
text_rezultate.tag_config("warning", foreground=CULORI["warning"])
text_rezultate.tag_config("grav_ridicata", foreground=CULORI["danger"], font=("Consolas", 10, "bold"))
text_rezultate.tag_config("grav_medie", foreground=CULORI["warning"], font=("Consolas", 10, "bold"))
text_rezultate.tag_config("grav_scazuta", foreground=CULORI["accent2"], font=("Consolas", 10, "bold"))
text_rezultate.tag_config("normal", foreground=CULORI["text"])
text_rezultate.config(state="disabled")

fereastra.mainloop()