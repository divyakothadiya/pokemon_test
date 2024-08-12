from django.test import TestCase
from battle.models import Pokemon, Battle
from battle.utils import calculate_damage, battle
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from battle.tasks import start_battle_task
class PokemonModelTest(TestCase):

    def setUp(self):
        self.bulbasaur = Pokemon.objects.create(
            name="Bulbasaur", hp=45, attack=49, defense=49, 
            against_grass=1.0, against_poison=1.0
        )
        self.charmander = Pokemon.objects.create(
            name="Charmander", hp=39, attack=52, defense=43, 
            against_grass=1.0, against_poison=1.0
        )

    def test_pokemon_creation(self):
        self.assertEqual(self.bulbasaur.hp, 45)
        self.assertEqual(self.charmander.attack, 52)

    def test_pokemon_str(self):
        self.assertEqual(str(self.bulbasaur), "Bulbasaur")

class BattleUtilsTest(TestCase):

    def setUp(self):
        self.bulbasaur = Pokemon.objects.create(
            name="Bulbasaur", 
            attack=49, 
            defense=49, 
            against_grass=0.5, 
            against_poison=0.5
        )
        self.charmander = Pokemon.objects.create(
            name="Charmander", 
            attack=52, 
            defense=43, 
            against_grass=1.0, 
            against_poison=1.0
        )

    def test_calculate_damage(self):
        damage_a_to_b, damage_b_to_a = calculate_damage(self.bulbasaur, self.charmander)
        self.assertGreater(damage_b_to_a, damage_a_to_b)

    def test_battle_logic(self):
        result = battle(self.bulbasaur.name, self.charmander.name)
        self.assertEqual(result['winnerName'], self.charmander.name)

        self.bulbasaur.attack = 70
        self.bulbasaur.save()
        result = battle(self.bulbasaur.name, self.charmander.name)
        self.assertEqual(result['winnerName'], self.bulbasaur.name)

class PokemonAPITest(APITestCase):
    def setUp(self):
        self.url = reverse('battle-start')
        self.bulbasaur = Pokemon.objects.create(name="Bulbasaur", type1="Grass", type2="Poison", hp=45, attack=49, defense=49)
        self.charmander = Pokemon.objects.create(name="Charmander", type1="Fire", hp=39, attack=52, defense=43)

    def test_valid_pokemon_names(self):
        data = {
            "pokemon_a": "Bulbasaur",
            "pokemon_b": "Charmander"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['pokemon_a'], "bulbasaur")
        self.assertEqual(response.data['pokemon_b'], "charmander")

    def test_invalid_pokemon_names(self):
        data = {
            "pokemon_a": "Bulbasaur",
            "pokemon_b": "Char"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Char is not a valid Pokemon name", response.data['error'])

class BattleAPITest(APITestCase):

    def setUp(self):
        self.pokemon1 = Pokemon.objects.create(name="Bulbasaur", hp=45, attack=49, defense=49)
        self.pokemon2 = Pokemon.objects.create(name="Charmander", hp=39, attack=52, defense=43)
        self.url = reverse('battle-start')

    def test_battle_endpoint(self):
        data = {
            "pokemon_a": self.pokemon1.name,
            "pokemon_b": self.pokemon2.name
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('battle_id', response.data)
        self.assertTrue(Battle.objects.filter(battle_id=response.data['battle_id']).exists())

    def test_battle_status_endpoint(self):
        battle_instance = Battle.objects.create(pokemon_a=self.pokemon1, pokemon_b=self.pokemon2)
        url = reverse('battle-status', args=[battle_instance.battle_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'BATTLE_INPROGRESS')

class BattleTasksTest(TestCase):

    def setUp(self):
        self.bulbasaur = Pokemon.objects.create(name="Bulbasaur", hp=45, attack=49, defense=49)
        self.charmander = Pokemon.objects.create(name="Charmander", hp=39, attack=52, defense=43)
        self.battle = Battle.objects.create(pokemon_a=self.bulbasaur, pokemon_b=self.charmander)

    def test_start_battle_task(self):
        start_battle_task(self.battle.battle_id)
        self.battle.refresh_from_db()
        self.assertEqual(self.battle.status, "BATTLE_COMPLETED")
        self.assertIsNotNone(self.battle.result)
