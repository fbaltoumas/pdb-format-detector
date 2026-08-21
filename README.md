# pdb-format-detector
 A small tool to automatically detect the file format of a structure (PDB) input

## Install

```bash
pip install .
```

## Usage

### As a Python package

```python
from pdb_format_detector import PDBDetector

d = PDBDetector("structure.bcif")   # accepts legacy PDB, mmCIF, or binary CIF
d.get_format()                      # "pdb", "cif", or "bcif"
d.get_format(detailed=True)         # "Legacy PDB", "PDBx/mmCIF", or "binary mmCIF"
d.save("structure.cif", out_format="cif")   # write out as pdb, cif, or mmcif
```

### As a command-line tool

```bash
pdb-format-detector -i structure.pdb
# pdb

pdb-format-detector -i structure.cif
# mmcif

pdb-format-detector -i structure.bcif
# bcif

pdb-format-detector -i structure.pdb -d
# Legacy PDB

pdb-format-detector -i structure.pdb -o structure.cif
pdb-format-detector -i structure.cif -o structure.pdb --output-format pdb
```

| Option | Description |
|---|---|
| `-i`, `--input` | Input structure file (required). |
| `-d`, `--detailed` | Print the human-readable format name instead of the short code. |
| `-o`, `--output` | Save the structure to this file, in the format given by `--output-format`. |
| `--output-format` | Format to use when saving with `-o`/`--output`: `pdb`, `cif`, or `mmcif` (default: `mmcif`). `cif` and `mmcif` are the same.|
| `-v`, `--version` | Show the installed version and exit. |
| `-h`, `--help` | Show usage and exit. |
