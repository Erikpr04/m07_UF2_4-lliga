from django.shortcuts import render
from futbol.models import *
from django.db.models import Count, Q


from django import forms
from django.shortcuts import redirect,get_object_or_404




def index(request):
    return render(request,"index.html")

def classificacio(request, lliga_id=None):
    # Obtener la liga seleccionada o usar la primera por defecto
    lliga = get_object_or_404(Lliga, id=lliga_id) if lliga_id else Lliga.objects.first()
    
    # Inicializar formulario con la liga actual
    form = MenuForm(initial={"lliga": lliga})

    equips = lliga.equips.all()
    classi = []

    for equip in equips:
        punts = 0
        victorias = 0
        derrotas = 0
        empates = 0
        goles_metidos = 0
        goles_recibidos = 0

        # Partidos jugados por el equipo (local o visitante)
        partits = Partit.objects.filter(Q(equip_local=equip) | Q(equip_visitant=equip), lliga=lliga)

        for partit in partits:
            es_local = partit.equip_local == equip  # Ver si el equipo jugó como local
            
            gols_fets = partit.gols_local() if es_local else partit.gols_visitant()
            gols_rebuts = partit.gols_visitant() if es_local else partit.gols_local()
            
            goles_metidos += gols_fets
            goles_recibidos += gols_rebuts

            if gols_fets > gols_rebuts:
                victorias += 1
                punts += 3
            elif gols_fets == gols_rebuts:
                empates += 1
                punts += 1
            else:
                derrotas += 1

        classi.append({
            "nom": equip.nom,
            "punts": punts,
            "victorias": victorias,
            "derrotas": derrotas,
            "empates": empates,
            "gols_metidos": goles_metidos,
            "gols_rebuts": goles_recibidos,
            "ga": round(goles_metidos - goles_recibidos, 2)  # Diferencia de goles
        })

    # Ordenar por puntos en orden descendente
    classi.sort(reverse=True, key=lambda x: x["punts"])

    return render(request, "classificacio.html", {
        "form": form,
        "classificacio": classi,
        "lliga": lliga,
    })

class MenuForm(forms.Form):
    lliga = forms.ModelChoiceField(
        queryset=Lliga.objects.all(), 
        empty_label="Selecciona una liga",  
        to_field_name="id",  
        widget=forms.Select(attrs={'class': 'form-control'}) ) 
 

class JugadorForm(forms.ModelForm):
    class Meta:
        model=Jugador
        fields="__all__"
 

def nou_jugador(request):  
    form = JugadorForm()

    if request.method == "POST":
        form = JugadorForm(request.POST)
        if form.is_valid():
            jugador = form.save(commit=False)  
            jugador.save()  

            return redirect('nou_jugador')  

    return render(request, "menu.html", {"form": form})  


def menu(request):
    form = MenuForm()
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            lliga = form.cleaned_data.get("lliga")
            # cridem a /classificacio/<lliga_id>
            return redirect('classificacio',lliga.id)
    return render(request, "menu.html",{
                    "form": form,
            })


def partits(request):

    lliga = Lliga.objects.all()[1]
    equips = lliga.equips.all()
    partits = []


    return render(request,"classificacio.html",
                {
                    "classificacio":classificacio,
                    "lliga":lliga,
                })


def goalsranked(request,lliga_id=None):


    if lliga_id:
        lliga = get_object_or_404(Lliga, id=lliga_id)  
    else:
        lliga = Lliga.objects.first()  
    equips = lliga.equips.all()

    
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            lliga = form.cleaned_data["lliga"]  
            return redirect('goals_ranked', lliga.id) 


    else:
        form = MenuForm(initial={'lliga': lliga})  

    goleadores = (
        Jugador.objects.filter(equip__in=equips)  # Filtramos por equipos de la liga
        .annotate(goles=Count('event', filter=Q(event__tipus_esdeveniment="gol")))  # Contamos los goles
        .order_by('-goles')  # Ordenamos de mayor a menor según goles
    )

    return render(request, "goalsranked.html", {
        "form": form,
        "goleadores": goleadores,
        "lliga": lliga,
    })



def taula_partits(request, lliga_id):
    lliga = Lliga.objects.get(id=lliga_id)
    equips = list(lliga.equips.all())  # Obtener todos los equipos de la liga

    # Crear la estructura de la tabla
    resultats = [[""] + [equip.nom for equip in equips]]  # Primera fila (encabezado)

    for equip1 in equips:
        fila = [equip1.nom]  # Primera columna (nombre del equipo)

        for equip2 in equips:
            if equip1 == equip2:
                fila.append("X")  # Si es el mismo equipo, ponemos una "X"
            else:
                # Buscar el partido entre equip1 y equip2
                partit = Partit.objects.filter(
                    lliga=lliga,
                    equip_local=equip1,
                    equip_visitant=equip2
                ).first()

                if partit:
                    resultat = f"{partit.gols_local()} - {partit.gols_visitant()}"
                else:
                    resultat = "-"

                fila.append(resultat)  # Añadir el resultado o un guion si no hay partido

        resultats.append(fila)  # Agregar la fila a la tabla

    return render(request, "taula_partits.html", {"resultats": resultats, "lliga": lliga})


