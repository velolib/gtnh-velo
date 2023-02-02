import itertools
from typing import TYPE_CHECKING

from gregtech.flow.gtnh.overclocks import OverclockHandler

from ._utils import round_readable

if TYPE_CHECKING:
    from gregtech.flow.cli import ProgramContext
    from gregtech.flow.data.basic_types import Recipe


class Graph:

    def __init__(self, graph_name: str, recipes: list, parent_context: 'ProgramContext', title: str = ''):
        """
        Graph abstraction class. This is not the graphviz Digraph class.

        Args:
            graph_name (str): Graph name, used as a title
            recipes (list): List of recipes
            parent_context (ProgramContext): ProgramContext object
            title (_type_, optional): _description_. Defaults to None.
        """
        self.graph_name = graph_name
        self.recipes: dict[str, 'Recipe'] = {str(i): x for i, x in enumerate(recipes)}
        self.nodes: dict = {}
        self.edges: dict = {}  # uniquely defined by (machine from, machine to, ing name)
        self.parent_context = parent_context
        self.graph_config = parent_context.graph_config
        self.title = title

        # Populated later on
        self.adj: dict = {}
        self.adj_machine: dict = {}

        self._color_dict: dict = dict()
        if self.graph_config.get('USE_RAINBOW_EDGES', None):
            self._color_cycler = itertools.cycle(self.graph_config['EDGECOLOR_CYCLE'])
        else:
            self._color_cycler = itertools.cycle(['#ffffff'])

        # Overclock all recipes to the provided user voltage
        oh = OverclockHandler(self.parent_context)
        for i, rec in enumerate(recipes):
            recipes[i] = oh.overclock_recipe(rec)
            rec.base_eut = rec.eut

        # DEBUG
        for rec in recipes:
            self.parent_context.log(rec)
        self.parent_context.log('')
        self._machine_check.cache_clear()

    @staticmethod
    def userRound(number: int | float) -> str:
        return round_readable(number)

    # Imports
    from ._port_nodes import _combine_inputs  # type: ignore
    from ._port_nodes import _combine_outputs  # type: ignore
    from ._port_nodes import (check_node_has_port, get_ing_id,  # type: ignore
                              get_ing_label, get_input_port_side,
                              get_output_port_side, get_port_id,
                              get_quant_label, get_unique_color,
                              strip_brackets)
    from ._utils import (_machine_check, _machine_iterate,  # type: ignore
                         add_edge, add_node, create_adjacency_list,
                         idx_to_voltage)
