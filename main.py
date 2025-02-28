import csv

# Zbiór wyjątków – imiona, które mimo kończącej się na "a" nie są żeńskie
wyjatki_mesky = {"Kuba", "Barnaba", "Kosma"}

def rozpoznaj_plec(imie):
    """
    Rozpoznaje płeć na podstawie imienia.
    Jeśli imię jest w wyjątkach, zwraca "Mężczyzna".
    Jeśli imię kończy się na "a", uznaje je za żeńskie.
    W innym przypadku zwraca "Mężczyzna".
    """
    if imie in wyjatki_mesky:
        return "Mężczyzna"
    if imie and imie[-1].lower() == "a":
        return "Kobieta"
    return "Mężczyzna"

def transform_name_heuristic(name):
    """
    Przekształca imię z mianownika do formy wołacza przy użyciu prostych heurystyk.
    Uwaga: metoda nie obejmuje wszystkich wyjątków języka polskiego.
    """
    if name.endswith("ek"):
        return name[:-2] + "ku"
    elif name.endswith("usz"):
        return name + "ie"
    elif name.endswith("n"):
        return name[:-1] + "nie"
    elif name.endswith("r"):
        return name + "ze"
    elif name.endswith("m"):
        return name + "ie"
    elif name.endswith("a"):
        return name[:-1] + "o"
    elif name.endswith("k"):
        return name[:-1] + "ku"
    elif name.endswith("t"):
        return name[:-1] + "cie"
    elif name.endswith("sz"):
        return name + "u"
    elif name.endswith("ł"):
        return name[:-1] + "le"
    elif name.endswith("j"):
        return name[:-1] + "ju"
    elif name.endswith("d"):
        return name + "zie"
    
    vowels = "aeiouyąęóAEIOUYĄĘÓ"
    if name and name[-1] not in vowels:
        return name + "ie"
    
    return name

# Ścieżki do plików CSV
input_file = 'input.csv'   # Plik oryginalny z kolumnami:
                           # Lp., Osoba Decyzyjna, Komórka, Telefon, Email,
                           # Wygląd na komputerze, Wygląd na telefonie, B2B/B2C,
                           # SSL (kłódka), Możliwości płatności, Szybkość,
                           # Google Ads, Shopping, Meta Ads, Social Media, Inne
output_file = 'output.csv' # Plik wynikowy w formacie wymaganym przez Kit

with open(input_file, newline='', encoding='utf-8') as csvfile_in, \
     open(output_file, 'w', newline='', encoding='utf-8') as csvfile_out:
    
    reader = csv.reader(csvfile_in)
    writer = csv.writer(csvfile_out)
    
    # Nagłówek zgodny z wymaganiami Kit:
    # First name, Last name, Email address, Tags
    writer.writerow(['First name', 'Last name', 'Email address', 'Tags'])
    
    for row in reader:
        # Pomijamy wiersz nagłówka, jeśli zawiera "Lp."
        if row[0].strip() == "Lp.":
            continue
        
        # Indeksy:
        # 0 - Lp.
        # 1 - Osoba Decyzyjna
        # 2 - Komórka (ignorujemy)
        # 3 - Telefon (ignorujemy)
        # 4 - Email
        # 5 - Wygląd na komputerze
        # 6 - Wygląd na telefonie
        # 7 - B2B/B2C (pomijamy)
        # 8 - SSL (kłódka)
        # 9 - Możliwości płatności
        # 10 - Szybkość
        # 11 - Google Ads
        # 12 - Shopping
        # 13 - Meta Ads
        # 14 - Social Media
        # 15 - Inne
        osoba_decyzyjna = row[1].strip() if len(row) > 1 else ""
        email_address = row[4].strip() if len(row) > 4 else ""
        
        # Wyodrębniamy imię i nazwisko z "Osoba Decyzyjna"
        tokens = osoba_decyzyjna.split()
        if tokens:
            imie = tokens[0].capitalize()
            nazwisko = tokens[-1].capitalize()
        else:
            imie = ""
            nazwisko = ""
        
        # Przekształcamy imię do formy wołacza
        first_name = transform_name_heuristic(imie) if imie else ""
        
        # Rozpoznajemy płeć – jeśli brak imienia, wstawiamy tag "brak imienia"
        if imie:
            gender_tag = rozpoznaj_plec(imie)
        else:
            gender_tag = "brak imienia"
        
        # Budujemy listę tagów zaczynając od tagu płci
        tags_list = [gender_tag]
        
        # Sprawdzamy kolumny 5..15 (od "Wygląd na komputerze" do "Inne")
        feature_columns = row[5:16]  # uzyskujemy 11 kolumn
        # Założenie: jeśli któraś kolumna zawiera dokładnie ",", to oznacza, że funkcja jest posiadana
        has_any_feature = any(col.strip() == ',' for col in feature_columns)
        if not has_any_feature:
            tags_list.append("brak strony")

        # Jeśli jest "brak strony", dodajemy dodatkowo tagi "GoogleAds-brak" i "MetaAds-brak"
        if "brak strony" in tags_list:
            if "GoogleAds-brak" not in tags_list:
                tags_list.append("GoogleAds-brak")
            if "MetaAds-brak" not in tags_list:
                tags_list.append("MetaAds-brak")
        
        # Dodajemy tag "Slaba strona" jeżeli:
        # - W kolumnie "Wygląd na telefonie" (indeks 6) lub "Wygląd na komputerze" (indeks 5) znajduje się dokładnie "."
        # - I nie został dodany tag "brak strony"
        wyglad_telefon = row[6].strip() if len(row) > 6 else ""
        wyglad_komputera = row[5].strip() if len(row) > 5 else ""
        if (wyglad_telefon == '.' or wyglad_komputera == '.') and "brak strony" not in tags_list:
            tags_list.append("Slaba strona")
        
        # Dodajemy tag "GoogleAds-brak" jeżeli:
        # - W kolumnie "Google Ads" (indeks 11) znajduje się dokładnie "."
        google_ads = row[11].strip() if len(row) > 11 else ""
        if google_ads == '.':
            tags_list.append("GoogleAds-brak")
        
        # Dodajemy tag "GoogleAds-slabe" jeżeli:
        # - W kolumnie "Google Ads" (indeks 11) znajduje się dokładnie ","
        # - W kolumnie "Shopping" (indeks 12) znajduje się dokładnie "."
        shopping = row[12].strip() if len(row) > 12 else ""
        if google_ads == ',' and shopping == '.':
            tags_list.append("GoogleAds-slabe")
        
        # Dodajemy tag "MetaAds-brak" jeżeli:
        # - W kolumnie "Meta Ads" (indeks 13) znajduje się dokładnie "."
        meta_ads = row[13].strip() if len(row) > 13 else ""
        if meta_ads == '.':
            tags_list.append("MetaAds-brak")
        
        # Dodajemy tag "Wszystko maja" jeżeli we wszystkich istotnych kolumnach (pomijając B2B/B2C) wartość wynosi dokładnie ","
        # Kolumny: 5 - Wygląd na komputerze, 6 - Wygląd na telefonie, 8 - SSL (kłódka), 9 - Możliwości płatności,
        # 10 - Szybkość, 11 - Google Ads, 12 - Shopping, 13 - Meta Ads, 14 - Social Media
        features_for_wszystko = [row[i].strip() for i in [5, 6, 8, 9, 10, 11, 12, 13, 14] if len(row) > i]
        if len(features_for_wszystko) == 9 and all(col == ',' for col in features_for_wszystko):
            tags_list.append("Wszystko maja")
        
        # Dodajemy tag "import-1" do każdego wiersza
        tags_list.append("import-1")
        
        # Łączymy tagi przecinkiem
        tags = ", ".join(tags_list)
        
        # Zapisujemy wiersz wynikowy
        writer.writerow([first_name, nazwisko, email_address, tags])

print("Przetwarzanie CSV zakończone. Wynik zapisany w pliku:", output_file)
