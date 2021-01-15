"""[ runs the program ]"""
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from . import auto_load as AutoLoader
from .src.InternalProperties.PropertyConstructor import construct_properties
from .src.MaterialManagers.ManagerInstance import construct_mgm

bl_info = {
    "name" : "BTestMK1",
    "author" : "Paige",
    "description" : "",
    "blender" : (2, 90, 0),
    "version" : (0, 0, 32),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

AutoLoader.init()

def register():
    """[ register using autoload ]"""
    AutoLoader.register()

def unregister():
    """[ unregister using autoload ]"""
    AutoLoader.unregister()

if __name__ == "__main__":
    register()
    construct_properties()
    construct_mgm()
