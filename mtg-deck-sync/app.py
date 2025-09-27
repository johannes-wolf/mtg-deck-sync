import mtg_parser as mtg
import tomllib as toml
import sys

deckfile = "decks.toml"
config = None

format_extension = {
    "text": "txt",
    "dck": "dck",
    "xmage": "dck",
}

def get_deck(cfg, cards):
    mainboard = []
    sideboard = []
    maybeboard = []

    for card in cards:
        if "sideboard" in card.tags or "commander" in card.tags:
            sideboard.append(card)
            if "maybeboard" in card.tags:
                print(f"    warning: Card '{card.name}' is in sideboard and maybeboard! Putting it into sideboard.")
        elif "maybeboard" in card.tags:
            maybeboard.append(card)
        else:
            mainboard.append(card)

    return mainboard, sideboard, maybeboard

def get_fixed_extension_number(card):
    number = card.number.upper()
    extension = card.extension.upper()
    if extension == "PLST":
        parts = number.split("-")
        extension = parts[0]
        number = parts[1]
    return extension, number


def txt_writer(filename, cards, cfg):
    mainboard, sideboard, maybeboard = get_deck(cfg, cards)

    mainboard_heading = cfg.get("mainboard", "Mainboard")
    sideboard_heading = cfg.get("sideboard", "Sideboard")
    maybeboard_heading = cfg.get("maybeboard", "Maybeboard")

    def format_card(prefix, card):
        extension, number = get_fixed_extension_number(card)

        return f"{card.quantity} {card.name} ({extension})"

    with open(filename, "w") as file:
        if len(mainboard) > 0:
            if mainboard_heading:
                file.write(f"{mainboard_heading}\n")
            for card in mainboard:
                file.write(format_card(card))
        if len(sideboard) > 0:
            if sideboard_heading:
                file.write(f"{sideboard_heading}\n")
            for card in sideboard:
                file.write(format_card(card))
        if len(maybeboard) > 0:
            if maybeboard_heading:
                file.write(f"{maybeboard_heading}\n")
            for card in maybeboard:
                file.write(format_card(card))


def dck_writer(filename, cards, cfg):
    mainboard, sideboard, maybeboard = get_deck(cfg, cards)

    xmage_extension_fix = {
        "4BB": "4ED",
    }

    def format_card(prefix, card):
        extension, number = get_fixed_extension_number(card)
        extension = xmage_extension_fix.get(extension, extension)

        name = card.name
        if name.find("//"):
            name = name.split("//")[0]

        return f"{prefix}{card.quantity} [{extension}:{number}] {name}\n"

    with open(filename, "w") as file:
        if len(mainboard) > 0:
            for card in mainboard:
                file.write(format_card("", card))
        if len(sideboard) > 0:
            for card in sideboard:
                file.write(format_card("SB: ", card))


format_writer = {
    "dck": dck_writer,
    "xmage": dck_writer,
    "text": txt_writer,
}


def sync_deck(name, deck_config):
    url = deck_config.get("url")
    if not url:
        return

    name = deck_config.get("name") or name
    format = deck_config.get("format") or "text"
    file = deck_config.get("file") or f"{name}.{format_extension[format]}"

    cards = list(mtg.parse_deck(url))
    if not format in format_writer:
        raise Exception(f"Unknown format: {format}")

    print(f"  - {name} → {file}")
    writer = format_writer[format]
    writer(file, cards, deck_config)

if __name__ == "__main__":
    try:
        with open(deckfile, "rb") as config_file:
            config = toml.load(config_file)
    except Exception as error:
        print(f"Could not load '{deckfile}'. Error: {error}.")
        sys.exit(-1)

    print("Syncing decks:")
    for name, deck in config["deck"].items():
        sync_deck(name, deck)
