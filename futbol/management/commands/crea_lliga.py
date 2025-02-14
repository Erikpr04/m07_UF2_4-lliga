from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from faker import Faker
from datetime import timedelta
from random import randint, random
import random

 
from futbol.models import *
 
faker = Faker(["es_CA","es_ES"])
 
class Command(BaseCommand):
    help = 'Crea una lliga amb equips i jugadors'
 
    def add_arguments(self, parser):
        parser.add_argument('titol_lliga', nargs=1, type=str)
 
    def handle(self, *args, **options):
        titol_lliga = options['titol_lliga'][0]
        lliga = Lliga.objects.filter(nom=titol_lliga)
        if lliga.count()>0:
            print("Aquesta lliga ja està creada. Posa un altre nom.")
            return
 
        print("Creem la nova lliga: {}".format(titol_lliga))
        lliga = Lliga( nom=titol_lliga )
        lliga.save()
 
        print("Creem equips")
        prefixos = ["RCD", "Athletic", "", "Deportivo", "Unión Deportiva","FC"]
        for i in range(20):
            ciutat = faker.city()
            prefix = prefixos[randint(0,len(prefixos)-1)]
            if prefix:
                prefix += " "
            nom =  prefix + ciutat
            any_fundacio=randint(1898,1999)
            equip = Equip(ciutat=ciutat,nom=nom,lliga=lliga,any_fundacio=any_fundacio)
            #print(equip)
            equip.save()
            lliga.equips.add(equip)
 
            print("Creem jugadors de l'equip "+nom)
            for j in range(25):
                nom = faker.name()
                posicio = "jugador"
                dorsal = randint(1,99)
                jugador = Jugador(nom=nom,posicio=posicio,equip=equip,dorsal=dorsal)
                #print(jugador)
                jugador.save()
 
        print("Creem partits de la lliga")
        for local in lliga.equips.all():
            for visitant in lliga.equips.all():
                if local != visitant:
                    partit = Partit(equip_local=local, equip_visitant=visitant, lliga=lliga)
                    partit.save()

                    for _ in range(randint(10, 20)): 
                        minut = randint(0, 99)
                        gol_marcado = randint(1, 3)
                        jugador = None

                        if gol_marcado == 1:
                            # Ha marcado equipo local
                            jugadores_locales = Jugador.objects.filter(equip=local)
                            if jugadores_locales.exists():
                                jugador = random.choice(jugadores_locales)
                        elif gol_marcado == 2:
                            # Ha marcado equipo visitante
                            jugadores_visitantes = Jugador.objects.filter(equip=visitant)
                            if jugadores_visitantes.exists():
                                jugador = random.choice(jugadores_visitantes)

                        if jugador:
                            event = Event(partit=partit, jugador=jugador, tipus_esdeveniment="gol", minut=minut)
                            event.save()