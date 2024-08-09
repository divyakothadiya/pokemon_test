from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from battle.models import Pokemon, Battle
from battle.utils import battle
from battle.tasks import start_battle_task
from rest_framework.pagination import PageNumberPagination

class PokemonListView(APIView):
    def get(self, request):
        pokemons = Pokemon.objects.all()
        paginator = PageNumberPagination()
        paginated_pokemons = paginator.paginate_queryset(pokemons, request)
        data = [{"name": p.name, "type1": p.type1, "type2": p.type2} for p in paginated_pokemons]
        return paginator.get_paginated_response(data)

class BattleAPIView(APIView):
    def post(self, request):
        pokemon_a = request.data.get("pokemon_a")
        pokemon_b = request.data.get("pokemon_b")
        pokemon_a_obj = Pokemon.objects.filter(name=pokemon_a).first()
        pokemon_b_obj = Pokemon.objects.filter(name=pokemon_b).first()
        battle_instance = Battle.objects.create(
            pokemon_a=pokemon_a_obj,
            pokemon_b=pokemon_b_obj
        )
        start_battle_task(battle_instance.battle_id)
        return Response({"battle_id":battle_instance.battle_id})

class BattleStatusAPIView(APIView):
    def get(self, request, battle_id):
        battle_instance = Battle.objects.get(battle_id=battle_id)
        return Response({"status": battle_instance.status, "result": battle_instance.result})
