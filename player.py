from collections import defaultdict
import bitarray


class Player:
    def __init__(self, player_id):
        self._id = player_id
        # {item_id: amount}
        self._items = {}
        self._money = 0

    def add_item(self, item_id, amount):
        # Return amount changed
        if amount > 0:
            self._items[item_id] = self._items.get(item_id, 0) + amount
            return self._items[item_id]
        else:
            self._items[item_id] = max(self._items.get(item_id, 0) + amount, 0)
            return self._items[item_id]

    def add_money(self, amount):
        self._money += amount

    def get_money(self):
        return self._money

    def get_item_amount(self, item_id):
        return self._items.get(item_id)

    def get_items_ids(self):
        return self._items.keys()


# Manager also store all extra information essential for our data
class PlayerManager:
    MAX_PLAYER_IDX = 1e5

    def __init__(self):
        # {player_id: Player}
        self.players = {}
        # NOTE: don't need currently, probably will be better delete in the future because of recalculation everything with heap i will 100% calculate this
        # {item_id: item_amount}
        # self.items_amount = defaultdict(int)
        # {item_id: set(player_id)}
        self.item_players_stash = defaultdict(set)

    def get_player(self, player_id):
        return self.players.get(player_id)

    def add_player_item(self, player_id, item_id, amount):
        if self.players.get(player_id) is None:
            self.players[player_id] = Player(player_id)
        added_amount = self.players[player_id].add_item(item_id, amount)
        # self.items_amount[item_id] += added_amount
        if self.players[item_id].get_item_amount(item_id) == 0:
            self.item_players_stash[item_id].discard(player_id)

    def add_player_money(self, player_id, amount):
        if self.players.get(player_id) is None:
            self.players[player_id] = Player(player_id)
        self.players[player_id].add_money(amount)
