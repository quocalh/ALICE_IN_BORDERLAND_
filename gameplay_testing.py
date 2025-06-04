from random import randint
import time

from components.settings import *


class Player:
    def __init__(self, is_bot: bool = True):
        self.number: int = -1
        self.vitality: int = 0
        self.is_bot = is_bot

    def ChosingNumber(self, overwrited_is_bot: bool = None, overwrite_number: int = None):
        if overwrited_is_bot != None:
            if overwrited_is_bot == True:
                self.number = overwrite_number if overwrite_number else randint(0, 100)
                print(f"The bot has made its choice. ({self.number})")
            elif overwrited_is_bot == False:
                self.number = int(input("Give me a number:             "))
        else: 
            if self.is_bot == True:
                self.number = overwrite_number if overwrite_number != None else randint(0, 100)
                print(f"The bot has made its choice. ({self.number})")
            else:
                self.number = int(input("Give me a number:             "))

class PlayerManager:
    def __init__(self, PlayerPool: list[Player] = []):
        self.player_pool: list[Player] = PlayerPool
        self.ultimate_number: float = -1
        
        "GAME LOGIC FLAGS"
        self.game_phase: int = 5 
    
    def PlayerPool_ChosingNumber(self, debug_mode: bool = False):
        if debug_mode:
            self.player_pool[0].ChosingNumber()
            try:
                self.player_pool[1].ChosingNumber(overwrite_number = 0)
            except: 
                pass
            try:
                self.player_pool[2].ChosingNumber(overwrite_number = 24)
            except: 
                pass
            try:
                self.player_pool[3].ChosingNumber(overwrite_number = 100)
            except: 
                pass
            try:
                self.player_pool[4].ChosingNumber(overwrite_number = 24)
            except: 
                pass
        else:
            for player in self.player_pool:
                player.ChosingNumber()


    
    def Gameloop(self) -> None:
        """
        FIND PLAYERS WHOSE NUMBERS ARE CLOSEST TO THE ULTIMATE NUMBER
        NOTE:
            keep in mind the rule:
                4th rule means 4 remaining player
                3rd rule means 3 remaining player
                2nd rule means 2 remaining player
        """
        if self.game_phase == 1:
            raise Exception("congrats")
        
        print(f"currently in phase {self.game_phase}")

        """finding ultimate number"""
        ultimate_number = 0
        delta_numbers_dict: dict[int, list[Player]] = {}
        for player in self.player_pool: 
            ultimate_number += player.number

        ultimate_number = ultimate_number / len(self.player_pool) * 0.8
        ultimate_number = int(ultimate_number)

        """counter is used to store players with delta numbers"""
        for player in self.player_pool:
            """important 1D vector"""
            delta_number = player.number - ultimate_number
            if delta_number in delta_numbers_dict:
                delta_numbers_dict[delta_number].append(player)
            else:
                delta_numbers_dict[delta_number] = [player]


        """for players who fall into the 4th rule"""
        if self.game_phase <= 4:
            for delta_number in list(delta_numbers_dict.keys()):
                bucket = delta_numbers_dict[delta_number]
                if len(bucket) != 1:
                    """if there are more than 1 player chose the same number
                       they will be counted as the losers, proceeding to delete them from the contestants list."""
                    del delta_numbers_dict[delta_number]

        """for players who activate the 3rd rule"""
        PunishemntCoefficient: int = 1
        if self.game_phase <= 3:
            if 0 in delta_numbers_dict:
                print()
                print("[GAME]: Damn! someone just activated the 3rd rule, damage casted this round will be doubled (x2).")
                print()
                PunishemntCoefficient: int = PunishemntCoefficient * 2

        """the 2nd rule """
        if self.game_phase <= 2:
            if - ultimate_number in delta_numbers_dict:
                # print("0 detected")
                if (100 - ultimate_number) in delta_numbers_dict:
                    # print(f"100 detected")
                    print()
                    print("[GAME]: Someone just activated the 2nd rule, people who chose 0 will automatically lose if there are players chose 100.")
                    print()
                    del delta_numbers_dict[100 - ultimate_number]


        print(f"\t\tultimate number: {ultimate_number}")

        the_closest_abs_delta_number: int = abs(min(delta_numbers_dict.keys(), key = lambda key: abs(key)))
        the_winning_list: list[Player] = []

        """listing winning players"""
        for delta_number in delta_numbers_dict:
            if abs(delta_number) == the_closest_abs_delta_number:
                the_winning_list = the_winning_list + delta_numbers_dict[delta_number]
                print(f"\t\t\t=> the_closest_number: {delta_number + ultimate_number}")

        """reducing the players' points"""
        for player in self.player_pool:
            if player not in the_winning_list:
                player.vitality -= 1 * PunishemntCoefficient
            
            
        for player in self.player_pool:
            print(f"The player's vitality: {player.vitality}")
            

        """eliminating players"""
        length = len(self.player_pool)
        for i in range(length):
            i = (length - 1) - i
            if self.player_pool[i].vitality <= - GAMEPLAY_MAX_LIFE:
                print("One player has been eliminated")
                del self.player_pool[i]
                
        self.game_phase = self.EleminatingPlayers()


    def ResetPlayerNumber(self):
        for player in self.player_pool:
            player.number = -1
        
    def ReducingPlayerPointExcept(self, the_winner_list: list[Player]):
        for player in self.player_pool:
            if not player in the_winner_list:
                player.vitality -= 1
            print(f"Player vitality: {player.vitality}")
    
    def EleminatingPlayers(self):
        "useless now"
        length_player_pool: int = len(self.player_pool)
        for i in range(len(self.player_pool)):
            i = (length_player_pool - 1) - i
            player = self.player_pool[i]
            if player.vitality <= - GAMEPLAY_MAX_LIFE:
                print("One player has been eliminated!")
                del self.player_pool[i]
        return len(self.player_pool)


Human = Player(False)
Bot1 = Player()
Bot2 = Player()
Bot3 = Player()
Bot4 = Player()

player_manager = PlayerManager([Human, Bot1, Bot2, Bot3, Bot4])

while True:
    print("\n\n=======================================")
    print("Get number phase...")
    player_manager.PlayerPool_ChosingNumber()
    
    print("\nChecking Phase...")

    the_winner_list = player_manager.Gameloop()
    
    




