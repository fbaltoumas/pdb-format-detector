import argparse
import sys

from . import __version__
from .detect import PDBDetector

_SHORT_FORMAT_DISPLAY = {"pdb": "pdb", "cif": "mmcif", "bcif": "bcif"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pdb-format-detector",
        description="Detect the format of a macromolecular structure file "
                     "(legacy PDB, PDBx/mmCIF, or binary CIF).",
    )
    parser.add_argument("-i", "--input", required=True,
                         help="Input structure file.")
    parser.add_argument("-d", "--detailed", action="store_true", required=False,
                         help="Print the human-readable format name instead of the short code.")
    parser.add_argument("-o", "--output", required=False,
                         help="Save the structure to this file, in the format given by --output-format.")
    parser.add_argument("--output-format", choices=("pdb", "cif", "mmcif"), default="mmcif", required=False,
                         help="Format to use when saving with -o/--output (default: mmcif).")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        detector = PDBDetector(args.input)

        if args.detailed:
            print(detector.get_format(detailed=True))
        else:
            print(_SHORT_FORMAT_DISPLAY[detector.get_format()])

        if args.output:
            detector.save(args.output, out_format=args.output_format)
    except (ValueError, NotImplementedError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
