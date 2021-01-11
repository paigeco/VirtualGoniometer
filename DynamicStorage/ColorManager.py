import bpy
from DynamicStorage.AccesibleColors import DIFFERENTIABLE_COLORS

# IT HAD TO BE DONE THIS WAY FOR ACCESIBILITY REASONS
# DON'T WORRY I PROBABLY FEEL WORSE ABOUT HOW UN-PYTHONIC
# THIS LOOKS THAN YOU DO
#
#
# THANKS TO SASHA TRUBESKY'S 20 COLORS RESOURCE!
# https://sashamaps.net/docs/resources/20-colors/
class ColorPairs(object):
    def __init__ (self):
        try:
            self.access_level = bpy.context.scene.cs_overall_VG_.accesibility_level
            self.active_colors = self.color_compresser(self.access_level)
        except AttributeError:
            pass
        
    # INSERT LEVEL OF ACCESSIBILITY REQUIRED
    # 0 for 100%
    # 1 for 99.99%
    # 2 for 99%
    # 3 for 95%
    # compresses recursively
    def color_compresser(self,x):
        try:
            if x >= 0:
                return self.color_compresser(x-1) + DIFFERENTIABLE_COLORS[x]
            else:
                return []
        except IndexError:
            return self.color_compresser(x-1) + []

    def get_pairs(self):
        offset = 0
        pairs = []
        for x in range(1,len(self.active_colors)):
            for y in range(0,x):
                
                # TODO:: YOU BETTER FIX THIS BEFORE RELEASE
                #    YOU UGLY LITTLE SCAMP
                ax = [float(c / 255.0) for c in self.active_colors[x]]
                ay = [float(c / 255.0) for c in self.active_colors[y]]
                
                pairs.append([ax, ay])
                
            offset += 1
        return pairs
    
    def return_active_pairs(self):
        al = bpy.context.scene.cs_overall_VG_.accesibility_level
        self.active_colors = self.color_compresser(al)
        # if sum([n for n in len(self.active_colors)])
        # TODO ADD LOOPING FOR ERROR ISSUES
        return self.get_pairs()