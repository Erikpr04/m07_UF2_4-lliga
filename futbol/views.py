from django.shortcuts import render
from futbol.models import *

def classificacio(request):
    lliga = Lliga.objects.all()[1]
    equips = lliga.equips.all()
    classi = []
 
    # calculem punts en llista de tuples (equip,punts)
    for equip in equips:
        punts = 0
        victorias = 0
        derrotas = 0
        empates = 0
        goles_metidos = 0
        goles_recibidos = 0
        for partit in lliga.partits.filter(equip_local=equip):
            goles_metidos += partit.gols_local()
            goles_recibidos += partit.gols_visitant()
            if partit.gols_local() > partit.gols_visitant():
                victorias+=1
                punts += 3
            elif partit.gols_local() == partit.gols_visitant():
                punts += 1
        for partit in lliga.partits.filter(equip_visitant=equip):
            goles_metidos += partit.gols_visitant()
            goles_recibidos += partit.gols_local()
            if partit.gols_local() < partit.gols_visitant():
                derrotas+=1
                punts += 3
            elif partit.gols_local() == partit.gols_visitant():
                empates+=1
                punts += 1
        classi.append( {"punts":punts,"nom":equip.nom ,"victorias":victorias,"derrotas":derrotas,"empates":empates,"gols_metidos":goles_metidos,"gols_rebuts":goles_recibidos,"ga":round(goles_metidos-goles_recibidos,2)} )
    # ordenem llista
    classi.sort(reverse=True,key=lambda x: x["punts"])
    return render(request,"classificacio.html",
                {
                    "classificacio":classi,
                    "lliga":lliga,
                })
