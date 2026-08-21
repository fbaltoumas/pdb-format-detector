# pdb-format-detector
 A small tool to automatically detect the file format of a structure (PDB) input

## Install

```bash
pip install .
```

## Usage

```python
from pdb_format_detector import PDBDetector

d = PDBDetector("structure.bcif")   # accepts legacy PDB, mmCIF, or binary CIF
d.get_format()                      # "pdb", "cif", or "bcif"
d.get_format(detailed=True)         # "Legacy PDB", "PDBx/mmCIF", or "binary mmCIF"
d.save("structure.cif", out_format="cif")   # write out as pdb, cif, or mmcif
```
