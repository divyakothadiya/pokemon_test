from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from battle.models import Pokemon, Battle
from battle.utils import normalize_and_validate_pokemon_names
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
        if not pokemon_a or not pokemon_b:
            return Response({"error": "Both Pokemon names are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validated_pokemon_a,validated_pokemon_b=normalize_and_validate_pokemon_names(pokemon_a, pokemon_b)
            pokemon_a_obj = Pokemon.objects.filter(name=pokemon_a).first()
            pokemon_b_obj = Pokemon.objects.filter(name=pokemon_b).first()
            if not pokemon_a_obj or not pokemon_b_obj:
                raise ValueError(f"One or both Pokemon names are invalid: '{pokemon_a}' or '{pokemon_b}'")
           
            battle_instance = Battle.objects.create(
                pokemon_a=pokemon_a_obj,
                pokemon_b=pokemon_b_obj
            )
            start_battle_task(battle_instance.battle_id)
            return Response({
                    "message": "Battle started!",
                    "battle_id": str(battle_instance.battle_id),
                    "pokemon_a": validated_pokemon_a,
                    "pokemon_b": validated_pokemon_b
                }, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class BattleStatusAPIView(APIView):
    def get(self, request, battle_id):
        battle_instance = Battle.objects.get(battle_id=battle_id)
        return Response({"status": battle_instance.status, "result": battle_instance.result})
