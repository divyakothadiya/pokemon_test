from django.urls import path
from .views import PokemonListView, BattleAPIView, BattleStatusAPIView

urlpatterns = [
    path('pokemon', PokemonListView.as_view(), name='pokemon-list'),
    path('battle', BattleAPIView.as_view(), name='battle-start'),
    path('battle/<uuid:battle_id>/', BattleStatusAPIView.as_view(), name='battle-status'),
]
