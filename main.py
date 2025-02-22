import csv

input_file = 'input.csv'
output_file = 'output.csv'

with open(input_file, newline='', encoding='utf-8') as csvfile_in, \
     open(output_file, 'w', newline='', encoding='utf-8') as csvfile_out:
    
    reader = csv.reader(csvfile_in)
    writer = csv.writer(csvfile_out)
    
    # Zapis nagłówka (opcjonalnie)
    writer.writerow(['Imie', 'Nazwisko'])
    
    for row in reader:
        full_name = row[1].strip()  # zakładamy, że pełne imię i nazwisko jest w drugiej kolumnie
        if not full_name:
            continue  # pomijamy puste wiersze
        
        tokens = full_name.split()
        
        if len(tokens) >= 2:
            # Używamy pierwszego tokena jako imienia oraz ostatniego jako nazwiska
            imie = tokens[0].capitalize()
            nazwisko = tokens[-1].capitalize()
        else:
            # Jeżeli mamy tylko jedno słowo, traktujemy je jako imię, nazwisko pozostaje puste
            imie = tokens[0].capitalize()
            nazwisko = ''
        
        writer.writerow([imie, nazwisko])

print("Przetwarzanie CSV zakończone. Wynik zapisany w pliku:", output_file)
