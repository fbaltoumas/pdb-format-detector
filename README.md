# pdb-format-detector
 A small tool to automatically detect the file format of a structure (PDB) input


**A bit of context**:

The Protein Data Bank (PDB) uses various file formats to store its structures, the main ones being:

 - **PDB (now known as "Legacy PDB")**: The default for many decades. A column-based format where atom information and coordinates were stored in 80-character long lines, starting with `ATOM` for protein/DNA coordinates and `HETATM` for heteroatoms. While relatively easy to use and parse (e.g. with Perl), this format eventually became obsolete, mostly due to the 80 character limit (a remnant of the old Fortran days), combined with the ever-increasing size of PDB assemblies (e.g. for whole viruses, with billions of atoms). It has been deprectated in favor of the new PDBx/mmCIF format (described below), although it is still kept for compatibility with older software and scripts.

 - **PDBx/mmCIF (or simply CIF)**:  The current default PDB format. A variation of the CIF format originally used in small molecule crystallographic data. The main improvement is that this format has no character limitations, and can actually handle very large structures.

 - **Binary CIF**: Binary version of the above.


**Why this tool exists**:

So, while modern tools, from structure viewers like `PyMOL` or `UCSF Chimera`, to search tools like `foldseek`, `reseek`, or `TM-align`, can recognize both the legacy PDB and the new CIF format (binary CIF, not so much), they don't always automatically recognize the file format by its contents.  Some tools try to auto-guess the format from the file extension (`*.pdb`, `*.cif` etc.), while others require the user to choose the format on their own. That's all fine when you are working with one or a few structures. But what if:

- you work with a large number of datasets (hundreds or thousands of structures), and they are not always in the same format? Imagine a mixture of `*.pdb` and `*.cif` files, plus some that do not necessarily have the standard extensions (e.g. the `*.ent` extension, which is often used interchangeably for PDB and CIF, or even some files saved as `*.txt`).  Any tool that depends on the extension for file format recognition would fail on the latter. So, you would have to either convert everything to the SAME format, or figure out a way to auto-recognize the format of the inputs.

- You want to create a pipeline, a web app, or something similar, that accepts user input (as text or file upload) and runs a structure-parsing workflow (e.g. runs `reseek` against a database).  You would have to either restrict yourself **AND your users** to one format (either PDB or CIF), or accommodate both. And in the latter case, you either expect the user to provide you with the information of which format they use, or somehow figure out how to auto-recognize the user input format, in order to run the workflow correctly.

This tool, `pdb-format-detector`, exists to automate this format detection issue. It auto-detects the three main PDB formats (legacy PDB, CIF, or binary CIF), returns the format to you and, optionally, converts the input structure to a format of your choosing.  Yes, you can do that by writing a python/Biopython script yourself, but this saves you the trouble, plus, gives you a way to quickly import structure format detection to your workflow.

`pdb-format-detector` works both as a command line tool and as a Python package.  You can run it in the CLI, use it in your bash script or nextflow pipeline, or import it as a module and use it in your python script instead.  Future updates will also include support for other, non-standard but commonly used structure formats, like the ones used in Molecular Dynamics tools (GROMACS, CHARMM, AMBER, NAMD etc).

## Install

```bash
git clone https://github.com/fbaltoumas/pdb-format-detector
cd pdb-format-detector
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
