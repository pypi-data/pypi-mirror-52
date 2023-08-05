"""
OCR-D reference implementation, base package: decorators and classes for processors and CLIs.

Related (and dependent) packages:
* ``ocrd_utils``
  Contains utilities and constants, e.g. for logging, path normalization, coordinate calculation etc.
* ``ocrd_models``
  Contains file format wrappers for PAGE-XML, METS, EXIF metadata etc.
* ``ocrd_modelfactory``
  Code to instantiate models from existing data.
* ``ocrd_validators``
  Schemas and routines for validating BagIt, ``ocrd-tool.json``, workspaces, METS, page, CLI parameters etc.
"""

from ocrd.processor.base import run_processor, run_cli, Processor
from ocrd_models import OcrdMets, OcrdExif, OcrdFile, OcrdAgent
from ocrd.resolver import Resolver
from ocrd_validators import *
from ocrd.workspace import Workspace
from ocrd.workspace_backup import WorkspaceBackupManager
