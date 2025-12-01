class Item:
    def __init__(self, item_id):
        self._id = id
        self._first_appearence = None
        self._last_appearence = None
        self._appearence_count = 0

    def add_timestamp(self, timestamp):
        if self._first_appearence is None:
            self._first_appearence = timestamp
        self._last_appearence = timestamp
        self._appearence_count += 1

    @property
    def id(self):
        return self._id

    @property
    def first_appearence(self):
        return self._first_appearence

    @property
    def last_appearence(self):
        return self._last_appearence

    @property
    def appearence_count(self):
        return self._appearence_count


class ItemManager:
    def __init__(self):
        self._items = {}

    def add_item_timestamp(self, item_id, timestamp):
        if self._items.get(item_id) is None:
            self._items[item_id] = Item(item_id)
        self._items[item_id].add_timestamp(timestamp)

    def get_item_ids(self):
        return tuple(self._items.keys())

    def get_item(self, item_id):
        return self._items[item_id]
