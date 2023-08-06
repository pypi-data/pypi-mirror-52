# -*- coding: utf-8 -*-
"""
Common tools for preparing Plumed inputs for calculations
"""
from __future__ import absolute_import
from __future__ import print_function


class BasePlumedInputGenerator(object):
    """
    Baseclass for the standard Plumed inputs.
    """
    _INPUT_FILE_NAME = 'plumed.in'
    _OUTPUT_FILE_NAME = 'plumed.out'
    _COLVAR_FILE_NAME = 'COLVAR.dat'

    def _generate_plumed_inputfile(self, parameters):
        """
        Prepare the input file for Plumed
        
        param: parameters: dictionary of input data
        returns:  
        """

        # Empty string to hold the content of the input file
        input_text = ""

        # Run over the primary keys of the parameters dictionary
        # Each key corresponds to a Plumed action.
        # Write this to this keyword to the stanza
        # Run over the arguments to this key word
        # Add them and finally add the stanza to the input file
        # string.

        for action, args in parameters.items():
            stanza = action + ' '
            for item in args:
                stanza += item + ' '
            input_text += stanza + '\n'

        return print(input_text)
