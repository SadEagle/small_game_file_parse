class Player:
    def __init__(self, player_id):
        self._id = player_id
        # {item_id: amount}
        self._items = {}
        self._money = 0
        self._first_appearence = None
        self._last_appearence = None

    def add_item(self, item_id, amount, timestamp):
        if self._first_appearence is None:
            self._first_appearence = timestamp
        self._last_appearence = timestamp
        # Return amount changed
        if amount > 0:
            self._items[item_id] = self._items.get(item_id, 0) + amount
            return self._items[item_id]
        else:
            self._items[item_id] = max(self._items.get(item_id, 0) + amount, 0)
            return self._items[item_id]

    def add_money(self, amount, timestamp):
        self._money += amount
        if self._first_appearence is None:
            self._first_appearence = timestamp
        self._last_appearence = timestamp

    @property
    def id(self):
        return self._id

    @property
    def money(self):
        return self._money

    @property
    def first_appearence(self):
        return self._first_appearence

    @property
    def last_appearence(self):
        return self._last_appearence

    def get_item_amount(self, item_id):
        return self._items.get(item_id, 0)

    def get_items_ids(self):
        return self._items.keys()


# Manager also store all extra information essential for our data
class PlayerManager:
    def __init__(self):
        # {player_id: Player}
        self._players = {}

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
