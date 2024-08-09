from battle.models import Pokemon

def calculate_damage(pokemon_a, pokemon_b):
    damage_a_to_b = (pokemon_a.attack / 200) * 100 - (
        ((pokemon_b.against_grass / 4) * 100) + ((pokemon_b.against_poison / 4) * 100)
    )
    damage_b_to_a = (pokemon_b.attack / 200) * 100 - (
        ((pokemon_a.against_grass / 4) * 100) + ((pokemon_a.against_poison / 4) * 100)
    )
    return damage_a_to_b, damage_b_to_a

def battle(pokemon_name_a, pokemon_name_b):
    pokemon_a = Pokemon.objects.filter(name__iexact=pokemon_name_a).first()
    pokemon_b = Pokemon.objects.filter(name__iexact=pokemon_name_b).first()
    
    damage_a_to_b, damage_b_to_a = calculate_damage(pokemon_a, pokemon_b)
    
    if damage_a_to_b > damage_b_to_a:
        return {"winnerName": pokemon_a.name, "wonByMargin": damage_a_to_b - damage_b_to_a}
    elif damage_b_to_a > damage_a_to_b:
        return {"winnerName": pokemon_b.name, "wonByMargin": damage_b_to_a - damage_a_to_b}
    else:
        return {"winnerName": "Draw", "wonByMargin": 0}
