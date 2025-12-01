import heapq


def get_first_n_items(item_manager, n=10):
    heap_first_met = (
        (item_manager.get_item(item_id).first_appearence, item_id)
        for item_id in item_manager.get_item_ids()
        if item_manager.get_item(item_id).first_appearence is not None
    )
    return heapq.nsmallest(n, heap_first_met)


def get_last_n_items(item_manager, n=10):
    heap_last_met = (
        (item_manager.get_item(item_id).last_appearence, item_id)
        for item_id in item_manager.get_item_ids()
        if item_manager.get_item(item_id).last_appearence is not None
    )
    return heapq.nlargest(n, heap_last_met)


def get_top_n_log_mention_items(item_manager, n=10):
    heap_popularity_items = (
        (item_manager.get_item(item_id).appearence_count, item_id)
        for item_id in item_manager.get_item_ids()
    )
    return heapq.nlargest(n, heap_popularity_items)


def get_top_n_player_by_money(player_manager, n=10):
    heap_money_players = (
        (player_manager.get_player(player_id).money, player_id)
        for player_id in player_manager.get_player_ids()
    )
    return heapq.nlargest(n, heap_money_players)
