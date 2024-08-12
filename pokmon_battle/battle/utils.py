from battle.models import Pokemon
from difflib import get_close_matches

def calculate_damage(pokemon_a, pokemon_b):
    # Calculate the damage from Pokemon A to Pokemon B
    damage_a_to_b = (pokemon_a.attack / 200) * 100 - (
        ((pokemon_b.against_grass if pokemon_b.type1 == 'Grass' else 0) / 4) * 100 +
        ((pokemon_b.against_poison if pokemon_b.type1 == 'Poison' else 0) / 4) * 100
    )
    
    # Calculate the damage from Pokemon B to Pokemon A
    damage_b_to_a = (pokemon_b.attack / 200) * 100 - (
        ((pokemon_a.against_grass if pokemon_a.type1 == 'Grass' else 0) / 4) * 100 +
        ((pokemon_a.against_poison if pokemon_a.type1 == 'Poison' else 0) / 4) * 100
    )
    
    return damage_a_to_b, damage_b_to_a


def battle(pokemon_name_a, pokemon_name_b):
    pokemon_a = Pokemon.objects.filter(name__iexact=pokemon_name_a).first()
    pokemon_b = Pokemon.objects.filter(name__iexact=pokemon_name_b).first()
    
    if not pokemon_a or not pokemon_b:
        return {"winnerName": "Error", "wonByMargin": 0}

    damage_a_to_b, damage_b_to_a = calculate_damage(pokemon_a, pokemon_b)
    
    if damage_a_to_b > damage_b_to_a:
        return {"winnerName": pokemon_a.name, "wonByMargin": damage_a_to_b - damage_b_to_a}
    elif damage_b_to_a > damage_a_to_b:
        return {"winnerName": pokemon_b.name, "wonByMargin": damage_b_to_a - damage_a_to_b}
    else:
        return {"winnerName": "Draw", "wonByMargin": 0}

def get_valid_pokemon_names():
    return [pokemon.name.lower() for pokemon in Pokemon.objects.all()]

def normalize_and_validate_pokemon_names(pokemon_name1, pokemon_name2):
    valid_pokemon_names = get_valid_pokemon_names()

    # Normalize input
    normalized_name1 = pokemon_name1.lower()
    normalized_name2 = pokemon_name2.lower()

    # Function to check if a name has one or more spelling mistakes
    def check_spelling(name, valid_names):
        matches = get_close_matches(name, valid_names, n=1, cutoff=0.8)
        if matches:
            # If the closest match is similar enough, consider it correct
            return matches[0]
        return None

    # Validate both names
    corrected_pokemon_a = check_spelling(normalized_name1, valid_pokemon_names)
    corrected_pokemon_b = check_spelling(normalized_name2, valid_pokemon_names)

    if corrected_pokemon_a and corrected_pokemon_b:
        return corrected_pokemon_a, corrected_pokemon_b
    else:
        # Handle the case of spelling mistakes
        errors = []
        if not corrected_pokemon_a:
            errors.append(f"{pokemon_name1} is not a valid Pokemon name.")
        if not corrected_pokemon_b:
            errors.append(f"{pokemon_name2} is not a valid Pokemon name.")
        raise ValueError(" ".join(errors))