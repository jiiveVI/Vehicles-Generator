import datetime
import calendar
from operator import indexOf
import random
import csv
import os
from tkinter import W


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

#calcul du nombre de véhicule avec un pattern donné
def pattern_data(pattern):
        i=0
        for vehicle in dictVhc :
                if vehicle['pattern'] == pattern:
                        i+=1
        txt = 'le nombre de véhicules avec le pattern {} est de {}'
        #print(txt.format(pattern,i))
        return i

#definition de l'horodatage et du sens des passages pour les passages sporadiques
def sporadique(nbrePassages):
        tempsIn = horodatage(annee, mois, random.randrange(1,nbreJoursMois), 0, 24)
        for i in range(nbrePassages):
                tempsIn = tempsIn + datetime.timedelta(days=random.randrange(0,5), hours=random.randrange(
                0, 10), minutes=random.randrange(0, 60), seconds=random.randrange(0, 60))
                
                tempsOut = tempsIn + datetime.timedelta(days=random.randrange(0,5), hours=random.randrange(
                0, 10), minutes=random.randrange(0, 60), seconds=random.randrange(0, 60))
                if tempsIn > datetime.datetime(2022,9,30,23,59,59) or tempsOut > datetime.datetime(2022,9,30,23,59,59):
                        break
                yield 'IN', tempsIn
                yield 'OUT', tempsOut
                
                i+=1



for values in sporadique(20):
        print(values)

###############               Véhicules FRA               ###############

#definition de l'horodatage et du sens des passages pour les frontaliers 
def frontaliers():
        x = 1
        tempsIn = horodatage(annee, mois, x, 6, 9)
        while x <= nbreJoursMois:
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
        
def interieur(aller = 'IN', retour = 'OUT'):
        x = 1
        tempsIn = horodatage(annee, mois, x, 6, 9)
        while x <= nbreJoursMois:
                if tempsIn.strftime('%a') != 'Sat' and tempsIn.strftime('%a') != 'Sun':
                        yield aller ,tempsIn
                        tempsOut = tempsIn + datetime.timedelta(hours=random.randrange(
                        9, 10), minutes=random.randrange(0, 60), seconds=random.randrange(0, 60))
                        yield retour, tempsOut
                        x += 1
                        tempsIn = tempsIn + datetime.timedelta(days=1,minutes=random.randrange(-20,20),seconds=random.randrange(-60,60))
                else:
                        x += 1
                        tempsIn = tempsIn + datetime.timedelta(days=1,minutes=random.randrange(-20,20),seconds=random.randrange(-60,60))

#attribution de l'horodatage type pendulaire pour les patterns intérieur
n=0
for vehicle in dictVhc :
        if vehicle['pattern'] == 'interieur':
                if  n < pattern_data('interieur')//3:
                        n+=1
                        cam = 'Saint Prex'
                        for values in interieur('OUT','IN'):
                                donnee = []
                                donnee.append(cam)
                                donnee.append(values)
                                vehicle['passages'].append(donnee)
                        #print(vehicle)
                        #print(n)
                elif  n >= pattern_data('interieur')//3 and n < (pattern_data('interieur')//3)*2 :
                        n+=1
                        cam = 'Saint Prex'
                        for values in interieur():
                                donnee = []
                                donnee.append(cam)
                                donnee.append(values)
                                vehicle['passages'].append(donnee)
                        #print(vehicle)
                        #print(n)
                

                        

'''
                        
                                z+=1
                                


                        cam = 'Lambda'
                        for values in interieur('OUT','IN'):
                                donnee = []
                                donnee.append(cam)
                                donnee.append(values)
                                vehicle['passages'].append(donnee)
                        z += 1
                        print(vehicle)    
                        print('z est :', z)
                                
                
                


r=0
for vehicle in dictVhc :
    if vehicle['pattern'] == 'interieur'and len(vehicle['passages']) == 0:
        print('celui ci est compté', vehicle)
        r+=1
        print(r)
print('le nombre de vehicule avec passages non attribués est de ', r)




#affichage de la liste des pasages pour les frontaliers
for vehicle in dictVhc :
        cumul = []
        if vehicle['pattern'] == 'frontalier':
                
                for z in range(len(vehicle['passages'])):
                        cumul.append(vehicle['passages'][z])
                print(cumul)


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
description_data('pattern','ouvreuse')

pattern_data('interieur')
pattern_data('frontalier')
pattern_data('sporadique')
pattern_data('ouvreuse')
pattern_data('interieur')


for vehicle in dictVhc :
        if vehicle['pattern'] == 'frontalier':
                print(vehicle,'\n')'''
                