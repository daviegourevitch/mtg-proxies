import argparse

import numpy as np

from mtgproxies import fetch_scans_scryfall, print_cards_matplotlib, print_cards_fpdf
from mtgproxies.cli import parse_decklist_spec


def papersize(string):
    spec = string.lower()
    if spec == "a4":
        return np.array([21, 29.7]) / 2.54
    if "x" in spec:
        split = spec.split("x")
        return np.array([float(split[0]), float(split[1])])
    raise argparse.ArgumentTypeError()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepare a decklist for printing.")
    parser.add_argument(
        "decklist",
        metavar="decklist_spec",
        help="path to a decklist in text/arena format, or manastack:{manastack_id}, or archidekt:{archidekt_id}",
    )
    parser.add_argument("outfile", help="output file. Supports pdf, png and jpg.")
    parser.add_argument("--dpi", help="dpi of output file (default: %(default)d)", type=int, default=300)
    parser.add_argument(
        "--paper",
        help="paper size in inches or preconfigured format (default: %(default)s)",
        type=papersize,
        default="a4",
        metavar="WIDTHxHEIGHT",
    )
    parser.add_argument(
        "--scale",
        help="scaling factor for printed cards (default: %(default)s)",
        type=float,
        default=1.0,
        metavar="FLOAT",
    )
    parser.add_argument(
        "--border_crop",
        help="how much to crop inner borders of printed cards (default: %(default)s)",
        type=int,
        default=14,
        metavar="PIXELS",
    )
    parser.add_argument(
        "--background",
        help='background color, either by name or by hex code (e.g. black or "#ff0000", default: %(default)s)',
        type=str,
        default=None,
        metavar="COLOR",
    )
    parser.add_argument(
        "--xshift",
        help='The amount to shift all cards to the left. Can be negative. (default: %(default)s)',
        type=int,
        default=4,
        metavar="XSHIFT",
    )
    parser.add_argument(
        "--yshift",
        help='The amount to shift all cards down. Can be negative. (default: %(default)s)',
        type=int,
        default=2,
        metavar="YSHIFT",
    )
    parser.add_argument(
        "--xmargin",
        help='The amount of space to put between the left and right of all cards. (default: %(default)s)',
        type=int,
        default=4,
        metavar="XMARGIN",
    )
    parser.add_argument(
        "--ymargin",
        help='The amount of space to put between the top and bottom of all cards. (default: %(default)s)',
        type=int,
        default=2,
        metavar="YMARGIN",
    )
    parser.add_argument(
        "--hidebacks",
        action="store_true",
        help='If specified, only the front face of double-sided cards will be included. (default: %(default)s)',
        default=False,
    )
    args = parser.parse_args()

    # Parse decklist
    decklist = parse_decklist_spec(args.decklist, args.hidebacks is not None)

    # Fetch scans
    images = fetch_scans_scryfall(decklist)

    # Plot cards
    if args.outfile.endswith(".pdf"):
        import matplotlib.colors as colors

        background_color = args.background
        if background_color is not None:
            background_color = (np.array(colors.to_rgb(background_color)) * 255).astype(int)

        print_cards_fpdf(
            images,
            args.outfile,
            papersize=args.paper * 25.4,
            cardsize=np.array([2.5, 3.5]) * 25.4 * args.scale,
            border_crop=args.border_crop,
            background_color=background_color,
            xshift=args.xshift,
            yshift=args.yshift,
            xmargin=args.xmargin,
            ymargin=args.ymargin,
        )
    else:
        print_cards_matplotlib(
            images,
            args.outfile,
            papersize=args.paper,
            cardsize=np.array([2.5, 3.5]) * args.scale,
            dpi=args.dpi,
            border_crop=args.border_crop,
            background_color=args.background,
        )
