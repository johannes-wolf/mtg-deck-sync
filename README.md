# About

This is a small tool to keep local MtG decks for online play in sync
with online decklists.

# Sample Configuration

Store a toml configuration file of the following format as "decks.toml".
By default, the tool picks up the "decks.toml" file in the current working
directory.

```toml
[deck."Pauper - Bogles"]
url = "https://archidekt.com/decks/14783773/bogles"
file = "Pauper/Bogles.dck"
format = "xmage"

[deck."Pauper - Terror"]
url = "https://archidekt.com/decks/14107899/mono_blue_terror"
file = "Pauper/Terror.dck"
format = "xmage"
```
