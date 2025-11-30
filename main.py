from logs_reader import AllLogsReader, InventoryReader, MoneyReader


if __name__ == "__main__":
    # TODO: add line-by-line reader, store this data and PlayerManager

    # TODO: calcualte heap information pre-call or post call

    # TODO: Also add carret reading file for first 10 and last 10

    logs_reader = InventoryReader("./inventory_logs.txt")
    money_reader = MoneyReader("./money_logs.txt")
    all_logs_reader = AllLogsReader(logs_reader, money_reader)
    for data_log in all_logs_reader:
        print(data_log.get("timestamp"), data_log.get("action_type"))
