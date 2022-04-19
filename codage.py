#!/usr/bin/env python
# coding: utf-8

#Lien afin de telechager le dossier de la carte.
#https://drive.google.com/drive/folders/1nXoQlZihtNS06FkbbwcBDsFP4JAQkba7?usp=sharing


#27 villes principales
#3 zones de difficulté
#zone 1 (jaune): -15% des troupes ennemies
#zone 2 (orange): -25% des troupes ennemies
#zone 3 (rouge): -50% des troupes ennemies
#La guerre est gagnee si la capitale tombe et si l'ennemi a encore des soldats dans son armee
#On supose que l'ennemi est la Russie donc il doit envahir par l'est (sans passer par la Bielorussie)
#Le but étant d'arriver à Kyiv donc de se diriger vers l'ouest. Par conséquent toute les villes à l'est de la progression Russe ne font plus partie des options des villes à envahir.
#Il entre dans une ville de facon aleatoire
#Il peut rentrer seulement dans les villes qui lui sont adjacentes
#Temps de siege zone 1 = 10 jours
#Temps de siege zone 2 = 25 jours 
#Temps de siege zone 3 = 50 jours



import random
import numpy as np
import pandas as pd
import shapefile as shp
import matplotlib.pyplot as plt 
import seaborn as sns
import glob
import os
import csv
from PIL import Image


sns.set(style="whitegrid",palette='bright',color_codes=True) 
sns.mpl.rc("figure", figsize=(10,6))
shp_path="/Users/adam/Downloads/UKR_adm1/UKR_adm1.shp"
sf=shp.Reader(shp_path)
len(sf.shapes())
sf.records()

#Elle va lire le fichier shapefile de la carte de l’Ukraine et le transformer en tableau.
def read_shapefile(sf):
    fields = [x[0] for x in sf.fields][1:]
    records = [list(i) for i in sf.records()]
    shps = [s.points for s in sf.shapes()]
    df = pd.DataFrame(columns=fields, data=records)
    df = df.assign(coords=shps)
    return df

df=read_shapefile(sf)

#Elle va venir afficher la carte et colorier les différentes zones passées en paramètre avec le paramètre ‘city’.
def plot_map_fill_multiples_ids(title, city, sf,progression,day,x_lim = None,y_lim = None, figsize = (9,7)):
  
    
    plt.figure(figsize = figsize)
    fig, ax = plt.subplots(figsize = figsize)
    ax.axis('off')
    fig.suptitle(title, fontsize=16)
    for shape in sf.shapeRecords():
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        ax.plot(x, y, 'k')
            
    for i in range(len(city)):
        shape_ex = sf.shape(city[i])
        x_lon = np.zeros((len(shape_ex.points),1))
        y_lat = np.zeros((len(shape_ex.points),1))
        for ip in range(len(shape_ex.points)):
            x_lon[ip] = shape_ex.points[ip][0]
            y_lat[ip] = shape_ex.points[ip][1]
        
        if title=='VICTOIRE RUSSIE':
            if i in {24,18,26,11,10,1,20,7,14}:
                ax.fill(x_lon,y_lat, 'w')
            elif i in {13,21,9,23,0,17,4,5,12}:
                ax.fill(x_lon,y_lat,'b')
            else:
                ax.fill(x_lon,y_lat,'r')
                
        elif title=='VICTOIRE UKRAINE':
            if i in {22,6,2,23,0,12,4,5,25,3,19,8,15,16}:
                ax.fill(x_lon,y_lat, 'y')
            else:
                ax.fill(x_lon,y_lat,'b')
            
        elif progression[i]<0.5 :
            ax.fill(x_lon,y_lat, 'y')
        
        elif progression[i]==1:
            ax.fill(x_lon,y_lat, 'r')
        
        elif 1>progression[i]>=0.5:
            ax.fill(x_lon,y_lat, 'tab:orange')
             
        x0 = np.mean(x_lon)
        y0 = np.mean(y_lat)
        plt.text(x0, y0, df.NAME_1[city[i]], fontsize=10)
    
    if (x_lim != None) & (y_lim != None):     
        plt.xlim(x_lim)
        plt.ylim(y_lim)
    
    #dossier dans lequel les cartes vont être enregistrées.A modifier avant utilisation. Mettre un chemin correcte.
    fig.savefig('/Users/adam/Desktop/Invasion_cartes/'+'Jour '+str(day)+'.png')
    plt.close('all')
    
    return None
    

#---------------------------------PARTIE CODE------------------------------------------------------------------------------------------------------------------------
indices_map={"Cherkasy":0,"Chernihiv":1,"Chernivtsi":2,"Crimea":3,"Dnipropetrovs'k":4,"Donets'k":5,"Ivano-Frankisv'k":6,
        "Kharkiv":7,"Kherson":8,"Khmel'nyts'kyy":9,"Kiev City":10,"Kiev":11,"Kirovohrad":12,
                "L'viv":13,"Luhans'k":14,"Mykolayiv":15,"Odessa":16,"Poltava":17,"Rivne":18,"Sevastopol'":19,
                "Sumy":20,"Ternopil'":21,"Transcarpathia":22,"Vinnytsya":23,"Volyn":24,"Zaporizhzhya":25,
                "Zhytomyr":26}

cities ={"Cherkasy":0,"Chernihiv":1,"Chernivtsi":2,"Crimea":3,"Dnipropetrovs'k":4,"Donets'k":5,"Ivano-Frankisv'k":6,
        "Kharkiv":7,"Kherson":8,"Khmel'nyts'kyy":9,"Kiev":10,"Kirovohrad":11,
        "L'viv":12,"Luhans'k":13,"Mykolayiv":14,"Odessa":15,"Poltava":16,"Rivne":17,"Sevastopol'":18,
        "Sumy":19,"Ternopil'":20,"Transcarpathia":21,"Vinnytsya":22,"Volyn":23,"Zaporizhzhya":24,
        "Zhytomyr":25,"Kiev City":26}

options=[['Kiev','Vinnytsya'],['Kiev'],["Ternopil'","Khmel'nyts'kyy",'Vinnytsya']
         ,['Kherson'],['Poltava','Kirovohrad','Mykolayiv'],["Dnipropetrovs'k",'Zaporizhzhya'],['Chernivtsi',"Ternopil'"]
         ,['Poltava',"Dnipropetrovs'k"],["Dnipropetrovs'k",'Mykolayiv'],['Vinnytsya','Zhytomyr'],['Kiev City'],['Cherkasy','Poltava','Vinnytsya']
         ,['Rivne',"Ternopil'"],["Donets'k"],['Odessa','Kirovohrad'],['Vinnytsya','Kirovohrad'],['Chernihiv','Kiev','Cherkasy']
         ,['Zhytomyr',"Khmel'nyts'kyy"],['Crimea'],["Chernihiv","Poltava"],["Rivne","Khmel'nyts'kyy"],["L'viv","Ivano-Frankisv'k"]
         ,['Kiev','Zhytomyr'],['Rivne'],["Dnipropetrovs'k","Kherson"],['Kiev']]

zone1 = {"Luhans'k",'Sumy','Kharkiv',"Donets'k",'Zaporizhzhya','Crimea',"Sevastopol'",'Kherson','Mykolayiv','Odessa','Chernivtsi'
         ,"Ivano-Frankisv'k",'Transcarpathia','Volyn',"L'viv"}
zone2 = {"Dnipropetrovs'k",'Poltava','Kirovohrad','Vinnytsya',"Ternopil'","Khmel'nyts'kyy",'Rivne','Cherkasy'}
zone3 = {'Kiev','Kiev City','Chernihiv','Zhytomir'}


#Elle vient faire la simulation du jeu en suivant les regles enoncees precedemment pour un nombre de jours passé en parametre (jour[0]).
#Elle vient aussi afficher les cartes pour chaque jour en faisant appel à la fonction plot_map_fill_multiples_ids.
def choose_city(soldats,jours):
    K=random.random()
    L=random.random()
    S=random.random()
    days=[]
    villes=[]
    pourcentages=[]
    ville=''
    inv_dico=dict()
    envahit=[]
    j=0
    d=1
    while j<jours[0] and soldats[len(soldats)-1]>0 and ville!='Kiev City':
        p=1
        if inv_dico==dict():
            lim=10
            m=0
            i=0
            for i in [K,L,S]:
                if i >= m:
                    m=i
            
            
            if m==K:
                ville='Kharkiv'

            elif m==L:
                ville="Luhans'k"

            elif m==S:
                ville='Sumy'

            soldats.append(soldats[len(soldats)-1]-int((15/100)*soldats[len(soldats)-1]))
            jours.append(jours[len(jours)-1]-lim)
            
            
        else:
            if ville!='Kiev City':
                r=int(random.random()*len(options[cities[ville]]))            
                ville=options[cities[ville]][r]
                

                if ville in zone1 :
                    lim=10
                    soldats.append(soldats[len(soldats)-1]-int((15/100)*soldats[len(soldats)-1]))
                    jours.append(jours[len(jours)-1]-lim)
                    
                    
                elif ville in zone2 :
                    lim=25
                    soldats.append(soldats[len(soldats)-1]-int((25/100)*soldats[len(soldats)-1]))
                    jours.append(jours[len(jours)-1]-lim)
                    
                elif ville in zone3 :
                    lim=50
                    soldats.append(soldats[len(soldats)-1]-int((50/100)*soldats[len(soldats)-1]))
                    jours.append(jours[len(jours)-1]-lim)
                    
        while p<=lim and j!=jours[0]:
            inv_dico[ville]=p/lim
            envahit.append([(v,inv_dico[v]) for v in inv_dico])
            p+=1
            j+=1
        
    
        
    for l in envahit:
        for (c,a) in l:
            days.append(d)
            villes.append(c)
            pourcentages.append(a)
            
        d+=1
    
    tab=[]
    for (d,c,a) in zip(days,villes,pourcentages):
        tab.append([d,c,a])
    
    towns={t for t in villes}
    
    for x in cities:
        if x not in towns:
            tab.append([0,x,0])
        
        
        
    titles=['Jours', 'Villes', 'Progression']
    
    with open('invasion_sumup','w') as f:
        write=csv.writer(f)
        write.writerow(titles)
        write.writerows(tab)
    
    data=pd.read_csv('invasion_sumup')
    
    for jour in range(1,j+1):
        w=data[data['Jours']==jour]
        cuidades=w['Villes']
        ids=[indices_map[z] for z in cuidades]
        progress=[e for e in w['Progression']]
        plot_map_fill_multiples_ids('Jour '+str(jour), ids,sf,progress,jour,x_lim = None,y_lim = None, figsize = (9,7))
    
    if villes[len(villes)-1]=='Kiev City' and pourcentages[len(pourcentages)-1]==1:
        plot_map_fill_multiples_ids('VICTOIRE RUSSIE',[indices_map[c] for c in indices_map],sf,[],j+1,x_lim = None,y_lim = None, figsize = (9,7))
            
    else:
        plot_map_fill_multiples_ids('VICTOIRE UKRAINE',[indices_map[c] for c in indices_map],sf,[],j+1,x_lim = None,y_lim = None, figsize = (9,7))

            
    frames = []
    imgs=[]
    for y in range(1,j+2):
        #dossier dans lequel les cartes vont être enregistrées.A modifier avant utilisation. Mettre un chemin correcte.
        path="/Users/adam/Desktop/Invasion_cartes/Jour "+str(y)+".png" #où sont stockées les images
        imgs.append(path)
    for i in imgs:
        new_frame = Image.open(i)
        frames.append(new_frame)
    
    #dossier dans lequel les cartes vont être enregistrées.A modifier avant utilisation. Mettre un chemin correcte.
    frames[0].save('/Users/adam/Desktop/Invasion_cartes/Invasion_'+str(soldats[0])+'_'+str(jours[0])+'.gif', format='GIF', #où sont stockées les images
                   append_images=frames[1:],
                   save_all=True,
                   duration=325,optimize=False, loop=1)
    
    
    for t in range(1,j+2):
            #dossier dans lequel les cartes vont être enregistrées.A modifier avant utilisation. Mettre un chemin correcte.
            os.remove("/Users/adam/Desktop/Invasion_cartes/Jour "+str(t)+".png") #où sont stockées les images
    
    return None





