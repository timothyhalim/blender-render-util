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

bl_info = {
    "name" : "Render Utilities",
    "author" : "Timothy Halim",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

import bpy

from .panel import RenderUtil_PT_Panel

from .operator import RenderUtil_OT_RemoveAsset
from .operator import RenderUtil_OT_CleanVisibilityKey
from .operator import RenderUtil_OT_CreateHiddenAllCollection


classes = (RenderUtil_PT_Panel, RenderUtil_OT_RemoveAsset, RenderUtil_OT_CleanVisibilityKey, RenderUtil_OT_CreateHiddenAllCollection)

# register, unregister = bpy.utils.register_classes_factory(classes)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
