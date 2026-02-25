def parse_data(data: dict) -> dict:
    """
    Parses Telegram message payload and extracts relevant fields
    for structured storage.

    Returns a dictionary ready to be converted into a PyArrow table.
    """

    parsed_data = {}

    for key, value in data.items():

        if key == "from":
            for k, v in value.items():
                if k in ["id", "is_bot", "first_name"]:
                    parsed_data[f"user_{k}"] = [v]

        elif key == "chat":
            for k, v in value.items():
                if k in ["id", "type"]:
                    parsed_data[f"chat_{k}"] = [v]

        elif key in ["message_id", "date", "text"]:
            parsed_data[key] = [value]

    # Guarantee column consistency
    if "text" not in parsed_data:
        parsed_data["text"] = [None]

    return parsed_data
