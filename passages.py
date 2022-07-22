import datetime
import calendar
import random
import csv
import os


#importation fichier patterns
os.chdir('.\Documents\projetsProg')
f = open('patterns.csv', 'r')
spamreader = csv.reader(f, delimiter=',', quotechar='|')

afv = {'601': {'cam' : ['Anière', 'Renfile']}, '602' : {'cam' : ['Pierre à Bochet', 'Thônex']}, '603' : {'cam' : ['Veyrier', 'Troinex']}, '605' : {'cam' : ['Bardonnex', 'Perly']}, '606' : {'cam' : ['Meyrin', 'Dardagny']}, '607':{'cam' : ['Ferney', 'Vireloup']}, '555' : {'cam': ['Saint Prex']}}

passages = []

jours = calendar.monthrange(2023,1)
print(jours[1])

jj = 1
hh = 13
mm = 0
ss = 0

temps = datetime.datetime(2022,9,jj,hh,mm,ss)
print(temps)

temps = temps - datetime.timedelta(hours=12)
print(temps)

'''temps = datetime.date(2022,9,1) - datetime.date(2022,11,1)
print(temps)'''

dict_vhc = {}
vehicles = []
listeFinale =[]


#tri des véhicules par typse et nationalités
for row in spamreader:
        vehicles.append(row)

def build_liste_finale():
        
        for i in range(len(vehicles)) :
                
                dict_vhc['id'] = vehicles[i][0]
                dict_vhc['type'] = vehicles[i][1]
                dict_vhc['marque'] = vehicles[i][2]
                dict_vhc['modèle'] = vehicles[i][3]
                dict_vhc['plaque'] = vehicles[i][5]
                dict_vhc['passage'] = []
                vehicles[i] = list(dict_vhc)
                #dict_vhc.clear()
                
                
build_liste_finale()

        

print('yo',vehicles)
print('sum',vehicles[2]) 
print('biched',dict_vhc)
        
print('popopo',listeFinale)
'''
dict_vhc['id'] = vehicles[0][0]
dict_vhc['type'] = vehicles[0][1]
dict_vhc['marque'] = vehicles[0][2]
dict_vhc['modèle'] = vehicles[0][3]
dict_vhc['plaque'] = vehicles[0][5]
dict_vhc['passage'] = []

dict_vhc['passage'].append(['600',temps])
dict_vhc['passage'].append(['6023',temps])
#print(vehicles[0])
#print(dict_vhc)
vehicles[0] = dict_vhc
print(len(vehicles[0]['passage']))
print(vehicles[1])
'''