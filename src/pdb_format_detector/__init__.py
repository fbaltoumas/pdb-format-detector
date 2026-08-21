"""Automatic format detection for macromolecular structure files (legacy PDB, PDBx/mmCIF, binary CIF)."""

from .detect import PDBDetector

__all__ = ["PDBDetector"]
__version__ = "1.0.0"
