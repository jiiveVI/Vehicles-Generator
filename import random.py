from itertools import count
import random
import csv
import os
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import numpy as np
import pandas as pd
os.path.realpath(__file__)
os.chdir('.\Documents\projetsProg')


#___items definition

Autobus = {'Iveco Bus':{'modèle':['Urbanway', 'Crealis', 'Crossway']}, 'man' :{'modèle': ['Lion\'s City', 'Lion\'s Classic', 'Lion\'s City Hybrid']}, 'Heuliez Bus' :{'modèle': ['GX 137', 'GX 337', 'GX Linium']}, 'Mercedes-Benz':{'modèle': ['Citaro C2', 'Citaro K', 'Citaro L']}}
Voiture = {'Bmw' : {'modèle':['X3','320','530','i8']}, 'Renault' : {'modèle':['Twingo','Clio','Scenic','Mégane']},'Toyota' : {'modèle':['Yaris','Celica','C-HR','Corolla']},'Peugeot' : {'modèle':['206','5008','3008','405']}, 'Mercedes-Benz' : {'modèle':['Classe A','Classe CLS','Classe SLK','Classe B']}, 'Audi' : {'modèle':['RS6','A8','Q5','e-tron']}}
Utilitaires = {'Renault' : {'modèle':['Trafic','Kangoo','Express']},'Citroën' : {'modèle':['Jumpy','Jumper','Berlingo']},'Volkswagen' : {'modèle':['Caddy','Crafter','Transporter',]}, 'Opel' : {'modèle':['Combo','Vivaro','Movano']}}
car_type = {}
choix_disponibles = ['Autobus', 'Voiture', 'Livraisons']



class vehicles():
    def __init__(self, id, type, marque, model, coutry, plate, spec):
        self.id = 0
        self.type = ''
        self.marque = ''
        self.model = ''
        self.country = ''
        self.plate = ''
        self.spec = ''

def chooseMarqueModel():
    sel_car_type = ''.join(random.choices(choix_disponibles, weights=[1,10,3], k=1))
    if sel_car_type == 'Autobus':
        car_type = Autobus
    elif sel_car_type == 'Voiture':
        car_type = Voiture
    elif sel_car_type == 'Livraisons':
        car_type = Utilitaires
    marque = random.choice(list(car_type.keys()))
    modele = random.choice(car_type.get(marque).get('modèle'))
    return sel_car_type, marque, modele

def createLicencePlate():
    nationality = ['CHE', 'FRA', 'ESP']
    country = ''.join((random.choices(nationality, weights=[4,3,1], k=1)))
    #print(country)
    chiffres = list('0123456789')
    letters = list('BCDFGHJKLMNPQRSTVWXYZ')
    plate = ''
    if country == 'CHE':
        canton = ['GE', 'VD', 'VS', 'FR', 'BE', 'BL', 'AI']
        plate = plate + ''.join(random.choices(canton, weights=[15,5,2,2,1,1,1], k=1))+ ''.join(random.sample(chiffres, k=6))
        while plate[2] == '0':
            plate = ''
            plate = plate + ''.join(random.choices(canton, weights=[15,5,2,2,1,1,1], k=1))+ ''.join(random.sample(chiffres, k=6))
        print(plate)
    elif country == 'FRA':
        plate = ''.join(random.sample(letters, k=2))+''.join(random.sample(chiffres, k=3))+''.join(random.sample(letters, k=2))
        while plate[2] == '0':
            plate = ''
            plate = ''.join(random.sample(letters, k=2))+''.join(random.sample(chiffres, k=3))+''.join(random.sample(letters, k=2))
        print(plate)
    else:
        plate = ''.join(random.sample(chiffres, k=4))+''.join(random.sample(letters, k=3))
        while plate[0] == '0':
            plate = ''
            plate = ''.join(random.sample(chiffres, k=4))+''.join(random.sample(letters, k=3))
        print(plate)
    return country, plate
listeFinale = []
def createVehicle(a):
    
    for i in range(a):
        vhc = vehicles
        
        genMrqMdl = chooseMarqueModel()
        genLicPla = createLicencePlate()
        vhc.id = i
        vhc.type = genMrqMdl[0]
        vhc.marque = genMrqMdl[1]
        vhc.model = genMrqMdl[2]
        vhc.country = genLicPla [0]
        vhc.plate = genLicPla[1]
        vhc.spec = 'indetermine'
        vhcItem = (vhc.id,vhc.type,vhc.marque,vhc.model,vhc.country,vhc.plate,vhc.spec)
        listeFinale.append(vhcItem)

createVehicle(200)

print(len(listeFinale))

car_header = ['id','type','marque', 'modele', 'pays', 'plaque','pattern']
with open('voitures.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(car_header)
    for i in range(len(listeFinale)):
        writer.writerow(listeFinale[i])
    csvfile.close()

'''

#GUI
schema = []
voitures = 0
livraisons = 0
autobus = 0
for i in range(len(listeFinale)):
    if listeFinale[i][1] == 'Voiture':
        voitures +=1
    if listeFinale[i][1] == 'Livraisons':
        livraisons +=1
    if listeFinale[i][1] == 'Autobus':
        autobus +=1
print(voitures)
print(livraisons)
print(autobus)

y = np.array([voitures, livraisons, autobus])
mylabels = ["voitures", "livraisons", "auotbus"]
plt.legend()

plt.pie(y, labels = mylabels)
plt.show()

plt.pie(y)
plt.show()
'''