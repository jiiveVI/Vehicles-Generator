import random
import csv
import os
from tkinter import Y

#importation fichier véhicules
os.chdir('.\Documents\projetsProg')
f = open('voitures.csv', 'r')
spamreader = csv.reader(f, delimiter=',', quotechar='|')

#création listes vides pour tri des véhicules
#voitures de livraison
deliveryFRA = []
deliveryCHE = []
deliveryESP = []

#voitures
carFRA = []
carCHE = []
carESP = []

#Autobus
busFRA = []
busCHE = []
busESP = []

#tri des véhicules par typse et nationalités
for row in spamreader:

    #véhicules de livraison
    if row[1] == 'Livraisons' and row[4] == 'FRA' :
        deliveryFRA.append(row)
    if row[1] == 'Livraisons' and row[4] == 'CHE' :
        deliveryCHE.append(row)
    if row[1] == 'Livraisons' and row[4] == 'ESP' :
        deliveryESP.append(row)

    #voitures
    if row[1] == 'Voiture' and row[4] == 'FRA' :
        carFRA.append(row)
    if row[1] == 'Voiture' and row[4] == 'CHE' :
        carCHE.append(row)
    if row[1] == 'Voiture' and row[4] == 'ESP' :
        carESP.append(row)

    #autobus
    if row[1] == 'Autobus' and row[4] == 'FRA' :
        busFRA.append(row)
    if row[1] == 'Autobus' and row[4] == 'CHE' :
        busCHE.append(row)
    if row[1] == 'Autobus' and row[4] == 'ESP' :
        busESP.append(row)

#patterns
#livraison france


#pattern assignement
#delivery pattern France -> plaques connues pour démarches en douane commerciale, plaques inconnues douane commerciale, passages inadéquats
patternLivraisonFrance = ['Douane OK', 'Douane KO', 'Vol 2 roues']
listePatternLivraisonFrance = random.choices(patternLivraisonFrance, weights=[4,3,2], k=len(deliveryFRA))
for i in range(len(deliveryFRA)):
    deliveryFRA[i][6] = listePatternLivraisonFrance[i]
#print(deliveryFRA)

#delivery pattern Swiss -> passages frontaliers(lu-ve), passages rapides A/R connu douanes commerciales, passages rapides A/R inconnu douanes commerciales
patternLivraisonSuisse = ['frontalierVhcEntreprise', 'achatsFranceDouaneOK','achatsFranceDouaneKO']
listePatternLivraisonSuisse = random.choices(patternLivraisonSuisse, weights=[4,3,2], k=len(deliveryCHE))
for i in range(len(deliveryCHE)):
    deliveryCHE[i][6] = listePatternLivraisonSuisse[i]
#print(deliveryCHE)

#delivery pattern Spain -> passages avec plaques connues douane commerciale, passages avec plaques inconnues douane commerciale
patternLivraisonEspagne = ['Douane OK', 'Douane KO']
listePatternLivraisonEspagne = random.choices(patternLivraisonEspagne, weights=[4,3], k=len(deliveryESP))
for i in range(len(deliveryESP)):
    deliveryESP[i][6] = listePatternLivraisonEspagne[i]
#print(deliveryESP)

#affichage des véhicules par type et nationalités
print('Le nombre de voitures françaises est : ' + str(len(carFRA)))
print('Le nombre de voitures suisses est : ' + str(len(carCHE)))
print('Le nombre de voitures espagnoles est : ' + str(len(carESP)))
print('Le nombre de bus français est : ' + str(len(busFRA)))
print('Le nombre de bus suisses est : ' + str(len(busCHE)))
print('Le nombre de bus espagnols est : ' + str(len(busESP)))
print('Le nombre de voitures de livraison françaises est : ' + str(len(deliveryFRA)))
print('Le nombre de voitures de livraison suisses est : ' + str(len(deliveryCHE)))
print('Le nombre de voitures de livraison espagnoles est : ' + str(len(deliveryESP)))

#connaitre le nombre de voiture restante
typelength = {'total voitures FRA' : len(carFRA), 'voitures FRA restantes ' : len(carFRA), 'total voitures CHE' : len(carCHE), 'total voitures ESP' : len(carESP)}

#fonctions pour générer les patterns
#patterns spécifiques

def random_car(x, action,type,cible = None):
    i=0
    global y
    y = 0
    while i < x:
        car = random.choice(type)
        if car[6] == 'indetermine':
            car[6]= action
            i+=1
        else:
            print('véhicule déjà assigné')
    for i in range(len(type)):        
        if type[i][6] == 'indetermine':
            y += 1
    print('le nombre de', type[i][1], type[i][4], ' non assigné est de ', y)
    
    
    
#complétion automatique
def rest_assign(type, action):
    for i in range(len(type)):
        if type[i][6] == 'indetermine':
            type[i][6] = action
        
#car pattern France -> frontaliers, weekend, sporadiques, DAB, ouvreuse, téléphonie, groupe telegram
random_car(1,'DAB', carFRA)
random_car(2,'ouvreuse',carFRA)
random_car(1,'téléphonie',carFRA)
random_car(2, 'telegram', carFRA)
random_car(2, 'sporadique', carFRA)
random_car(2, 'weekend', carFRA)
rest_assign(carFRA, 'frontalier')


for car in carFRA:
    print(car)



#car pattern Swiss -> courses en France, fisc, sporadiques, téléphonie, ouvreuse, telegram, intérieur du pays
random_car(y//12,'fisc', carCHE,)
random_car(6,'ouvreuse', carCHE)
random_car(4,'telegram', carCHE)
random_car(2,'téléphonie', carCHE)
random_car(y//10,'sporadiques', carCHE)
for car in carCHE:
    print(car)
random_car(y//3,'courses en France', carCHE)
for car in carCHE:
    print(car)

rest_assign(carCHE, 'interieur')

for car in carCHE:
    print(car)

#car pattern Spain -> livraison stup (600,stprex,600 rapide), vacances, TVA vhc
random_car(2,'stup', carESP)
random_car(4,'TVA', carESP)
rest_assign(carESP, 'vacances')

for car in carESP:
    print(car)

#bus pattern FRA -> flixbus, RPLF, cabotage (600,stprex,stprex,600)
random_car(2,'cabotage', busFRA)
random_car(1,'RPLF', busFRA)
rest_assign(busFRA, 'flixbus')

for car in busFRA:
    print(car)

#bus pattern Swiss -> Buchard
rest_assign(busCHE, 'buchard')

for car in busCHE:
    print(car)

#bus pattern Spain -> flixbus, RPLF, cabotage (600,stprex,stprex,600)
random_car(1,'cabotage', busESP)
random_car(1,'RPLF', busESP)
rest_assign(busESP, 'flixbus')

for car in busESP:
    print(car)



listeFinale = carCHE + carFRA + carESP + deliveryCHE + deliveryFRA + deliveryESP + busCHE + busFRA + busESP

car_header = ['id','type','marque', 'modele', 'pays', 'plaque','pattern']
with open('patterns.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(car_header)
    for i in range(len(listeFinale)):
        writer.writerow(listeFinale[i])
    csvfile.close()