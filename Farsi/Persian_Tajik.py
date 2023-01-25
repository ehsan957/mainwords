import csv
from googletrans import Translator
translator = Translator()
header = ['Persian', 'Tajik']
data = []
counter = 0
with open("Top100FarsiWords.txt",'r') as f:
    for line in f:
        persian = line.strip()
        tajik = translator.translate(persian, src='fa', dest='tg').text
        new_word = [persian, tajik]
        data.append(new_word)
        counter += 1
with open('Persian_Tajik.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data)