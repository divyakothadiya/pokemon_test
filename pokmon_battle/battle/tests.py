from django.test import TestCase
from battle.models import Pokemon
from battle.views import calculate_winner
from django.core.management import call_command
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
import os

class PokemonModelTest(TestCase):

    def setUp(self):
        self.bulbasaur = Pokemon.objects.create(name="Bulbasaur", hp=45, attack=49, defense=49)
        self.charmander = Pokemon.objects.create(name="Charmander", hp=39, attack=52, defense=43)

    def test_pokemon_creation(self):
        self.assertEqual(self.bulbasaur.hp, 45)
        self.assertEqual(self.charmander.attack, 52)

    def test_pokemon_str(self):
        self.assertEqual(str(self.bulbasaur), "Bulbasaur")

class BattleLogicTest(TestCase):

    def setUp(self):
        self.bulbasaur = Pokemon.objects.create(name="Bulbasaur", hp=45, attack=49, defense=49)
        self.charmander = Pokemon.objects.create(name="Charmander", hp=39, attack=52, defense=43)

    def test_calculate_winner(self):
        winner = calculate_winner(self.bulbasaur, self.charmander)
        self.assertEqual(winner, self.bulbasaur)

        self.charmander.attack = 70
        self.charmander.save()
        winner = calculate_winner(self.bulbasaur, self.charmander)
        self.assertEqual(winner, self.charmander)

class LoadPokemonCommandTest(TestCase):

    def test_load_pokemon_data(self):
        csv_file_path = os.path.join(os.path.dirname(__file__), '../data/pokemon.csv')
        call_command('load_pokemon')
        self.assertTrue(Pokemon.objects.exists())

        bulbasaur = Pokemon.objects.get(name="Bulbasaur")
        self.assertEqual(bulbasaur.hp, 45)
        self.assertEqual(bulbasaur.attack, 49)

class PokemonAPITest(APITestCase):

    def setUp(self):
        self.url = reverse('pokemon-list')
        Pokemon.objects.create(name="Bulbasaur", hp=45, attack=49, defense=49)

    def test_get_pokemon_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Bulbasaur")

    def test_create_pokemon(self):
        data = {
            "name": "Squirtle",
            "hp": 44,
            "attack": 48,
            "defense": 65
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Pokemon.objects.count(), 2)
        self.assertEqual(Pokemon.objects.get(name="Squirtle").hp, 44)

class BattleAPITest(APITestCase):

    def setUp(self):
        self.pokemon1 = Pokemon.objects.create(name="Bulbasaur", hp=45, attack=49, defense=49)
        self.pokemon2 = Pokemon.objects.create(name="Charmander", hp=39, attack=52, defense=43)
        self.url = reverse('battle')

    def test_battle_endpoint(self):
        data = {
            "pokemon1_id": self.pokemon1.id,
            "pokemon2_id": self.pokemon2.id
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('winner', response.data)
        self.assertEqual(response.data['winner'], self.pokemon1.name)

    def test_battle_endpoint_invalid_pokemon(self):
        data = {
            "pokemon1_id": self.pokemon1.id,
            "pokemon2_id": 999
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
