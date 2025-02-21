"""
URL configuration for lliga project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from futbol import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('classificacio/',views.classificacio),
    path("",views.index,name="index"),
    path("menu", views.menu, name="menu"),
    path('nou_jugador', views.nou_jugador, name='nou_jugador'),
    path("classificacio/<int:lliga_id>", views.classificacio, name="classificacio"),
    path('goals_ranked/', views.goalsranked, name='goals_ranked'),  # Sin ID usa la primera liga
    path('goals_ranked/<int:lliga_id>/', views.goalsranked, name='goals_ranked'), 
    path('taula_partits/<int:lliga_id>/', views.taula_partits, name='taula_partits'),]
