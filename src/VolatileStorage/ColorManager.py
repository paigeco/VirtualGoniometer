"""[ code for generating color blind friendly color pairs ]"""
import bpy
from .AccesibleColors import DIFFERENTIABLE_COLORS, COLOR_NAMES

# IT HAD TO BE DONE THIS WAY FOR ACCESIBILITY REASONS
# DON'T WORRY I PROBABLY FEEL WORSE ABOUT HOW UN-PYTHONIC
# THIS LOOKS THAN YOU DO
#
#
# THANKS TO SASHA TRUBESKY'S 20 COLORS RESOURCE!
# https://sashamaps.net/docs/resources/20-colors/
class ColorPairs():
    """[ generates color pairs ]"""
    def __init__(self):
        try:
            # Pull the access level
            self.access_level = bpy.context.scene.cs_overall_VG_.accesibility_level
            
            # Pull the active colors
            self.active_colors = self.color_compresser(self.access_level)
            
        except AttributeError:
            pass
        
    # INSERT LEVEL OF ACCESSIBILITY REQUIRED
    # 0 for 100%
    # 1 for 99.99%
    # 2 for 99%
    # 3 for 95%
    # compresses recursively
    def color_compresser(self, x):
        """[ recursively generates color pairs ]

        Args:
            x ([int]): [ access_level ]

        Returns:
            [list]: [ list of lists i think? ]
        """
        try:
            if x >= 0:
                return self.color_compresser(x-1) + DIFFERENTIABLE_COLORS[x]
            else:
                return []
        except IndexError:
            return self.color_compresser(x-1) + []

    def get_pairs(self):
        """ [  ]

        Returns:
            [pairs object]: [description]
        """
        offset = 0
        pairs = []
        for x in range(1, len(self.active_colors)):
            for y in range(0, x):
                
                # TODO:: YOU BETTER FIX THIS BEFORE RELEASE
                #    YOU UGLY LITTLE SCAMP
                ax = [float(c / 255.0) for c in self.active_colors[x]]
                ay = [float(c / 255.0) for c in self.active_colors[y]]
                
                pairs.append([ax, ay])
                
            offset += 1
        return pairs
    
    def return_active_pairs(self):
        """ [ returns the staged color pairs ]

        Returns:
            [type]: [description]
        """
        al = bpy.context.scene.cs_overall_VG_.accesibility_level
        self.active_colors = self.color_compresser(al)
        # if sum([n for n in len(self.active_colors)])
        # TODO ADD LOOPING FOR ERROR ISSUES
        return self.get_pairs()

    def get_tuple_from_color_name(self, name) -> 'tuple':
        
        # The Blender version of the V.G. doesn't support black
        if name == 'Black':
            # This is a bodge so colors come out the same
            return (255, 255, 255) 
        elif name in COLOR_NAMES:
            # Return the tuple
            return COLOR_NAMES[name]
        else: 
            return (255, 255, 255) #Is not in list return 'Black'
    
    def get_color_name_from_tuple(self, tupl) -> 'str':

        # Dictionary flip using dictionary compression, not efficient, but it doesn't matter
        tuple_names = {v:k for (k, v) in COLOR_NAMES.items()}
        
        print(tupl)
        print(tuple_names)
        # Find the name in tuple list.
        # TODO: At some point add functionality to find closest match to currently displayed
        #     color as colors are user editable
        if tupl in tuple_names:
            return tuple_names[tupl]
        else:
            return 'N/A'
        
