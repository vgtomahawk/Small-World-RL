"""
RoomsOptions Environment
"""

import numpy as np
import networkx as nx
import pdb

from Environment import *
import OptionGenerator
from Rooms import Rooms

class RoomsOptions( ):

    @staticmethod
    def create( spec, scheme = 'none', count = 20, *args ):
        """
        @spec - Specification (size, endpoints, barriers); either exactly
                specified in a file, or with numeric values in a list
        @option_scheme - none|manual|optimal|small-world|random|ozgur's betweenness|ozgur's randomness|end
        @n_actions - Number of steps that need to taken
        comment : optimal(shortest path to destination)??|random|ozgur's betweenness|ozgur's randomness
        """

        env = Rooms.create( spec )
        g = env.to_graph()
        gr = g.reverse()

        # Percentage
        if isinstance(count,str):
            count = int(count[:-1])
            count = count*env.S/100

        # Add options for all the optimal states
        O = []
        if scheme == "none":
            pass
        elif scheme == "random-node":
            O = OptionGenerator.optimal_options_from_random_nodes( g, gr, count, *args )
        elif scheme == "random-path":
            O = OptionGenerator.optimal_options_from_random_paths( g, gr, count, *args )
        elif scheme == "betweenness":
            O = OptionGenerator.optimal_options_from_betweenness( g, gr, count, *args )
        elif scheme == "small-world":
            O = OptionGenerator.optimal_options_from_small_world( g, gr, count, *args )
        elif scheme == "betweenness+small-world":
            O = OptionEnvironment.optimal_options_from_betweenness( g, gr, count )
            count_ = count - len( O ) 
            O += OptionEnvironment.optimal_options_from_small_world( g, gr, count_, *args )
        elif scheme == "load":
            O = OptionGenerator.options_from_file( *args )
        else:
            raise NotImplemented() 

        return OptionEnvironment( env.S, env.A, env.P, env.R, env.R_bias, env.start_set, env.end_set, O )

    @staticmethod
    def reset_rewards( env, spec, *args ):
        O = env.O
        env = Rooms.reset_rewards( env, spec )
        return OptionEnvironment( env.S, env.A, env.P, env.R, env.R_bias, env.start_set, env.end_set, O )

