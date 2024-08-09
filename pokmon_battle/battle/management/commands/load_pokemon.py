# battle/management/commands/load_pokemon.py
import os
from django.conf import settings
import pandas as pd
from django.core.management.base import BaseCommand
from battle.models import Pokemon

class Command(BaseCommand):
    help = 'Load Pokémon data from a CSV file'

    def handle(self, *args, **kwargs):
        csv_path = os.path.join(settings.BASE_DIR, 'data', 'pokemon.csv')
        df = pd.read_csv(csv_path)
        for _, row in df.iterrows():
            Pokemon.objects.create(
                # name=row['name'],
                # type1=row['type1'],
                # type2=row.get('type2', None),
                # #total=row['total'],
                # #hp=row['hp'],
                # attack=row['attack'],
                # #defense=row['defense'],
                # sp_attack=row['sp_attack'],
                # sp_defense=row['sp_defense'],
                # against_grass=row['against_grass'],
                # against_poison=row['against_poison'],
                name=row['name'],
                type1=row['type1'],
                type2=row.get('type2', None),
                attack=row['attack'],
                against_grass=row['against_grass'],
                against_poison=row['against_poison'],
            )
        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
