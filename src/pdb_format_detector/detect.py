import numpy as np
from Bio.PDB import PDBParser, MMCIFParser, PDBIO, MMCIFIO
from Bio.PDB import binary_cif as _binary_cif
from Bio.PDB.binary_cif import BinaryCIFParser

from sys import stderr


def _patched_string_array_decoder(column):
    """Workaround for a Biopython bug (still present as of 1.88): the stock decoder
    ignores the column mask and always does unique_strings[lookups], which crashes
    with IndexError whenever a string column is entirely null (e.g. most structures'
    _atom_site.pdbx_PDB_ins_code) since the dictionary is then empty but lookups is
    still -1. -1 marks a null entry per the BinaryCIF spec and must not be indexed."""
    encoding = column["data"]["encoding"][-1]
    assert encoding["kind"] == "StringArray"

    offsets_column = {
        "data": {"data": encoding["offsets"], "encoding": encoding["offsetEncoding"]}
    }
    lookup_column = {
        "data": {"data": column["data"]["data"], "encoding": encoding["dataEncoding"]}
    }

    string_data = encoding["stringData"]
    offsets = _binary_cif._decode(offsets_column)
    unique_strings = np.empty((len(offsets) - 1,), dtype=object)
    for index in range(len(unique_strings)):
        unique_strings[index] = string_data[offsets[index]: offsets[index + 1]]

    lookups = _binary_cif._decode(lookup_column)
    decoded = np.empty(lookups.shape, dtype=object)
    valid = lookups >= 0
    decoded[valid] = unique_strings[lookups[valid]]
    decoded[~valid] = None

    column["data"]["data"] = decoded
    column["data"]["encoding"].pop()


_binary_cif._decoders["StringArray"] = _patched_string_array_decoder


class PDBDetector:
    FORMAT_DESC = {"pdb": "Legacy PDB",
                   "cif": "PDBx/mmCIF",
                   "mmcif": "PDBx/mmCIF",
                   "bcif": "binary mmCIF"}

    def __init__(self, filename: str) -> None:
        attempts = (
            ("cif", MMCIFParser(QUIET=True)),
            ("pdb", PDBParser(QUIET=True)),
            ("bcif", BinaryCIFParser()),
        )
        struct = None
        pformat = None
        for candidate_format, parser in attempts:
            try:
                candidate_struct = parser.get_structure("test_format", filename)
                if len(list(candidate_struct.get_atoms())) == 0:
                    raise ValueError("parsed structure contains no atoms")
                struct = candidate_struct
                pformat = candidate_format
                break
            except Exception as e:
                print(f"File is NOT in the {self.FORMAT_DESC[candidate_format]} format ({e}), trying next...",
                      file=stderr)

        if struct is None:
            raise ValueError(f"Could not determine structure format for {filename!r}: "
                              f"failed to parse as PDB, mmCIF, or binary CIF.")

        self.structure = struct
        self.format = pformat

    def get_format(self, detailed: bool = False) -> str:
        """Return the format detected at construction time.

        With detailed=False (default), returns the short code: "pdb", "cif", or "bcif".
        With detailed=True, returns the human-readable name instead (e.g. "PDBx/mmCIF").
        """
        if detailed:
            return self.FORMAT_DESC[self.format]
        return self.format

    def save(self, output: str, out_format: str = "cif") -> None:
        """Write the parsed structure to `output` in `out_format` ("pdb", "cif", or "mmcif").

        "cif" and "mmcif" are equivalent and both write mmCIF. An unrecognized out_format
        falls back to "cif" with a warning on stderr. Raises NotImplementedError for
        out_format="bcif": Biopython can read binary CIF but has no writer for it.
        """
        if out_format.lower() == "bcif":
            raise NotImplementedError("Saving in binary CIF format is not supported: "
                                       "Biopython only provides a BinaryCIF reader, no writer.")
        if out_format.lower() not in ("pdb", "cif", "mmcif"):
            print(f"{out_format} is not one of accepted file formats, using cif/mmcif instead...", file=stderr)
            out_format = "cif"
        if out_format in ("cif", "mmcif"):
            structio = MMCIFIO()
        else:
            structio = PDBIO()
        structio.set_structure(self.structure)
        structio.save(output)
        print(f"Structure saved as {output} in the {self.FORMAT_DESC[out_format]} format.", file=stderr)
