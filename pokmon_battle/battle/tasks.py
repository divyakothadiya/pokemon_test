# battle/tasks.py
from celery import shared_task
from battle.models import Battle
from battle.utils import battle

@shared_task
def start_battle_task(battle_id):
    battle_instance = Battle.objects.get(battle_id=battle_id)
    result = battle(battle_instance.pokemon_a.name, battle_instance.pokemon_b.name)
    battle_instance.result = result
    battle_instance.status = "BATTLE_COMPLETED"
    battle_instance.save()
