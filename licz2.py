#generuje program sterujacy silnikiem krokowym z biblioteki accelstepper(domyslne piny podlaczenia silnika 8,9,10,11), trzeba pokombinowac
#z kolejnoscia przylaczenia do silnika, ale powinno dac rade. Program zaklada w tym momencie sterowanie z zastosowaniem 3 przyciskow i 3 diodek.
#Generuje także zwykle listy predkosci i pozycji do wpisania do dowolnie zaprojektowanego programu dla Arduino.
#parametry nalezy ustalic w skrypcie a nastepnie puscic skrypt. Pliki wynikowe znajda sie w katalogu ze skryptem.

#Program jest przypuszczanie okropnie niedokladny i liczy wszystko numerycznie krok za krokiem




import math

ramie = 270			#dlugosc ramienia montazu mm
skok =  1.25			#skok sruby prowadzącej mm
kroki = 4075	#ilosc krokow/obrot silnika krokowego
przelozenie = 144		#przelozenie slimaka, jesli obecny
typ =	"nozyce"			#typ napedu "koziolek","nozyce","slimak"
ogniskowa = 600		#ogniskowa obiektywy do policzenia dokladnosci mm
piksel = 4.3			#rozmiar piksela do policzenia dokladnosci um
rozrzut = 2			#teoretyczne maksymalne odchylenie prowadzenia w czasie "czas" dla policzenia dokładnosci piksele
czas = 180			#czas dla policzenia dokladnosci sekundy
koncowka = "ostry"			#kształt koncowki sruby prowadzacej "ostry" lub "kula"
promien_kuli = 4		#promien kuli konczacej srube prowadzaca koziolek mm
dlugosc = 250		#dlugosc sruby prowadzacej mm
dlugosc_startowa = 50 	#dlugosc rozwarcia ramion na poczatku prowadzenia mm


typ_montazu = "nozyce"  #wpisz: koziolek,koziolek-kula, nozyce,przekladnia.  okresla tym montazu dla ktorego chcemy wypisac program




def nozyce_count(rm,sk,kr,ogn,pix,roz,cz,dl,dl_str):
	pixelscale = (pix/ogn)*206.3
	speedlist = []					#lista pre
	positionlist = []                       #lista pozycji
	rad_speed = math.radians(360/24/3600)                 #predkosc obrotu w radianach na sekunde          
	screw_movement = sk/kr                  #predkosc wysuwu sruby w mm/skok
	rad_err = math.radians(((pix*roz*206.3)/ogn)/3600)	#maksymalny blad prowadzenia
	

	current_step = 0					#aktualny krok silnika
	current_screw_len = dl_str+current_step*screw_movement#aktualne wysuniecie sruby
	first_degree = math.asin((current_screw_len/2)/rm)
	new_degree =first_degree+rad_speed/2
	new_screw_position = math.sin(new_degree)*rm*2
	first_screw_movement = new_screw_position - dl_str
	first_speed = first_screw_movement/screw_movement #predkosc startowa w step/s
	recent_speed = first_speed              #przypisuje aktualna predkosc jako predkosc startowa
	recent_speed_position = 0
	current_speed_position = 0

	
	while current_screw_len < dl:
		current_degree = math.asin((current_screw_len/2)/rm)			#aktualny kat rozwarcia nozyc
		new_degree =current_degree+rad_speed/2
		new_screw_position = math.sin(new_degree)*rm*2
		current_screw_movement = new_screw_position-current_screw_len             #dlugosc, o jaka ma sie przesunac sruba w ciagu 1s przy aktualnym rozwarciu		
		current_speed = current_screw_movement/screw_movement					#dokladna predkosc dla danego kroku
		recent_speed_position =recent_speed_position	+ recent_speed	#pozycja silnika, tak jakby poruszał się z prędkościa ustaloną ostatnio
		current_speed_position =current_speed_position + current_speed 			#pozycja silnika, tak jakby poruszał się z dokładnie ustalaną predkoscia
		position_err = math.fabs((current_speed*cz*screw_movement)-(recent_speed*cz*screw_movement))					#ilosc mm bledu
		cumulative_err = math.fabs(current_degree-(math.asin(((current_screw_len+position_err)/2)/rm)))					#aktualnie nagromadzony blad w radianach
		current_step = current_speed_position
		current_screw_len = dl_str+current_step*screw_movement
		if cumulative_err > rad_err :
			speedlist.append(recent_speed)		#dodaj recent speed do listy predkosci
			positionlist.append(recent_speed_position)		#dodaj recent_speed_position do listy pozycji, na ktorych ma sie konczyc dzialanie z dana predkoscia
			recent_speed = current_speed            #uaktualnij recent speed
			current_step = recent_speed_position   #uaktualnij pozycje, tak aby odpowiadala rzeczywistosci
			current_speed_position = recent_speed_position
			
	required_precision = math.sin(rad_err*roz)*rm                #wymagana precyzja ruchu sruby
	drive_time = ((math.degrees(current_degree*2-first_degree*2))/360)*24*60                                                #czas prowadzenia
	
	return drive_time,required_precision,speedlist,positionlist,pixelscale
	
	
def koziolek_kula(rm,sk,kr,ogn,pix,roz,cz,dl,dl_str,pk):
	pixelscale = (pix/ogn)*206.3
	speedlist = []					#lista pre
	positionlist = []                       #lista pozycji
	rad_speed = math.radians(360/24/3600)                 #predkosc obrotu w radianach na sekunde          
	screw_movement = sk/kr                  #predkosc wysuwu sruby w mm/skok
	rad_err = math.radians(((pix*roz*206.3)/ogn)/3600)	#maksymalny blad prowadzenia
	
	current_step = 0					#aktualny krok silnika                   
	current_screw_len = dl_str+current_step*screw_movement #aktualne wysuniecie sruby
	first_degree = math.atan(current_screw_len/rm)
	current_ball_offset = pk-(pk*math.cos(first_degree))
	current_screw_len = current_screw_len - current_ball_offset
	new_degree =first_degree+rad_speed
	new_screw_position = math.tan(new_degree)*rm
	first_screw_movement = new_screw_position - dl_str
	first_speed = first_screw_movement/screw_movement #predkosc startowa w step/s
	recent_speed = first_speed              #przypisuje aktualna predkosc jako predkosc startowa
	recent_speed_position = 0
	current_speed_position = 0

	
	while current_screw_len < dl:
		current_degree = math.atan(current_screw_len/rm)			#aktualny kat rozwarcia nozyc
		new_degree =current_degree+rad_speed
		new_screw_position = math.tan(new_degree)*rm
		current_screw_movement = new_screw_position-current_screw_len             #dlugosc, o jaka ma sie przesunac sruba w ciagu 1s przy aktualnym rozwarciu
		new_screw_movement = screw_movement*(current_screw_len/(current_screw_len+current_ball_offset))		
		current_speed = current_screw_movement/new_screw_movement					#dokladna predkosc dla danego kroku
		recent_speed_position =recent_speed_position	+ recent_speed	#pozycja silnika, tak jakby poruszał się z prędkościa ustaloną ostatnio
		current_speed_position =current_speed_position + current_speed 			#pozycja silnika, tak jakby poruszał się z dokładnie ustalaną predkoscia
		position_err = math.fabs((current_speed*cz*new_screw_movement)-(recent_speed*cz*new_screw_movement))					#ilosc mm bledu
		cumulative_err = math.fabs(current_degree-(math.atan((current_screw_len+position_err)/rm)))					#aktualnie nagromadzony blad w radianach
		current_step = current_speed_position
		current_screw_len = dl_str+current_step*screw_movement
		current_degree = math.atan(current_screw_len/rm)
		current_ball_offset = pk-(pk*math.cos(current_degree))
		current_screw_len = current_screw_len - current_ball_offset
		if cumulative_err > rad_err :
			speedlist.append(recent_speed)		#dodaj recent speed do listy predkosci
			positionlist.append(recent_speed_position)		#dodaj recent_speed_position do listy pozycji, na ktorych ma sie konczyc dzialanie z dana predkoscia
			recent_speed = current_speed            #uaktualnij recent speed
			current_step = recent_speed_position   #uaktualnij pozycje, tak aby odpowiadala rzeczywistosci
			current_speed_position = recent_speed_position
			
	required_precision = math.tan(rad_err*roz)*rm            #dokladnosc ruchu sruby w um
	drive_time = ((math.degrees(current_degree-first_degree))/360)*24*60    #czas prowadzenia 
	print(current_screw_len)

	return drive_time,required_precision,speedlist,positionlist,pixelscale
	
	
def koziolek_count(rm,sk,kr,ogn,pix,roz,cz,dl,dl_str):
	pixelscale = (pix/ogn)*206.3
	speedlist = []					#lista pre
	positionlist = []                       #lista pozycji
	rad_speed = math.radians(360/24/3600)                 #predkosc obrotu w radianach na sekunde          
	screw_movement = sk/kr                  #predkosc wysuwu sruby w mm/skok
	rad_err = math.radians(((pix*roz*206.3)/ogn)/3600)	#maksymalny blad prowadzenia
	
	current_step = 0					#aktualny krok silnika
	current_screw_len = dl_str+current_step*screw_movement#aktualne wysuniecie sruby
	first_degree = math.atan(current_screw_len/rm)
	new_degree =first_degree+rad_speed
	new_screw_position = math.tan(new_degree)*rm
	first_screw_movement = new_screw_position - dl_str
	first_speed = first_screw_movement/screw_movement #predkosc startowa w step/s
	recent_speed = first_speed              #przypisuje aktualna predkosc jako predkosc startowa
	recent_speed_position = 0
	current_speed_position = 0

	
	while current_screw_len < dl:
		current_degree = math.atan(current_screw_len/rm)			#aktualny kat rozwarcia nozyc
		new_degree =current_degree+rad_speed
		new_screw_position = math.tan(new_degree)*rm
		current_screw_movement = new_screw_position-current_screw_len             #dlugosc, o jaka ma sie przesunac sruba w ciagu 1s przy aktualnym rozwarciu		
		current_speed = current_screw_movement/screw_movement					#dokladna predkosc dla danego kroku
		recent_speed_position =recent_speed_position	+ recent_speed	#pozycja silnika, tak jakby poruszał się z prędkościa ustaloną ostatnio
		current_speed_position =current_speed_position + current_speed 			#pozycja silnika, tak jakby poruszał się z dokładnie ustalaną predkoscia
		position_err = math.fabs((current_speed*cz*screw_movement)-(recent_speed*cz*screw_movement))					#ilosc mm bledu
		cumulative_err = math.fabs(current_degree-(math.atan((current_screw_len+position_err)/rm)))					#aktualnie nagromadzony blad w radianach
		current_step = current_speed_position
		current_screw_len = dl_str+current_step*screw_movement
		if cumulative_err > rad_err :
			speedlist.append(recent_speed)		#dodaj recent speed do listy predkosci
			positionlist.append(recent_speed_position)		#dodaj recent_speed_position do listy pozycji, na ktorych ma sie konczyc dzialanie z dana predkoscia
			recent_speed = current_speed            #uaktualnij recent speed
			current_step = recent_speed_position   #uaktualnij pozycje, tak aby odpowiadala rzeczywistosci
			current_speed_position = recent_speed_position
			
	required_precision = math.tan(rad_err*roz)*rm            #dokladnosc ruchu sruby w um
	drive_time = ((math.degrees(current_degree-first_degree))/360)*24*60    #czas prowadzenia 
	print(current_screw_len)
	
	return drive_time,required_precision,speedlist,positionlist,pixelscale


def przekladnia_count(przel,kr,ogn,pix):
	
	ziarnistosc = (360*3600)/(przel*kr)
	predkosc = (kr*przel)/(24*3600)	
	pixelscale = (pix/ogn)*206.3
	ziarnistosc = ziarnistosc/pixelscale
	
	
	
	
	return predkosc,ziarnistosc,pixelscale
	
def writefile_koziolki(czas,prec,speeds,positions,pixel):
	outfilename = "info_i_predkosc.txt"
	file = open(outfilename, 'w')
	file.write("skala piksela będzie wynosiła " + str(pixel) + ' \"\n')
	file.write("naped bedzie prowadzil przez " + str(czas) + ' min\n')
	file.write("wymagana precyzja ruchu sruby wynosi " + str(prec) + ' mm\n')
	file.write("lista predkosci do kontroli silnika krokowego:\n" )
	file.write("\n")
	n=1
	for item in speeds:
		file.write("float speed"+str(n)+" = " + str(item)+";\n")
		n+=1
	file.write("\n")
	file.write("lista pozycji do kontroli silnika krokowego:\n" )
	file.write("\n")
	n=1
	for item in positions:
		file.write("long position"+str(n)+" = " + str(int(item))+";\n")
		n+=1
	
	file.close()
	
	return None
	
def writefile_przekladnia(pred,ziar,pixel):
	outfilename = "info_i_predkosc.txt"
	file = open(outfilename, 'w')
	file.write("skala piksela będzie wynosiła " + str(pixel) + ' \"\n')
	file.write("natomiast ziarnistosc prowadzenia to min " + str(ziar) +" \"\n")
	file.write("Predkosc obrotowa silnika powinna wynosic " +str(pred)+" step/s")
	file.close()
	

	
	
	
if typ_montazu == "koziolek":
	czas,prec,speeds,positions,pixelscale = koziolek_count(ramie,skok,kroki,ogniskowa,piksel,rozrzut,czas,dlugosc,dlugosc_startowa)
	writefile_koziolki(czas,prec,speeds,positions,pixelscale)
elif typ_montazu == "koziolek-kula":
	czas,prec,speeds,positions,pixelscale = koziolek_kula(ramie,skok,kroki,ogniskowa,piksel,rozrzut,czas,dlugosc,dlugosc_startowa,promien_kuli)
	writefile_koziolki(czas,prec,speeds,positions,pixelscale)
elif typ_montazu == "nozyce":
	czas,prec,speeds,positions,pixelscale = nozyce_count(ramie,skok,kroki,ogniskowa,piksel,rozrzut,czas,dlugosc,dlugosc_startowa)
	writefile_koziolki(czas,prec,speeds,positions,pixelscale)
elif typ_montazu == "przekladnia":
	pred,ziar,pixelscale = przekladnia_count(przelozenie,kroki,ogniskowa,piksel)
	writefile_przekladnia(pred,ziar,pixelscale)
	
	
	
	



#print(czas)
#print(prec)
#print(speeds[-1])
#print(positions)





