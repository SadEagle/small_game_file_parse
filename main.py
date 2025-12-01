import heapq
from collections import defaultdict

from items import ItemManager
from player import PlayerManager
from logs_reader import AllLogsReader, InventoryReader, MoneyReader

from analytics import (
    get_first_n_items,
    get_last_n_items,
    get_top_n_log_mention_items,
    get_top_n_player_by_money,
)


def make_file_analytics(items_manager, player_manager):
    # Get analytics
    top_10_mention_times = get_top_n_log_mention_items(item_manager)
    top_10_rich_players = get_top_n_player_by_money(player_manager)
    first_10_items_met = get_first_n_items(item_manager)
    last_10_items_met = get_last_n_items(item_manager)
    with open("./output.txt", "w") as f:
        f.write("Top 10 mention itmes:\n")
        for count, item_id in top_10_mention_times:
            f.write(item_id + ", " + str(count) + "\n")
        f.write("\nTop 10 richest players:\n")
        for _, player_id in top_10_rich_players:
            cur_player = player_manager.get_player(player_id)
            if cur_player is None:
                raise ValueError("Unexpected player")
            f.write(
                cur_player.id
                + ", "
                + str(cur_player.money)
                + ", "
                + cur_player.first_appearence
                + ", "
                + cur_player.last_appearence
                + "\n"
            )

        f.write("\nFirst 10 items:\n")
        for first_item_timestamp, item_id in first_10_items_met:
            f.write(item_id + ", " + first_item_timestamp + "\n")
        f.write("\nLast 10 Items:\n")
        # Need reverse top n last because of order
        for last_item_timestamp, item_id in first_10_items_met[::-1]:
            f.write(item_id + ", " + last_item_timestamp + "\n")


def interactive_answers(player_manager):
    # {item_id: set(player_id)}
    item_relation_map = defaultdict(set)

    for player_id in player_manager.get_player_ids():
        player_items = player_manager.get_player(player_id).get_items_ids()

        for item_id in player_items:
            item_relation_map[item_id].add(player_id)

    while True:
        item_id = input()
        current_item_players = item_relation_map.get(item_id)
        if current_item_players is None:
            print("Unknown item, please try another one")
            continue

        total_amount = 0
        heap_item_player_amount = []

        for player_id in current_item_players:
            cur_player_amount = player_manager.get_player(player_id).get_item_amount(
                item_id
            )
            total_amount += cur_player_amount
            heap_item_player_amount.append((cur_player_amount, player_id))

        top_10_item_players = heapq.nlargest(10, heap_item_player_amount)

        print()
        print("Item_id: " + item_id)
        print("Item amount: " + str(total_amount))
        print("Top players:")
        for item_amount, player_id in top_10_item_players:
            print(player_id + ", " + str(item_amount))


if __name__ == "__main__":
    inventory_reader = InventoryReader("./inventory_logs.txt")
    money_reader = MoneyReader("./money_logs.txt")
    all_logs_reader = AllLogsReader(inventory_reader, money_reader)

    # print(next(iter(money_reader)))
    # TODO: add file writer
    player_manager = PlayerManager()
    item_manager = ItemManager()

    # Logs processing
    for data_log in all_logs_reader:
        if data_log["action_type"] in ("MONEY_ADD", "MONEY_REMOVE"):
            player_manager.add_player_money(
                data_log["player_id"], data_log["money_amount"], data_log["timestamp"]
            )
        elif data_log["action_type"] in ("ITEM_ADD", "ITEM_REMOVE"):
            for item_id, item_amount in data_log["items_data"]:
                player_manager.add_player_item(
                    data_log["player_id"], item_id, item_amount, data_log["timestamp"]
                )
                item_manager.add_item_timestamp(item_id, data_log["timestamp"])
        else:
            raise ValueError("Unknown action type")

    make_file_analytics(item_manager, player_manager)

    interactive_answers(player_manager)
