import heapq


def get_first_n_items(data_manager, n=10):
    heap_first_met = (
        (item.first_appearence, item_id)
        for item_id, item in data_manager.items.items()
        if item.first_appearence is not None
    )
    return heapq.nsmallest(n, heap_first_met)


def get_last_n_items(data_manager, n=10):
    heap_last_met = (
        (item.last_appearence, item_id)
        for item_id, item in data_manager.items.items()
        if item.last_appearence is not None
    )
    return heapq.nlargest(n, heap_last_met)


def get_top_n_log_mention_items(data_manager, n=10):
    heap_popularity_items = (
        (item.appearence_count, item_id) for item_id, item in data_manager.items.items()
    )
    return heapq.nlargest(n, heap_popularity_items)


def get_top_n_player_by_money(data_manager, n=10):
    heap_money_players = (
        (player.money_amount, player_id)
        for player_id, player in data_manager.players.items()
    )
    return heapq.nlargest(n, heap_money_players)
