import json


class Player:
    def __init__(self, player_id, name=None, level=None):
        self.id = player_id
        # {item_id: amount}
        self.name = name
        self.level = level
        self.items = {}
        self.money = 0
        self.first_appearence = None
        self.last_appearence = None

    def add_item(self, item_id, amount, timestamp):
        if self.first_appearence is None:
            self.first_appearence = timestamp
        self._last_appearence = timestamp
        # Return amount changed
        if amount > 0:
            self.items[item_id] = self.items.get(item_id, 0) + amount
            return self.items[item_id]
        else:
            self.items[item_id] = max(self.items.get(item_id, 0) + amount, 0)
            return self.items[item_id]

    def add_money(self, amount, timestamp):
        self.money += amount
        if self.first_appearence is None:
            self.first_appearence = timestamp
        self.last_appearence = timestamp

    def get_item_amount(self, item_id):
        return self.items.get(item_id, 0)

    def get_items_ids(self):
        return self.items.keys()


# Manager also store all extra information essential for our data
class PlayerManager:
    def __init__(self, player_data_path=None):
        # {player_id: Player}
        self._players = {}
        if player_data_path is not None:
            with open(player_data_path) as f:
                player_data_dict = json.load(f)
            for player in player_data_dict["players"]:
                player["id"] = str(player["id"])
                self._players[player["id"]] = Player(
                    player["id"], player["name"], str(player["level"])
                )

    def get_player(self, player_id):
        return self._players.get(player_id)

    def get_player_ids(self):
        return tuple(self._players.keys())

    def add_player_item(self, player_id, item_id, amount, timestamp):
        if self._players.get(player_id) is None:
            self._players[player_id] = Player(player_id)
        self._players[player_id].add_item(item_id, amount, timestamp)
        # added_amount = self.players[player_id].add_item(item_id, amount)
        # self.items_amount[item_id] += added_amount
        # if self.players[item_id].get_item_amount(item_id) == 0:
        #     self.item_players_stash[item_id].discard(player_id)

    def add_player_money(self, player_id, amount, timestamp):
        if self._players.get(player_id) is None:
            self._players[player_id] = Player(player_id)
        self._players[player_id].add_money(amount, timestamp)
