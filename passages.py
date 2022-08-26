import datetime
import calendar
from itertools import count
from operator import indexOf
import random
import csv
import os
from tkinter import W
import matplotlib.pyplot as plt
import numpy as np
import itertools


#importation fichier patterns
os.chdir('..\\')
f = open('patterns.csv', 'r')
spamreader = csv.reader(f, delimiter=',', quotechar='|')

afv = {'601': {'cam' : ['Anière', 'Renfile']}, '602' : {'cam' : ['Pierre à Bochet', 'Thônex']}, '603' : {'cam' : ['Veyrier', 'Troinex']}, '605' : {'cam' : ['Bardonnex', 'Perly']}, '606' : {'cam' : ['Meyrin', 'Dardagny']}, '607':{'cam' : ['Ferney', 'Vireloup']}, '555' : {'cam': ['Saint Prex']}}

#faire une liste regroupant tous les passages pour ne pas avoir 2 fois le même passage sur la même cam (voitures en même temps)
passages_cam = []

#fonction test descriptifs
def description_data(cle, valeur):
        k = 0
        cle = cle
        valeur = valeur
        for vehicle in dictVhc :
                if vehicle[cle] == valeur:
                        k += 1
        txt = 'le nombre de véhicules avec la clé {} est de {}'
        print(txt.format(valeur,k))

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

#variable pour appel de la fonction calendar
cal = calendar.Calendar()



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
        #txt = 'le nombre de véhicules avec le pattern {} est de {}'
        #print(txt.format(pattern,i))
        return i

#definition de l'horodatage et du sens des passages pour les passages erratique
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


'''
for values in sporadique(20):
        print(values)
'''
#########################################################################
###############               Véhicules FRA               ###############
#########################################################################

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

###############            Pattern weekend               ################

#liste des jeudis, vendredis et samedis soir du mois
jedredis = [week for week in cal.monthdatescalendar(annee, mois)]

jedredis = [[datetime.datetime(day.year,day.month,day.day) for day in week
            if day.strftime('%a') == 'Thu' or day.strftime('%a') == 'Fri' or day.strftime('%a') == 'Sat' and day.month == mois]
        for week in jedredis]
jedredis = list(filter(None, jedredis))
jedredis = [element for liste in jedredis for element in liste]


for vehicle in dictVhc :
    if vehicle['pattern'] == 'weekend':
        passages = []
        result = []
        cam = choix_camera()
        while cam == 'Saint Prex':
                cam = choix_camera()
        nbreDeFois = random.randint(1, len(jedredis))
        for x in range(nbreDeFois):
                jours = random.choice(jedredis)
                while jours in result:
                        jours = random.choice(jedredis)
                if jours not in result:
                        result.append(jours)
        result.sort()
        
        for x in range(len(result)):
                selectionJours = result[x]
                horaireIn = selectionJours + datetime.timedelta(hours=random.randint(19,23),minutes=random.randint(0,59), seconds=random.randint(0,59))
                horaireOut = horaireIn + datetime.timedelta(hours=random.randint(2,5),minutes=random.randint(0,59), seconds=random.randint(0,59))
                passages.append([cam, ('IN', horaireIn)])
                passages.append([cam, ('OUT', horaireOut)])
        vehicle['passages'] = passages

###############            Pattern frontalierVhcEntreprise               ################

for vehicle in dictVhc:
        if vehicle['pattern']== 'frontalierVhcEntreprise':
                cam = choix_camera()
                while cam == 'Saint Prex':
                        cam = choix_camera()
                for values in frontaliers():
                        donnee = []
                        donnee.append(cam)
                        donnee.append(values)
                        vehicle['passages'].append(donnee)
        



#########################################################################
###############               Véhicules CHE               ###############
#########################################################################

###############               Pattern fisc               ################
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

###############               Pattern intérieur               ###############
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

#création passages aléatoires pour les véhicules ayant un pattern "intérieur"
def random_inland():

        #création liste jours aléatoires
        joursDuMois = []
        for i in range(random.randrange(1,20)):
                joursDuMois.append(random.randrange(1,nbreJoursMois+1))
                joursDuMois.sort()

        #conversion en datetime
        for i in range(len(joursDuMois)):
                joursDuMois[i] = datetime.datetime(annee,mois,joursDuMois[i],random.randrange(0,24),random.randrange(0,60),random.randrange(0,60))
        joursDuMois.sort()
        def sens():
                sensAleatoire = random.choice(['IN', 'OUT'])
                yield sensAleatoire
                for i in range(len(joursDuMois)):
                        if sensAleatoire == 'IN':
                                sensAleatoire = 'OUT'
                                yield sensAleatoire
                        else:
                                sensAleatoire = 'IN'
                                yield sensAleatoire
        InOut = sens()


        #création de la liste avec cam sens et heure
        newlist=[['Saint Prex',(next(InOut),x)] for x in joursDuMois]


        return newlist

                
        

#attribution de l'horodatage pour les patterns intérieur
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
                else:
                        vehicle['passages'] = random_inland()
                
###############               Pattern courses en France               ###############               
#attribution de l'horodatage pour les patterns courses en France


JoursOuvrablesDuMois = [week for week in cal.monthdatescalendar(annee, mois)]

JoursOuvrablesDuMois = [[day for day in week
            if day.strftime('%a') != 'Sun' and day.month == mois]
        for week in JoursOuvrablesDuMois]

for vehicle in dictVhc :
    if vehicle['pattern'] == 'courses en France':
        nbreDeFois = random.randint(1, len(JoursOuvrablesDuMois))
        result = [9]*nbreDeFois
        passages = []
        cam = choix_camera()
        while cam == 'Saint Prex':
                cam = choix_camera()
        
        for x in range(len(result)):
                z = random.randrange(0, len(JoursOuvrablesDuMois))
                while z in result:
                        z = random.randrange(0, len(JoursOuvrablesDuMois))
                if z not in result:
                        result[x] = z
        result.sort()
        for x in result:
                selectionJours = random.choice(JoursOuvrablesDuMois[x])
                horaireOut = datetime.datetime(selectionJours.year,selectionJours.month,selectionJours.day) + datetime.timedelta(hours=random.randint(8,18),minutes=random.randint(0,59), seconds=random.randint(0,59))
                horaireIn = horaireOut + datetime.timedelta(hours=random.randint(1,3),minutes=random.randint(0,59), seconds=random.randint(0,59))
                passages.append([cam, ('OUT', horaireOut)])
                passages.append([cam, ('IN', horaireIn)])
        vehicle['passages'] = passages
        

###############               Pattern erratique               ###############
def erratique():
        joursDuMois = list(cal.itermonthdates(annee, mois))

        joursDuMois = [datetime.datetime(day.year,day.month,day.day) for day in joursDuMois if day.month == mois]

        joursSelectionnes = list(set(random.choices(joursDuMois, k=random.randint(6,nbreJoursMois))))
        joursSelectionnes.sort()
        #print('les jours selectionnés sont : ',joursSelectionnes,'\n')
        passageFinal=[]
        for x in joursSelectionnes:
                passage= []
                nbreDeFois = random.randint(1, 5)
                heures = []
                while len(heures) != nbreDeFois:
                        h=random.randint(0, 23)
                        while h in heures:
                                h=random.randint(0, 23)
                        heures.append(h)
                        heures.sort()
                #print('les heures sont : ', heures)
                for z in range(nbreDeFois):
                        passage.append([choix_camera(),(random.choice(['IN', 'OUT']),x.replace(hour=heures[z],minute=random.randint(0,59),second=random.randint(0,59)))])
                passageFinal = passageFinal + passage
        return passageFinal

for vehicle in dictVhc :
    if vehicle['pattern'] == 'erratique':
        vehicle['passages']=erratique()



#########################################################################
###############               Véhicules ESP               ###############
#########################################################################

###############               Pattern vacances              #############
#samedis du mois
listeSamedis = [week for week in cal.monthdatescalendar(annee, mois)]

listeSamedis = [[datetime.datetime(day.year,day.month,day.day) for day in week
            if day.strftime('%a') == 'Sat' and day.month == mois]
        for week in listeSamedis]
listeSamedis = filter(None, listeSamedis)


list_cycle = itertools.pairwise(listeSamedis)
list_cycle = list(list_cycle)
#next(list_cycle)
#semaineDeVacance = [x + next(list_cycle) for x in listeSamedis if x[i] != x[0]]
#print(semaineDeVacance)
#print(list_cycle)
#print('le nombre de paires est de : ',len(list_cycle))
def vacances():
        passages= []
        choixSemaine = random.choice(list_cycle)
        passages = list((['Bardonnex', ('IN', choixSemaine[0][0].replace(hour=random.randint(6,12),minute=random.randint(0,59),second=random.randint(0,59)))],['Bardonnex', ('OUT', choixSemaine[1][0].replace(hour=random.randint(12,23),minute=random.randint(0,59),second=random.randint(0,59)))]))
        return passages
for vehicle in dictVhc:
        if vehicle['pattern']== 'vacances':
                vehicle['passages'] = vacances()



#########################################################################
###############                Autobus                    ###############
#########################################################################


def flix():
        camBus = [['Bardonnex', 'Thônex'],['Saint Prex']]
        passages = []
        joursDuMois = list(cal.itermonthdates(annee, mois))
        joursDuMois = [datetime.datetime(day.year,day.month,day.day) for day in joursDuMois if day.month == mois]
        def passage_flix():
                p = random.choice(camBus)
                if len(p) >1:
                        p = random.choice(p)
                else:
                        p = ''.join(p)
                sensBus = ['IN', 'OUT']
                t = joursDuMois[0] + datetime.timedelta(hours=8, minutes=25)
                passages.append([p,(random.choice(sensBus),t)])
                
        passages.append(passage_flix()) 
        return passages

test = flix()
print(test)



'''
        passages =[]
        result = []
        t = None
        def passage_flix():
                if len(result) != 0:
                        p = random.choice(camBus)
                        if len(p) >1:
                                p = random.choice(p)
                        else:
                                p = ''.join(p)
                else:
                        p=random.choice(camBus[0])
                return p
        result.append(passage_flix())
        result.append(('IN',t))
        passages.append(result)
        
        print(passages[len(passages)-1])

        
        return result


w = flix()



for vehicle in dictVhc:
        if vehicle['passages']!=[]:
                print(vehicle)
                break


for i in range(10):
        w = flix()
        print(w)
'''






'''
sensBus = ['IN','OUT']
result = []
t = None
g = random.choice(camBus[0])



for vehicle in dictVhc:
        if vehicle['pattern']=='flixbus':
                print(vehicle)

'''
'''
for vehicle in dictVhc:
        if vehicle['pattern']== 'frontalier':
                print(vehicle, '\n') 

for vehicle in dictVhc:
        if vehicle['passages']==[]:
                print(vehicle)

for vehicle in dictVhc:
        if vehicle['pattern']== 'weekend':
                print(vehicle, '\n') 

description_data('pattern', 'courses en France')

for vehicle in dictVhc:
        if vehicle['pattern']== 'courses en France':
                print(vehicle, '\n')


for vehicle in dictVhc:
        if vehicle['passages']==[]:
                print(vehicle)

for vehicle in dictVhc:
        if vehicle['pattern']== 'vacances':
                print(vehicle)


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

description_data('pattern','erratique')
description_data('pattern','interieur')
description_data('pattern','courses en France')


for vehicle in dictVhc:
        if vehicle['passages']==[]:
                print(vehicle)


description_data('pays','CHE')
description_data('pays','FRA')
description_data('pays','ESP')

pattern_data('erratique')
pattern_data('interieur')
pattern_data('frontalier')
pattern_data('sporadique')
pattern_data('ouvreuse')
pattern_data('interieur')




timage = []
#extraction passages WIP
StPrexIn = 0
StPrexOut = 0
for vehicle in dictVhc:
        if vehicle['passages']!=[]:
                for passages in vehicle['passages']:
                        if passages[0] == 'Saint Prex' and passages[1][0] == 'IN':
                                timage.append(passages[1][1].strftime('%X'))


for vehicle in dictVhc:
        if vehicle['pattern']== 'courses en France':
                print(vehicle, '\n')

#graphiques       
print(StPrexIn)
print(StPrexOut)

plt.hist(timage)
plt.show()



for vehicle in dictVhc:
        if vehicle['pattern']== 'erratique':
                print(vehicle)
'''