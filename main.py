import csv

# Zbiór wyjątków – imiona, które mimo kończącej się na "a" nie są żeńskie
wyjatki_mesky = {"Kuba", "Barnaba", "Kosma"}

def rozpoznaj_plec(imie):
    """
    Rozpoznaje płeć na podstawie imienia.
    Jeśli imię jest w zbiorze wyjątków, zwracamy "Mężczyzna".
    W przeciwnym wypadku, jeśli imię kończy się na "a", uznajemy je za żeńskie.
    """
    if imie in wyjatki_mesky:
        return "Mężczyzna"
    if imie[-1].lower() == "a":
        return "Kobieta"
    else:
        return "Mężczyzna"

def transform_name_heuristic(name):
    """
    Przekształca imię z mianownika do formy wołacza za pomocą heurystyk.
    Uwaga: Metoda nie obejmuje wszystkich wyjątków języka polskiego.
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
    if name[-1] not in vowels:
        return name + "ie"
    
    return name

input_file = 'input.csv'
output_file = 'output.csv'

with open(input_file, newline='', encoding='utf-8') as csvfile_in, \
     open(output_file, 'w', newline='', encoding='utf-8') as csvfile_out:
    
    reader = csv.reader(csvfile_in)
    writer = csv.writer(csvfile_out)
    
    # Zmieniamy nagłówek – zamiast kolumny "Imie" zapisujemy "Forma wołacza"
    # oraz dodajemy nową kolumnę "Tagi" (płeć)
    writer.writerow(['Forma wołacza', 'Nazwisko', 'Tagi'])
    
    for row in reader:
        # Załóżmy, że pełne imię i nazwisko znajduje się w kolumnie o indeksie 1
        full_name = row[1].strip()
        if not full_name:
            continue
        
        tokens = full_name.split()
        if len(tokens) >= 2:
            imie = tokens[0].capitalize()
            nazwisko = tokens[-1].capitalize()
        else:
            imie = tokens[0].capitalize()
            nazwisko = ''
        
        # Przekształcamy imię do formy wołacza
        vocative = transform_name_heuristic(imie)
        # Rozpoznajemy płeć na podstawie imienia (w mianowniku)
        plec = rozpoznaj_plec(imie)
        
        writer.writerow([vocative, nazwisko, plec])

print("Przetwarzanie CSV zakończone. Wynik zapisany w pliku:", output_file)
