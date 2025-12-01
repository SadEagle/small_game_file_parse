import xml.etree.ElementTree as ET


class Item:
    def __init__(self, item_id, item_name=None, price=None):
        self.id = id
        self.name = item_name
        self.price = price
        self.first_appearence = None
        self.last_appearence = None
        self.appearence_count = 0

    def add_timestamp(self, timestamp):
        if self.first_appearence is None:
            self.first_appearence = timestamp
        self.last_appearence = timestamp
        self.appearence_count += 1


class ItemManager:
    def __init__(self, item_data_path=None):
        self._items = {}

        if item_data_path is not None:
            with open(item_data_path) as f:
                xml_string = f.read()
            root = ET.fromstring(xml_string)
            for item in root.findall("item"):
                item_dict = {}
                for child in item:
                    item_dict[child.tag] = child.text
                self._items[item_dict["item_type_id"]] = Item(
                    item_dict["item_type_id"],
                    item_dict["item_name"],
                    item_dict["price"],
                )

    def add_item_timestamp(self, item_id, timestamp):
        if self._items.get(item_id) is None:
            self._items[item_id] = Item(item_id)
        self._items[item_id].add_timestamp(timestamp)

    def get_item_ids(self):
        return tuple(self._items.keys())

    def get_item(self, item_id):
        return self._items[item_id]
