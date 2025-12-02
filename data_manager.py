import json
import xml.etree.ElementTree as ET
from collections import defaultdict


class Player:
    def __init__(self, player_id, name=None, level=None):
        self.player_id = player_id
        self.name = name
        self.level = level
        self.money_amount = 0
        self.first_appearence = None
        self.last_appearence = None


class Item:
    def __init__(self, item_id, item_name=None, price=None):
        self.item_id = id
        self.name = item_name
        self.price = price
        self.first_appearence = None
        self.last_appearence = None
        self.appearence_count = 0


# Manager also store all extra information essential for our data
class DataManager:
    def __init__(self, player_json_db_path=None, item_xml_db_path=None):
        # {player_id: Player}
        self.players = {}
        # {item_id: Item}
        self.items = {}
        # {player_id: {item_id: amount}}
        self.per_player_items = defaultdict(dict)
        if player_json_db_path is not None:
            self._read_player_db_json(player_json_db_path)
        if item_xml_db_path is not None:
            self._read_item_db_json(item_xml_db_path)

    def _read_player_db_json(self, player_json_db_path):
        with open(player_json_db_path) as f:
            player_data_dict = json.load(f)
        for player in player_data_dict["players"]:
            player["id"] = str(player["id"])
            self.players[player["id"]] = Player(
                player["id"],
                player["name"],
                str(player["level"]),
            )

    def _read_item_db_json(self, item_xml_db_path):
        with open(item_xml_db_path) as f:
            xml_string = f.read()
            root = ET.fromstring(xml_string)
            for item in root.findall("item"):
                item_dict = {}
                for child in item:
                    item_dict[child.tag] = child.text
                self.items[item_dict["item_type_id"]] = Item(
                    item_dict["item_type_id"],
                    item_dict["item_name"],
                    item_dict["price"],
                )

    def add_item(self, player_id, item_id, item_amount, timestamp):
        if self.players[player_id] is None:
            # Object wasn't preloaded and firstly appeared inside logs
            self.players[player_id] = Player(player_id)
        if self.items[item_id] is None:
            # Item wasn't preloaded and firstly appeared inside logs
            self.items[item_id] = Item(item_id)
        cur_player = self.players[player_id]
        cur_item = self.items[item_id]

        if cur_item.first_appearence is None:
            cur_item.first_appearence = timestamp
        cur_item.last_appearence = timestamp
        if cur_player.first_appearence is None:
            cur_player.first_appearence = timestamp
        cur_player.last_appearence = timestamp

        # Item_amount > 0
        self.per_player_items[player_id][item_id] = max(
            self.per_player_items[player_id].get(item_id, 0) + item_amount, 0
        )
        self.items[item_id].appearence_count += 1

    def add_item_list(self, player_id, items_data, timestamp):
        """Logs data processing"""
        for item_id, item_amount in items_data:
            self.add_item(player_id, item_id, item_amount, timestamp)

    def add_money(self, player_id, money_amount, timestamp):
        if self.players[player_id] is None:
            # Object wasn't preloaded and firstly appeared inside logs
            self.players[player_id] = Player(player_id)

        cur_player = self.players[player_id]
        if cur_player.first_appearence is None:
            cur_player.first_appearence = timestamp
        cur_player.last_appearence = timestamp

        cur_player.money_amount += money_amount
