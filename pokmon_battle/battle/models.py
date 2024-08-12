from django.db import models
import uuid

class Pokemon(models.Model):
    name = models.CharField(max_length=100)
    type1 = models.CharField(max_length=50)
    type2 = models.CharField(max_length=50, null=True, blank=True)
    total = models.IntegerField(null=True, blank=True)
    hp = models.IntegerField(null=True, blank=True)
    attack = models.IntegerField()
    defense = models.IntegerField(null=True, blank=True)
    sp_attack = models.IntegerField(null=True, blank=True)
    sp_defense = models.IntegerField(null=True, blank=True)
    against_grass = models.FloatField(default=1.0)
    against_poison = models.FloatField(default=1.0)

    def __str__(self):
        return self.name

class Battle(models.Model):
    battle_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pokemon_a = models.ForeignKey(Pokemon, related_name='battles_as_a', on_delete=models.CASCADE)
    pokemon_b = models.ForeignKey(Pokemon, related_name='battles_as_b', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='BATTLE_INPROGRESS')
    result = models.JSONField(null=True, blank=True)
