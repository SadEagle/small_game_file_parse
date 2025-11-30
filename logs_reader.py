from abc import ABCMeta, abstractmethod
import re


class FileReader:
    __metaclass__ = ABCMeta

    def __init__(self, file_path):
        self.file_path = file_path

    def __iter__(self):
        with open(self.file_path, "r") as file:
            for line in file:
                yield self._parse_data(line)

    @abstractmethod
    def _parse_data(self, data_line):
        pass


class InventoryReader(FileReader):
    def _parse_data(self, data_line):  # type: ignore
        inventory_data_re = r"\[(?P<timestamp>\d+)\] (?P<action_type>\w+) \| (?P<player_id>\d+), \((?P<items_data>(\d+, )+\d+)\)"
        inventory_data_match = re.match(inventory_data_re, data_line)
        if inventory_data_match is None:
            raise ValueError("Can't parse file")

        # Parse items_data
        items_data = inventory_data_match.group("items_data").split(", ")
        # (item_type, amount)
        if len(items_data) % 2 != 0:
            raise ValueError("Odd items data len, expected even")

        items_type = items_data[::2]
        items_amount = items_data[1::2]
        # Converation str to int
        if inventory_data_match.group("action_type") == "ITEM_ADD":
            items_amount = tuple(map(int, items_amount))
        elif inventory_data_match.group("action_type") == "ITEM_REMOVE":
            items_amount = tuple(map(lambda x: -int(x), items_amount))
        else:
            raise ValueError("undefined action type")

        items_data = tuple(
            (item_type, item_amount)
            for item_type, item_amount in zip(items_type, items_amount)
        )

        inventory_dict = inventory_data_match.groupdict()
        # Replace items_data with parsed one
        inventory_dict["items_data"] = items_data
        # Full data string
        inventory_dict["data_line"] = data_line
        return inventory_dict


class MoneyReader(FileReader):
    def _parse_data(self, data_line):  # type: ignore
        money_data_re = r"\[(?P<timestamp>\d+)\] (?P<player_id>\w+) \| \((?P<action_type>\w+), (?P<amount>\d+), (?P<reason>\w+))"
        money_data_match = re.match(money_data_re, data_line)
        if money_data_match is None:
            raise ValueError("Can't parse file")
        money_data = money_data_match.groupdict()

        # Convertation str to int
        if money_data.get("action_type") == "MONEY_ADD":
            money_data["amount"] = int(money_data["amount"])
        elif money_data.get("action_type") == "MONEY_REMOVE":
            money_data["amount"] = -int(money_data["amount"])
        else:
            raise ValueError("undefined action type")
        money_data["data_line"] = data_line
        return money_data


# TODO: Realize line by line reader
class AllLogsReader:
    DATE_MAX = "31.12.999 23:59:59"

    def __init__(self, *readers):
        self._readers = readers

    @staticmethod
    def _get_next(iter):
        try:
            return next(iter)
        except StopIteration:
            return None

    # @classmethod
    # def _get_timestamp(cls, val):
    #     if val is None:
    #         return cls.DATE_MAX
    #     else:
    #         return val["timestamp"]

    def __iter__(self):
        # Add only log files with at least one readable log line
        reader_iter_list = []
        cur_val_list = []
        for reader in self._readers:
            cur_iter = iter(reader)
            cur_val = AllLogsReader._get_next(cur_iter)
            if cur_val is not None:
                # Exist at least one readable line in the file
                reader_iter_list.append(cur_iter)
                cur_val_list.append(cur_val)

        if len(reader_iter_list) == 0:
            raise ValueError(
                "Get 0 logs lines, files are unreadable or there is not reader files"
            )

        while True:
            next_timestamp_idx = cur_val_list.index(
                # min(cur_val_list, key=lambda x: AllLogsReader._get_timestamp(x))
                min(cur_val_list, key=lambda x: x["timestamp"])
            )
            next_value = AllLogsReader._get_next(reader_iter_list[next_timestamp_idx])
            if next_value is None:
                if len(reader_iter_list) == 1:
                    # Get out of last iterator
                    break
                # Get end of the iterator
                if next_timestamp_idx == len(reader_iter_list) - 1:
                    reader_iter_list = reader_iter_list[:next_timestamp_idx]
                else:
                    reader_iter_list = (
                        reader_iter_list[:next_timestamp_idx]
                        + reader_iter_list[next_timestamp_idx + 1 :]
                    )
            yield next_value
