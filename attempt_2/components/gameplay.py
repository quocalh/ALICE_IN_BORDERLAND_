import numpy as np
import numba as nb
from numba import jit, njit
# will try to implement numba

from components.settings import  *

class Player:
    id_counter: int = 0
    def __init__(self):
        self.vitality: int = 0
        self.number: int = -1
        self.name: str = "player" + str(self.id_counter)

        self.id_counter += 1 

class KingofDiamonds:
    def __init__(self, players_bool: list[Player]):
        self.players_pool: list[Player] = players_bool

        # REFRESHED EVERY ROUND
        self.ultimate_number: int = -1
        self.winners_list: list[Player] = []

    def GetPlayerRemaining(self):
        return len(self.players_pool)
    
    def Gameloop(self):
        # check for -1
        for i, player in enumerate(self.players_pool):
            assert player.number != -1, f"some of the players have not fill up their numbers (ID-index: {i})"

        player_remaining = self.GetPlayerRemaining()

        print(f"currently: {player_remaining} player remaining...")

        if player_remaining == 1:
            print(self.players_pool[0].name, "claims the victory!")
            raise Exception("good one")

        ultimate_number = sum([player.number for player in self.players_pool]) / len(self.players_pool) * 0.8 
        ultimate_number = int(ultimate_number)
        self.ultimate_number = ultimate_number

        # each one of the key is a 1D vector
        # scale from itself to the ultimate number (player_number - ult_number)
        delta_number_dict: dict = {}
        abs_delta_number_dict: dict = {}
        for player in self.players_pool:
            delta_number = player.number - ultimate_number
            if delta_number not in delta_number_dict:
                delta_number_dict[delta_number] = [player]
                abs_delta_number_dict[abs(delta_number)] = [player]
            else:
                delta_number_dict[delta_number].append(player)
                abs_delta_number_dict[abs(delta_number)].append(player)


        if player_remaining <= 4:
            # if only four players remaining
            # new rule will be added: whoever choose the same number with the others 
            #   will be counted as a lost
            # -> disqualifing them from the dict, standing no chance to win the in the current round
            for delta_number in delta_number_dict:
                bucket = delta_number_dict[delta_number]
                if len(bucket) > 1:
                    del delta_number_dict[delta_number]

        punishment_coef: int = 1
        if player_remaining <= 3:
            # 3 players remaining, until now, whenever a person chose exactly the ultimate number
            # the losers will lost 2 points in the current round rather than 1 point like the previous one
            if 0 in delta_number_dict:
                punishment_coef = 2

        if player_remaining <= 2:
            # 2 players remaning, in this case, the game is entirely analougos to rock, paper, scissors
            # the player who chose 100 will win against who chose 0
            if - ultimate_number in delta_number_dict:
                if 100 - ultimate_number in delta_number_dict:
                    del delta_number_dict[- ultimate_number]
        
        # NOTE: supposed that 50 is the ult number then 65 and 45 hold the same potential to win 
        the_closest_abs_delta_number: int = min(list(abs_delta_number_dict.keys()))

        # (keep in mind that the game can have multiple winners in 1 round)
        the_winning_players: list[Player] = abs_delta_number_dict[the_closest_abs_delta_number]
        self.winners_list = the_winning_players

        
        for player in self.players_pool:
            if player not in the_winning_players:
                player.vitality -= punishment_coef * 1

        for i in range(len(self.players_pool)):
            i = (len((self.players_pool)) - 1) - i
            if self.players_pool[i].vitality <= GAMEPLAY_MINIMUM_VITALITY:
                del self.players_pool[i]
        

        # to improve the function reliability, we fill the players_pool's players with -1
        # and will raise an error if a player.number with -1 has been spotted