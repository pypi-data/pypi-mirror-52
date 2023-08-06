def generate_plumed_inputfile(self, parameters):
    """
    Prepare the input file for Plumed
    
    param: parameters: list of dictionaries of input data
    returns:  
    
    In Plumed it's common to use actions more than once and the
    order of the actions is important. In Python dicts this presents
    a problem as keys must be unique. The solution we implement is 
    not to use a dictionary of dictionaries, as is common for other 
    AiiDA plugins, but a list of dictionaries. We then read the list
    in order. Each dictionary must have a key called 'action' which 
    stores the name of the action to be carried out. The remaining 
    keys are then different parameters or options for the action.
    If the key is a parameter, it's value is stored as a string.
    If it's an option, it's value should be stored as (boolean) True.
    One can also set it to (boolean) False in which case it is ignored and
    not printed.
    
    Example input list:
     [ { 'action' : 'group' ,  
         'atoms' : '1,2,3,4' ,
         'label' : 'chainA'
       },
       { 'action' : 'GROUP' ,
         'atoms' : '5,6,7,8' ,
         'label' : 'chainB'
       },
       { 'action' : 'coordination' ,
         'groupa' : 'chainA' ,
         'groupb' : 'chainB' ,
         'nopbc'  : True ,
         'R_0'    : '1.0'
       }
     ]

    Printed output string:
    GROUP LABEL=chainA ATOMS=1,2,3,4 
    GROUP LABEL=chainB ATOMS=5,6,7,8 
    COORDINATION R_0=1.0 NOPBC GROUPA=chainA GROUPB=chainB 
    
    """
     
    # Empty string to hold the content of the input file
    input_text = ""

    #Run over the list of dictionaries.
    #The key, 'action', corresponds to a Plumed action.
    #Write this this keyword to the stanza
    #Run over the other keys and add them to the stanza
    #Add the stanza to the input file string.
    # Note: we convert action or parameters names to
    # uppercase. This not required by Plumed, but is 
    # readability convention.
                  
    # Loop over primary list:
    for action_dict in parameters:
        try:
            stanza = action_dict['action'].upper() + ' '
        except KeyError:
            print("No 'action' key found in "
                  "action dict: {}".format(action_dict))
            raise
        # Loop over the other dictionary keys to get the parameters   
        for param,value in action_dict.items():
            if param == 'action':
                continue
            if value is True :
                stanza += param.upper() + ' '
            elif value is False :
                continue
            else:
                stanza += param.upper() +'=' + value + ' '
        input_text += stanza + '\n'

    print(input_text)
    return  

