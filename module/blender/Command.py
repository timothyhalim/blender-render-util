import bpy

def get_library_using_object(object):
    for lib in bpy.data.libraries:
        if object.data in lib.users_id:
            return lib

def get_cache_using_object(object):
    for cache in object.modifiers.values() + object.constraints.values():
        cache_file = getattr( cache, 'cache_file', None )
        if cache_file:
            return cache_file
    
def get_object_using_cache( cache ):
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

def delete_objects(objects):
    objects = objects if hasattr( objects, '__iter__' ) else [ objects ]
    allObjects = []
    for object in objects:
        allObjects.append( object )
        for obj in get_descendants( object ):
            allObjects.append( obj )
    bpy.ops.object.delete( { 'selected_objects': allObjects } )

def purge(context):
    override = context.copy()
    override["area.type"] = ['OUTLINER']
    override["display_mode"] = ['ORPHAN_DATA']
    bpy.ops.outliner.orphans_purge(override) 

def remove_library(lib):
    lib.user_clear()

def remove_asset_using_object(context, object):
    cache = get_cache_using_object(object)
    objects = [get_top_node(obj) for obj in get_object_using_cache(cache)]
    lib = get_library_using_object(object)
    
    delete_objects(objects)
    remove_library(lib)
    purge(context)


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
