import argparse

__version__ = "0.3.1"
__author__ = "Oprax <oprax@me.com>"


def main():
    from .Extractor import Extractor

    parser = argparse.ArgumentParser(description="Extract token from FreeOTP")
    parser.add_argument(
        "-v", "--version", action="version", version="{}".format(__version__)
    )
    parser.add_argument(
        "input", help="File containing XML with tokens (usually 'tokens.xml')"
    )
    parser.add_argument(
        "-o",
        "--output",
        required=False,
        action="store",
        help="Give the output file for save tokens",
    )
    parser.add_argument(
        "-q",
        "--qrcode",
        required=False,
        action="store",
        choices=("term", "svg", "eps"),
        help="Use a JSON input to recreate QRcode for each issuer. Use 'term' to display directly to the terminal, 'svg' and 'eps' output the qrcode into a file",
    )
    args = parser.parse_args()

    ext = Extractor(args.input)
    if args.qrcode:
        ext.qrcode(args.qrcode, args.output)
    else:
        ext.run(args.output)


if __name__ == "__main__":
    main()
