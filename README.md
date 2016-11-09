# Astrotracker

# Program liczacy predkosci

programik liczący prędkości do sterowania silnikiem krokowym dla roznego typu amatorskich napędów paralaktycznych.
W przyszłości może coś więcej.

Program liczy predkosci potrzebne dla sterowania silnikiem krokowym napędów nożycowych lub koziołków. 
Wyrzuca listy prędkosci w formie do wklejenia do kodu programu sterującego
Parametry należy zadać przed wyedytowanie zmiennych zamieszczonych na początku kodu programu, a następnie odpalenie skryptu w Python 3. Rezultaty w plikach tekstowych.

# Projekt napędu.

Narazie to, co z całego napędu działa najsensowniej. 2 identyczne ramiona do wycięcia w plexi lub sklejce. Obracają się na łożysku oporowym 52mm średnicy. ramiona są ściskane przez 2 krążku wycięte najlepiej z aluminium, ściskane przez kawałek śruby M5 z dwiema nakrętkami samohamownymi. Zapewnia to płynny ruch. Na ile zapewnia stałą oś obrotu -  nie wiem. 

Do jednej z plytek nalezy przytwierdzić mocowanie głowicy foto(śruba 3/8 lub 1/4 cala). do drugiej mocowanie do głowicy statywu(nakrętka 3/8 lub 1/4 cala) lub klin paralaktyczny.

W bliższy otwór wchodzi lunetka biegunowa. Nie jest ona jednak optymalnym rozwiązaniem tutaj, ponieważ celowanie przez nią jest niemal niemożliwe bez zastosowania zielonego lasera, którym świecimy przez lunetkę. Najlepszym rozwiązaniem byloby kolimowalne mocowanie zielonej diody laserowej. Umieszczenie celownika na biegun na ramieniu pozwala na łatwą kolimację z rzeczywista osią obrotu poprzez obracanie ramienia i sprawdzanie, czy laser świeci cały czas w to samo miejsce.

W dalsze otwory wchodzi ułozyskowane mocowanie nakrętki prowadzącej oraz śruby napędowej . Narazie nie rozwiązałem tego problemu w zadowalajacy sposób



# Program sterujący

Przykładowy kod programu sterującego arduino. Do sterowania wykorzstamy prosty shield wraz z tanim sterownikiem silnika krokowegu 28-BYJ4 (koszt jakies 25zł).
Do kodu wstawiamy predkosci policzone przez program.


# Elektronika shielda Arduino

Będzie

# Proste testowanie PE takiego napędu

Ustawiamy napęd 20-30 stopni od polarnej. Ustawiamy obiektyw 90 st od osi obrotu napędu. Ustawiamy niskie ISO i jakied 3-4 min ekspozycji. Po tym czasie, oglądamy uzyskane slady gwiazd, i jeśli PE jest znaczny, widzimy fale o częstotliwosci PE. PE powienien byc w zasadzie niewidoczny, jeśli uzyskana precyzja prowadzenia jest zadowalająca.
