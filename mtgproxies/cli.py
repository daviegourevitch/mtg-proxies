from pathlib import Path

from mtgproxies.decklists import archidekt, manastack, parse_decklist
from mtgproxies.decklists.decklist import Decklist


def parse_decklist_spec(decklist_spec: str, hidebacks: bool = False, warn_levels=["ERROR", "WARNING", "COSMETIC"]) -> Decklist:
    """Attempt to parse a decklist from different locations.

    Args:
        decklist_spec: File path or ManaStack id
        warn_levels: Levels of warnings to show
    """
    print("Parsing decklist ...")
    if Path(decklist_spec).is_file():  # Decklist is file
        decklist, ok, warnings = parse_decklist(decklist_spec, hidebacks=hidebacks)
    elif decklist_spec.lower().startswith("manastack:") and decklist_spec.split(":")[-1].isdigit():
        # Decklist on Manastack
        manastack_id = decklist_spec.split(":")[-1]
        decklist, ok, warnings = manastack.parse_decklist(manastack_id, hidebacks=hidebacks)
    elif decklist_spec.lower().startswith("archidekt:") and decklist_spec.split(":")[-1].isdigit():
        # Decklist on Archidekt
        manastack_id = decklist_spec.split(":")[-1]
        decklist, ok, warnings = archidekt.parse_decklist(manastack_id, hidebacks=hidebacks)
    else:
        print(f"Cant find decklist '{decklist_spec}'")
        quit()

    # Print warnings
    for _, level, msg in warnings:
        if level in warn_levels:
            print(f"{level}: {msg}")

    # Check for grave errors
    if not ok:
        print("Decklist contains invalid card names. Fix errors above before reattempting.")
        quit()

    print(f"Found {decklist.total_count} cards in total with {decklist.total_count_unique} unique cards.")

    return decklist
