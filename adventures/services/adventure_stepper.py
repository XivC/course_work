import datetime
import random
from dataclasses import dataclass
from functools import cached_property
from typing import Callable

from django.db.models import Q
from django.db.transaction import atomic
from rest_framework.exceptions import ValidationError

from adventures.models import Adventure, AdventurePlanet, Teammate
from affects.models import CreatureEffectRule, PlanetEffectRule
from battles.models import Battle, BattleMember, BattlerEffect, BattleReport
from battles.services import BattlersBulkCreator
from course_work.services import ServiceBase
from course_work.storage import FunctionCaller
from creatures.models import Creature
from planets.models import Planet


@dataclass
class AdventureStepper(ServiceBase):
    adventure: Adventure

    @atomic
    def action(self) -> Battle:
        self.start_adventure()
        self.visit_planet()
        if self.report.allies_power < self.report.opponents_power:
            self.adventure.is_successful = False
            self.adventure.save()
        elif not AdventurePlanet.objects.filter(adventure=self.adventure, is_visited=False).exists():
            self.adventure.is_successful = True
            self.adventure.finished_at = datetime.datetime.utcnow()
            self.adventure.save()

        return self.battle

    def start_adventure(self):
        if not self.adventure.started_at:
            self.adventure.started_at = datetime.datetime.utcnow()
            self.adventure.save()

    def visit_planet(self):
        self.adventure_planet.is_visited = True
        self.adventure_planet.save()

    @cached_property
    def report(self) -> BattleReport:
        members = BattleMember.objects.filter(battle=self.battle).select_related('battler__creature', 'battler__weapon')
        allies = members.filter(is_opponent=False)
        enemies = members.filter(is_opponent=True)

        allies_power = self.calculate_total_power(allies)
        enemies_power = self.calculate_total_power(enemies)
        return BattleReport.objects.create(
            allies_power=allies_power,
            opponents_power=enemies_power,
            battle=self.battle,
        )

    def calculate_total_power(self, battle_members: list[BattleMember]) -> int:
        battlers = {bm.battler_id for bm in battle_members}
        applied_effects = [beff for beff in self.battlers_effects if beff in battle_members]
        self_power = sum([member.battler.creature.power for member in battle_members])
        weapons_power = sum([member.battler.weapon for member in battle_members if member.battler.weapon])
        effects_power = sum([aef.effect.power_affect for aef in applied_effects])

        return self_power + weapons_power + effects_power

    @cached_property
    def battlers_effects(self) -> list[BattlerEffect]:
        return self.fill_planets_based_effect_rules() + self.fill_creatures_based_effects()

    def fill_planets_based_effect_rules(self) -> list[BattlerEffect]:
        appliable_planet_effect_rules = PlanetEffectRule.objects.filter(planet=self.planet, creature_to_id__in=self.battle_creatures_ids).select_related('effect')
        battler_effects = []

        planet_battlers = {member.battler.creature_id: member.battler_id for member in self.battle_members}

        for rule in appliable_planet_effect_rules:
            battler_effects.append(
                BattlerEffect(
                    battle=self.battle,
                    effect=rule.effect,
                    battler_id=planet_battlers[rule.creature_to_id]
                )
            )

        BattlerEffect.objects.bulk_create(battler_effects)
        return battler_effects

    def fill_creatures_based_effects(self) -> list[BattlerEffect]:
        appliable_creature_effect_rules = CreatureEffectRule.objects.filter(
            Q(creature_to_id__in=self.battle_creatures_ids) | Q(creature_to_id__in=self.battle_creatures_ids)
        ).select_related('effect')
        battler_effects = []

        allies = {member.battler.creature_id: member.battler_id for member in self.battle_members if
                  not member.is_opponent}
        enemies = {member.battler.creature_id: member.battler_id for member in self.battle_members if
                   member.is_opponent}

        for rule in appliable_creature_effect_rules:
            battler_effect = BattlerEffect(
                battle=self.battle,
                effect=rule.effect,
            )
            should_be_added = False

            groups = [(allies, allies), (enemies, enemies)] if rule.is_to_ally else [(allies, enemies),
                                                                                     (enemies, allies)]
            for group_from, group_to in groups:
                if rule.creature_from_id in group_from and rule.creature_to_id in group_to:
                    battler_effect.battler_id = group_to[rule.creature_to_id]
                    should_be_added = True
                    break

            if should_be_added:
                battler_effects.append(battler_effect)

        BattlerEffect.objects.bulk_create(battler_effects)
        return battler_effects


    @cached_property
    def battle_creatures_ids(self) -> list[int]:
        return [member.battler.creature_id for member in self.battle_members]

    @cached_property
    def battle_members(self):
        creatures_on_planet = Creature.objects.filter(planet=self.planet).exclude(
            id__in=Teammate.objects.filter(team=self.adventure.team).select_related('battler').values_list('battler__creature_id', flat=True)
        ).order_by('?')
        battlers = BattlersBulkCreator(adventure=self.adventure, creatures=creatures_on_planet, weapons = [])()
        battlers += [mate.battler for mate in self.adventure.team.teammates.select_related('battler')]

        battle_members = []
        for battler in battlers:
            member = BattleMember(
                battle=self.battle,
                battler=battler,
                is_opponent=(random.random() > 0.5),
            )

        BattleMember.objects.bulk_create(battle_members)
        return battle_members

    @cached_property
    def adventure_planet(self) -> AdventurePlanet | None:
        adventure_planet = AdventurePlanet.objects.filter(
            is_visited=False, adventure=self.adventure,
        ).select_related('planet').order_by('?').first()
        return adventure_planet

    @cached_property
    def planet(self) -> Planet | None:
        if not self.adventure_planet:
            return None

        return self.adventure_planet.planet

    @cached_property
    def battle(self) -> Battle:
        return Battle.objects.create(
            adventure=self.adventure,
            planet=self.planet,
        )

    def validate_adventure_not_finished(self):
        if self.adventure.finished_at:
            raise ValidationError('Adventure already finished')

    def validate_planet_exists(self):
        if not self.planet:
            raise ValidationError('No unvisited planets in adventure')

    def get_validators(self) -> list[Callable]:
        return [
            self.validate_planet_exists,
            self.validate_adventure_not_finished,
        ]