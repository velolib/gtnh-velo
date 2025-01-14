"""GT: Flow CLI wrapper implementation."""

from __future__ import annotations

import logging
from pathlib import Path

from gregtech.flow.cli import ProgramContext


def flow(project_name: Path | str, output_path: Path | str = 'output/', projects_path: Path |
         str = 'projects/', create_dirs: bool = False, config_path: Path | str = 'flow_config.yaml'):
    """GT: Flow CLI wrapper. Note that this is basically the Direct CLI.

    Args:
        project_name (Path | str): Project path relative to projects_path
        output_path (Path | str, optional): Output path. Defaults to 'output/'.
        projects_path (Path | str, optional): Path to projects directory. Defaults to 'projects/'.
        create_dirs (bool, optional): Whether or not to create output_path and projects_path
        config_path (Path | str, optional): Configuration file path. Will create one no matter what if nonexistent. Defaults to 'flow_config.yaml'
    """
    project_name = Path(project_name)
    projects_path = Path(projects_path)
    output_path = Path(output_path)
    config_path = Path(config_path)

    pc = ProgramContext(output_path, projects_path, create_dirs, config_path)

    if not output_path.exists() or not output_path.is_dir():
        raise FileNotFoundError(f'Invalid output_path: {output_path}')
    if not projects_path.exists() or not projects_path.is_dir():
        raise FileNotFoundError(f'Invalid projects_path: {projects_path}')

    rich = logging.getLogger('rich')
    rich.setLevel(logging.CRITICAL + 1)
    pc.quiet = True

    pc.create_graph(project_name)
