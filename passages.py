import datetime
import calendar
from operator import indexOf
import random
import csv
import os


#importation fichier patterns
os.chdir('.\Documents\projetsProg')
f = open('patterns.csv', 'r')
spamreader = csv.reader(f, delimiter=',', quotechar='|')

afv = {'601': {'cam' : ['Anière', 'Renfile']}, '602' : {'cam' : ['Pierre à Bochet', 'Thônex']}, '603' : {'cam' : ['Veyrier', 'Troinex']}, '605' : {'cam' : ['Bardonnex', 'Perly']}, '606' : {'cam' : ['Meyrin', 'Dardagny']}, '607':{'cam' : ['Ferney', 'Vireloup']}, '555' : {'cam': ['Saint Prex']}}

#faire une liste regroupant tous les passages pour ne pas avoir 2 fois le même passage sur la même cam (voitures en même temps)
passages_cam = []

#calculer le nombre de jours dans le mois
#jours = calendar.monthrange(2023,1)
#print(jours[1])

dictVhc = {}
vehicles = []


#tri des véhicules par type et nationalités
for row in spamreader:
        vehicles.append(row)


#fonction pour création de la liste
def build_liste_finale() :
    return [
        { 'id' : vehicle[0],
          'type' : vehicle[1],
          'marque' : vehicle[2],
          'modèle' : vehicle[3],
          'pays' : vehicle[4],
          'plaques' : vehicle[5],
          'pattern' : vehicle[6],
          'passages' : [],
       } for vehicle in vehicles]

#construction de la liste
dictVhc = build_liste_finale()

#fonction pour générer les horaires aléatoires

#input pour entrer la date
annee = 2022 #int(input('entrez l\'année\n'))

mois = 9 #int(input('entrez le mois\n'))

jours = 1 #int(input('entrez le jours\n'))


#défini le nombre de jours dans le mois
nbreJoursMois = calendar.monthrange(annee, mois)[1]
print(nbreJoursMois)



def horodatage(annee,mois,jours, heureMin, heureMax):
        annee = annee
        mois = mois
        jours = jours
        hh = random.randrange(heureMin, heureMax)
        mm = random.randrange(0,60)
        ss = random.randrange(0,60)
        temps = datetime.datetime(annee,mois,jours,hh,mm,ss)
        return temps

###############               Véhicules FRA               ###############

#definition de l'horodatage et du sens des passages pour les frontaliers 
def frontaliers():
        x = 1
        tempsIn = horodatage(annee, mois, x, 6, 9)
        while x < nbreJoursMois:
                if tempsIn.strftime('%a') != 'Sat' and tempsIn.strftime('%a') != 'Sun':
                        yield 'IN' ,tempsIn
                        tempsOut = tempsIn + datetime.timedelta(hours=random.randrange(
                        9, 10), minutes=random.randrange(0, 60), seconds=random.randrange(0, 60))
                        yield 'OUT',tempsOut
                        x += 1
                        tempsIn = tempsIn + datetime.timedelta(days=1,minutes=random.randrange(-20,20),seconds=random.randrange(-60,60))
                else:
                        x += 1
                        tempsIn = tempsIn + datetime.timedelta(days=1,minutes=random.randrange(-20,20),seconds=random.randrange(-60,60))
                        
        
                
#définition de la zone et de la caméra
def choix_camera():
    zone = random.choice(list(afv.keys()))
    cam = random.choice(afv.get(zone).get('cam'))
    return cam
choix_camera()
frontaliers()

# ajout des listes de passages et des caméras pour les frontaliers
for vehicle in dictVhc :
    if vehicle['pattern'] == 'frontalier':
        cam = choix_camera()
        while cam == 'Saint Prex':
                cam = choix_camera()
        for values in frontaliers():
                donnee = []
                donnee.append(cam)
                donnee.append(values)
                vehicle['passages'].append(donnee)



###############               Véhicules CHE               ###############

#definition de l'horodatage et du sens des passages pour les patterns Fisc
for vehicle in dictVhc :
    if vehicle['pattern'] == 'fisc':
        cam = choix_camera()
        while cam == 'Saint Prex':
                cam = choix_camera()
        for values in frontaliers():
                donnee = []
                donnee.append(cam)
                donnee.append(values)
                vehicle['passages'].append(donnee)

#definition de l'horodatage et du sens des passages pour les patterns intérieur du pays
for vehicle in dictVhc :
    if vehicle['pattern'] == 'fisc':
        cam = 'Saint Prex'







'''
#affichage de la liste des pasages pour les frontaliers
for vehicle in dictVhc :
        cumul = []
        if vehicle['pattern'] == 'frontalier':
                
                for z in range(len(vehicle['passages'])):
                        cumul.append(vehicle['passages'][z])
                print(cumul)
'''

#test descriptif
def description_data(cle, valeur):
        k = 0
        cle = cle
        valeur = valeur
        for vehicle in dictVhc :
                if vehicle[cle] == valeur:
                        k += 1
        txt = 'le nombre de {} est de {}'
        print(txt.format(valeur,k))

description_data('pays','CHE')
description_data('pays','FRA')
description_data('pays','ESP')