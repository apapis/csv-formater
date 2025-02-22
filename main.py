import csv

# Zbiór wyjątków – imiona, które mimo kończącej się na "a" nie są żeńskie
wyjatki_mesky = {"Kuba", "Barnaba", "Kosma"}

def rozpoznaj_plec(imie):
    """
    Rozpoznaje płeć na podstawie imienia.
    Jeśli imię jest w wyjątkach, zwraca 'Mężczyzna'.
    Jeśli imię kończy się na 'a', uznaje je za żeńskie.
    W innym przypadku zwraca 'Mężczyzna'.
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
input_file = 'input.csv'   # Oryginalny plik z kolumnami: Lp., Osoba Decyzyjna, Komórka, Telefon, Email
output_file = 'output.csv' # Wynikowy plik CSV w formacie wymaganym przez Kit

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
        
        # Wczytujemy dane z kolumn (resztę ignorujemy):
        # 0 - Lp. (nieużywane)
        # 1 - Osoba Decyzyjna
        # 4 - Email
        osoba_decyzyjna = row[1].strip() if len(row) > 1 else ""
        email_address = row[4].strip() if len(row) > 4 else ""
        
        # Rozbijamy "Osoba Decyzyjna" na tokeny -> imię (pierwszy), nazwisko (ostatni)
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
        
        # Tutaj tworzymy listę tagów – w tym przypadku tylko płeć (lub "brak imienia")
        tags = gender_tag  # jeśli chcesz więcej tagów, możesz je tu dodać i łączyć przecinkiem
        
        # Zapisujemy wiersz w formacie wymaganym przez Kit
        writer.writerow([first_name, nazwisko, email_address, tags])

print("Przetwarzanie CSV zakończone. Wynik zapisany w pliku:", output_file)
