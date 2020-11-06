import bpy

# File
def get_current_filepath():
    return bpy.data.filepath

def save( filepath=None, **kwargs ):
    if filepath is None:
        filepath = get_current_filepath()
        
    return bpy.ops.wm.save_mainfile( filepath=filepath, **kwargs )

# Scene
def get_current_frame():
    return bpy.context.scene.frame_current

def get_scene_cache_filepaths():
    return [cacheFile.filepath for cacheFile in bpy.data.cache_files]

# Hierarchy

def get_top_node( object ):
    root = object
    while root.parent:
        root = root.parent
    
    return root

def get_descendants( object ):
    descendants = []
    for child in object.children:
        descendants.append( child )
        descendants.extend( get_descendants( child ) )
    
    return descendants

def parent(child, parent):
    if not child.name in parent.children.keys():
        parent.children.link(child)

# Selection

def select(objects):
    objects = objects if hasattr( objects, '__iter__' ) else [ objects ]
    for object in objects:
        bpy.context.view_layer.objects.active = object
        object.select_set(state=True)

def clear_selection():
    bpy.ops.object.select_all(action='DESELECT')

def select_hierarchy(objects, exclude = [], caseSensitive = False, fullpath = False):
    clear_selection()
    
    objects = objects if hasattr( objects, '__iter__' ) else [ objects ]
    exclude = exclude if hasattr( exclude, '__iter__' ) else [ exclude ]
    exclude = [get_object_by_name(object) if isinstance(object, str) else object for object in exclude]
    
    for object in objects:
        if isinstance(object, str):
            objects = get_object_by_name(object)
        descendants = get_descendants(object)
        select([o for o in descendants if not o in exclude])

# Object

def get_object_by_name(name):
    return next((object for object in bpy.data.objects if object.name == name), None)

def get_object_using_cache(cache):
    assetObjs = []
    for object in bpy.data.objects:
        identified = False
        
        attrs = object.modifiers.values() + object.constraints.values()
        for item in attrs:
            if getattr( item, 'cache_file', None ) == cache:
                if not object in assetObjs:
                    assetObjs.append( object )
                identified=True
                break
        
        if identified:
            break
    
    return assetObjs

def get_Object_using_data(data):
    return next((object for object in bpy.data.objects if object.data == data), None)

# Library

def get_library_using_object(object):
    for lib in bpy.data.libraries:
        if object.data in lib.users_id:
            return lib

# Cache

def get_cache_using_object(object):
    for cache in object.modifiers.values() + object.constraints.values():
        cache_file = getattr( cache, 'cache_file', None )
        if cache_file:
            return cache_file
    
# Animation

def get_object_keyframes(object):
    data = {}
    tracks = object.animation_data.action.fcurves
    for fcu in tracks:
        data[fcu.data_path] = [keyframe.co for keyframe in fcu.keyframe_points]
    return data

def clear_object_animation(object, data):
    tracks = object.animation_data.action.fcurves
    for fcu in tracks:
        if fcu.data_path == data:
            tracks.remove(fcu)

# Collection

def get_collection_using_object(context, object):
    collections = object.users_collection
    if collections:
        return collections
    return context.scene.collection

def create_collection(name):
    collections = [ c for c in bpy.data.collections if c.name == name]
    if collections:
        return collections[0]
    else:
        collection = bpy.data.collections.new(name)
        return collection

def add_objects_to_collection(collection, objects = [], move=False):
    for o in objects:
        if move:
            oldCollections = get_collection_using_object(bpy.context, o)
            for oc in oldCollections:
                oc.objects.unlink(o)
            print ("Moving {object} to {collection} Collection".format(object=o, collection=collection.name))
        else:
            print ("Adding {object} to {collection} Collection".format(object=o, collection=collection.name))
        collection.objects.link(o)

# Clean Up

def delete_hierarchy(objects):
    objects = objects if hasattr( objects, '__iter__' ) else [ objects ]
    allObjects = []
    for object in objects:
        allObjects.append( object )
        for obj in get_descendants( object ):
            allObjects.append( obj )
    bpy.ops.object.delete( { 'selected_objects': allObjects } )

def remove_library(lib):
    lib.user_clear()

def purge(context):
    override = context.copy()
    override["area.type"] = ['OUTLINER']
    override["display_mode"] = ['ORPHAN_DATA']
    bpy.ops.outliner.orphans_purge(override) 

def remove_asset_using_object(context, object):
    cache = get_cache_using_object(object)
    objects = [get_top_node(obj) for obj in get_object_using_cache(cache)]
    lib = get_library_using_object(object)
    
    delete_hierarchy(objects)
    remove_library(lib)
    purge(context)

# Viewport
def viewport_context():
    override = {}
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                override['window'] = window
                override['screen'] = window.screen
                override['area'] = area
                for space in area.spaces:
                    if space.type == 'VIEW_3D': 
                        override['space_data'] = space
                    
                return override

def focus_selected():
    context = viewport_context()
    area = context['area']
    for region in area.regions:
        if region.type == 'WINDOW':
            override = {'area': area, 'region': region}
            bpy.ops.view3d.view_selected(override)