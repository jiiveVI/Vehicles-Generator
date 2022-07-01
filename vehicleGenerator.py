import random
import csv

Autobus = {'Iveco Bus':{'modèle':['Urbanway', 'Crealis', 'Crossway']}, 'man' :{'modèle': ['Lion\'s City', 'Lion\'s Classic', 'Lion\'s City Hybrid']}, 'Heuliez Bus' :{'modèle': ['GX 137', 'GX 337', 'GX Linium']}, 'Mercedes-Benz':{'modèle': ['Citaro C2', 'Citaro K', 'Citaro L']}}
Voiture = {'Bmw' : {'modèle':['X3','320','530','i8']}, 'Renault' : {'modèle':['Twingo','Clio','Scenic','Mégane']},'Toyota' : {'modèle':['Yaris','Celica','C-HR','Corolla']},'Peugeot' : {'modèle':['206','5008','3008','405']}, 'Mercedes-Benz' : {'modèle':['Classe A','Classe CLS','Classe SLK','Classe B']}, 'Audi' : {'modèle':['RS6','A8','Q5','e-tron']}}
Utilitaires = {'Renault' : {'modèle':['Trafic','Kangoo','Express']},'Citroën' : {'modèle':['Jumpy','Jumper','Berlingo']},'Volkswagen' : {'modèle':['Caddy','Crafter','Transporter',]}, 'Opel' : {'modèle':['Combo','Vivaro','Movano']}}

def createVehicle():
    car_type = random.choice([Autobus, Voiture, Utilitaires])
    marque = random.choice(list(car_type.keys()))
    modele = random.choice(car_type.get(marque).get('modèle'))
    return marque, modele

class vehicles():
    def __init__(self):
        self.objet = []
        #print(self.objet)
        #self.objet += [createVehicle() + createLicencePlate()]
        #print(self.objet)

def createLicencePlate():
    nationality = ['CHE', 'FRA', 'ESP']
    country = ''.join((random.choices(nationality, weights=[10,3,1], k=1)))
    #print(country)
    chiffres = list('0123456789')
    letters = list('BCDFGHJKLMNPQRSTVWXYZ')
    plate = ''
    if country == 'CHE':
        canton = ['GE', 'VD', 'VS', 'FR', 'BE', 'BL', 'AI']
        plate = plate + ''.join(random.choices(canton, weights=[15,5,2,2,1,1,1], k=1))+ ''.join(random.sample(chiffres, k=6))
        #print(plate)
    elif country == 'FRA':
        plate = ''.join(random.sample(letters, k=2))+''.join(random.sample(chiffres, k=3))+''.join(random.sample(letters, k=2))
        #print(plate)
    else:
        plate = ''.join(random.sample(chiffres, k=4))+''.join(random.sample(letters, k=3))
        #print(plate)
    return country, plate
        
def recursion(a):
    truc = vehicles()
    for i in range(a):
        truc.objet += [createVehicle() + createLicencePlate()]
    return truc

bibi = recursion(10)
print(bibi.objet[5][2])

with open('write.csv', 'x', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(bibi.objet[0])
    writer.writerow(bibi.objet[1])
    writer.writerow(bibi.objet[2])
    