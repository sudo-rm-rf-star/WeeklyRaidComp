from logic.raid_composition.AQRaidCompositionEvaluator import AQRaidCompositionEvaluator
from logic.raid_composition.BWLRaidCompositionEvaluator import BWLRaidCompositionEvaluator
from logic.raid_composition.RaidCompositionEvaluator import RaidCompositionEvaluator
from logic.enums.RosterStatus import RosterStatus
from logic.enums.SignupStatus import SignupStatus
from typing import List, Optional
from random import sample
from logic.Character import Character
from datetime import datetime

MAX_EVALUATION_TIME_SECS = 2
HILL_CLIMB_ITERATIONS = 250
EVALUATORS = {
    "bwl": BWLRaidCompositionEvaluator,
    "aq": AQRaidCompositionEvaluator
}


class CompositionOptimizer:
    def __init__(self, raid_name: str, characters: List[Character]):
        self.raid_name = raid_name
        self.characters = characters
        self.evaluator = EVALUATORS.get(raid_name, lambda characters: RaidCompositionEvaluator(raid_name, characters))
        self.fitness_cache = {}  # This function is hard to compute

        # By sorting by role and then class we effectively make all neighbors in the next array by switching a
        # neighboring zero and one
        self.population = sorted([character for character in characters if (character.signup_status != SignupStatus.DECLINE and character.roster_status != RosterStatus.DECLINE)],
                                 key=lambda char: (char.role.name, char.klass.name))
        self.population_size = len(self.population)

    def make_raid_composition(self) -> List[Character]:
        accepted_characters = self.candidate_to_characters(self.random_restart_hill_climbing())
        updated_characters = []
        print(len(accepted_characters))
        for character in self.characters:
            if character in accepted_characters:
                roster_status = RosterStatus.ACCEPT
            elif character.signup_status != SignupStatus.DECLINE and character.roster_status != RosterStatus.DECLINE:
                roster_status = RosterStatus.EXTRA
            else:
                roster_status = RosterStatus.DECLINE
            if roster_status != character.roster_status:
                character.roster_status = roster_status
                updated_characters.append(character)
        return updated_characters

    def hill_climbing(self) -> int:
        """ https://en.wikipedia.org/wiki/Hill_climbing """
        start_time = datetime.now()
        stoppingCondition = lambda: (datetime.now() - start_time).seconds > MAX_EVALUATION_TIME_SECS

        currentNode = self.choose_initial_candidate()
        while not stoppingCondition():
            neighbourhood = self.get_neighbors(currentNode)
            nextNode = None
            for x in neighbourhood:
                if self.fitness(x) > self.fitness(nextNode):
                    nextNode = x
            if self.fitness(nextNode) <= self.fitness(currentNode):
                break
            currentNode = nextNode
        return currentNode

    def random_restart_hill_climbing(self) -> int:
        currentNode = None
        iteration = 0

        while iteration < HILL_CLIMB_ITERATIONS:
            nextNode = self.hill_climbing()
            if self.fitness(nextNode) > self.fitness(currentNode):
                currentNode = nextNode
            iteration += 1
        print(f"Achieved a fitness of {self.fitness(currentNode)}")
        return currentNode

    def fitness(self, candidate: Optional[int]) -> float:
        if candidate is None:
            return float("-inf")
        if candidate not in self.fitness_cache:
            self.fitness_cache[candidate] = self.evaluator(self.candidate_to_characters(candidate)).score()
        return self.fitness_cache[candidate]

    def choose_initial_candidate(self):
        """ Candidates are presented as bit vector where 1 indicates an accepted player and 0 declined. """
        candidate = 0
        subset = sample(range(self.population_size), 40) if len(self.population) > 40 else range(len(self.population))
        for i in subset:
            candidate |= 1 << i
        return candidate

    def get_neighbors(self, candidate: int) -> List[int]:
        neighbours = []
        for i in range(self.population_size - 1):
            if (candidate >> i & 1) != (candidate >> (i + 1) & 1):
                neighbour = candidate
                neighbour ^= 1 << i
                neighbour ^= 1 << (i + 1)
                neighbours.append(neighbour)
        return neighbours

    def candidate_to_characters(self, candidate: int) -> List[Character]:
        characters = []
        index = len(self.population) - 1
        while candidate:
            if candidate & 1:
                characters.append(self.population[index])
            index -= 1
            candidate >>= 1
        return characters
