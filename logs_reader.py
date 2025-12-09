from abc import ABCMeta, abstractmethod
import re


class LogFileReader:
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


class InventoryReader(LogFileReader):
    # Task file parse structure (somehow different)
    inventory_data_re_compile = re.compile(
        r"\[(?P<timestamp>\d+)\] (?P<player_id>\d+) \| (?P<action_type>\w+), \((?P<items_data>(\d+, )+\d+)\)"
    )
    # Current file parse
    inventory_data_re_example_compile = re.compile(
        r"\[(?P<timestamp>\d+)\] (?P<action_type>\w+) \| (?P<player_id>\d+), \((?P<items_data>(\d+, )+\d+)\)"
    )

    def __init__(self, file_path):
        # Example file and thechnical task has 2 different file versions
        super(InventoryReader, self).__init__(file_path)

    def _parse_data(self, data_line):  # type: ignore
        inventory_data_match = InventoryReader.inventory_data_re_compile.match(
            data_line
        )
        if inventory_data_match is None:
            inventory_data_match = (
                InventoryReader.inventory_data_re_example_compile.match(data_line)
            )
        if inventory_data_match is None:
            raise ValueError("Can't parse InventoryReader in file: " + self.file_path)

        # Parse items_data
        items_data = inventory_data_match.group("items_data").split(", ")
        # (item_type, amount)
        if len(items_data) % 2 != 0:
            raise ValueError("Odd items data len, expected even")

        # Split data by logical sight
        item_type_list = items_data[::2]
        item_amount_list = items_data[1::2]
        # Converation str to int
        item_amount_list = tuple(map(int, item_amount_list))

        if inventory_data_match.group("action_type") == "ITEM_ADD":
            item_sign = 1
        elif inventory_data_match.group("action_type") == "ITEM_REMOVE":
            item_sign = -1
        else:
            raise ValueError(
                "Unexpected action_type in InventoryReader: "
                + inventory_data_match.group("action_type")
            )
        items_data = tuple(
            (item_type, item_sign * item_amount)
            for item_type, item_amount in zip(item_type_list, item_amount_list)
        )

        return {
            "timestamp": int(inventory_data_match.group("timestamp")),
            "action_type": inventory_data_match.group("action_type"),
            "player_id": inventory_data_match.group("player_id"),
            "items_data": items_data,
            "data_line": data_line,
        }


class MoneyReader(LogFileReader):
    money_data_re_compile = re.compile(
        r"(?P<timestamp>\d+)\|(?P<player_id>\d+)\|(?P<action_type>\w+),(?P<money_amount>\d+),(?P<reason>\w+)"
    )

    def __init__(self, file_path):
        super(MoneyReader, self).__init__(file_path)

    def _parse_data(self, data_line):  # type: ignore
        money_data_match = MoneyReader.money_data_re_compile.match(data_line)
        if money_data_match is None:
            raise ValueError("Can't parse MoneyReader file: " + self.file_path)
        # money_data = money_data_match.groupdict()

        # Convertation str to int
        if money_data_match.group("action_type") == "MONEY_ADD":
            money_sign = 1
        elif money_data_match.group("action_type") == "MONEY_REMOVE":
            money_sign = -1
        else:
            raise ValueError(
                "Unexpected action_type in MoneyReader: "
                + money_data_match.group("action_type")
            )
        money_amount = money_sign * int(money_data_match.group("money_amount"))
        return {
            "timestamp": int(money_data_match.group("timestamp")),
            "player_id": money_data_match.group("player_id"),
            "action_type": money_data_match.group("action_type"),
            "money_amount": money_amount,
            "reason": money_data_match.group("reason"),
        }


class AllLogsReader:
    def __init__(self, *readers):
        self._readers = readers

    @staticmethod
    def _get_next(iter):
        try:
            return next(iter)
        except StopIteration:
            return None

    def __iter__(self):
        # Add only log files with at least one readable log line
        reader_iters = []
        cur_entries = []
        for reader in self._readers:
            cur_iter = iter(reader)
            cur_val = AllLogsReader._get_next(cur_iter)
            if cur_val is not None:
                # Exist at least one readable line in the file
                reader_iters.append(cur_iter)
                cur_entries.append(cur_val)

        if len(reader_iters) == 0:
            return

        while True:
            next_timestamp_idx = cur_entries.index(
                min(cur_entries, key=lambda x: x["timestamp"])
            )
            cur_value = cur_entries[next_timestamp_idx]
            next_value = AllLogsReader._get_next(reader_iters[next_timestamp_idx])
            if next_value is None:
                if len(reader_iters) == 1:
                    # Last value of the last iterator
                    yield cur_value
                    break

                # Delete next_timestamp_idx id from list
                reader_iters = (
                    reader_iters[:next_timestamp_idx]
                    + reader_iters[next_timestamp_idx + 1 :]
                )
                cur_entries = (
                    cur_entries[:next_timestamp_idx]
                    + cur_entries[next_timestamp_idx + 1 :]
                )
            else:
                cur_entries[next_timestamp_idx] = next_value
            yield cur_value
