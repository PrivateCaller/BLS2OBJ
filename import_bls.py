import os
import bpy, bmesh
import ntpath
from bpy_extras.io_utils import unpack_list
from bpy_extras import node_shader_utils

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def AddTex(blPath, Tex): # final command
    if bpy.data.textures.find(Tex) == -1:

        if Tex == 'PRINT':
            path = os.path.join(blPath, "base/data/shapes/spraycanLabel.png")
            print("Print textures are not implemented in the importer yet, replacing with spray can (don't spray your face)")
        else:
            path = os.path.join(blPath, "base/data/shapes/brick" + Tex + ".png")

        image = bpy.data.images.load(path)
        text = bpy.data.textures.new(Tex, 'IMAGE')
        text.image = image
        # text.image.use_fields = True

        if Tex == 'SIDE':
            text.extension = 'EXTEND'

    return

def AddFace(bmesh, POS1, POS2, POS3, POS4):
    POS1 = ( float(POS1[0]) , float(POS1[1]) , (float(POS1[2])/2.5) )
    POS2 = ( float(POS2[0]) , float(POS2[1]) , (float(POS2[2])/2.5) )
    POS3 = ( float(POS3[0]) , float(POS3[1]) , (float(POS3[2])/2.5) )
    POS4 = ( float(POS4[0]) , float(POS4[1]) , (float(POS4[2])/2.5) )

    Vert1 = bmesh.verts.new(POS1)
    Vert2 = bmesh.verts.new(POS2)
    Vert3 = bmesh.verts.new(POS3)
    Vert4 = bmesh.verts.new(POS4)

    NewFace = bmesh.faces.new( (Vert1,Vert2,Vert3,Vert4) )
    return NewFace

def AddUV(NewFace, UV1, UV2, UV3, UV4, Layer, Tex, Angle):

    if Tex == 'TOP':
        if float(Angle) == 2:
            UV1 = ( float(UV1[0]) , (float(UV1[1])*-1)+1 )
            UV2 = ( float(UV2[0]) , (float(UV2[1])*-1)+1 )
            UV3 = ( float(UV3[0]) , (float(UV3[1])*-1)+1 )
            UV4 = ( float(UV4[0]) , (float(UV4[1])*-1)+1 )

            NewFace.loops[3][Layer].uv = ( UV1[0] , UV1[1] )
            NewFace.loops[0][Layer].uv = ( UV2[0] , UV2[1] )
            NewFace.loops[1][Layer].uv = ( UV3[0] , UV3[1] )
            NewFace.loops[2][Layer].uv = ( UV4[0] , UV4[1] )

            return NewFace

        if float(Angle) == 3:
            UV1 = ( (float(UV1[1])*-1)+1 , (float(UV1[0])*-1)+1 )
            UV2 = ( (float(UV2[1])*-1)+1 , (float(UV2[0])*-1)+1 )
            UV3 = ( (float(UV3[1])*-1)+1 , (float(UV3[0])*-1)+1 )
            UV4 = ( (float(UV4[1])*-1)+1 , (float(UV4[0])*-1)+1 )

            NewFace.loops[3][Layer].uv = ( UV1[0] , UV1[1] )
            NewFace.loops[0][Layer].uv = ( UV2[0] , UV2[1] )
            NewFace.loops[1][Layer].uv = ( UV3[0] , UV3[1] )
            NewFace.loops[2][Layer].uv = ( UV4[0] , UV4[1] )

            return NewFace

        if float(Angle) == 0:
            UV1 = ( float(UV1[1]) , (float(UV1[0])*-1)+1 )
            UV2 = ( float(UV2[1]) , (float(UV2[0])*-1)+1 )
            UV3 = ( float(UV3[1]) , (float(UV3[0])*-1)+1 )
            UV4 = ( float(UV4[1]) , (float(UV4[0])*-1)+1 )

            NewFace.loops[3][Layer].uv = ( UV1[1] , UV1[0] )
            NewFace.loops[0][Layer].uv = ( UV2[1] , UV2[0] )
            NewFace.loops[1][Layer].uv = ( UV3[1] , UV3[0] )
            NewFace.loops[2][Layer].uv = ( UV4[1] , UV4[0] )

            return NewFace

        if float(Angle) == 1:
            UV1 = ( float(UV1[1]) , float(UV1[0]) )
            UV2 = ( float(UV2[1]) , float(UV2[0]) )
            UV3 = ( float(UV3[1]) , float(UV3[0]) )
            UV4 = ( float(UV4[1]) , float(UV4[0]) )

            NewFace.loops[3][Layer].uv = ( UV1[0] , UV1[1] )
            NewFace.loops[0][Layer].uv = ( UV2[0] , UV2[1] )
            NewFace.loops[1][Layer].uv = ( UV3[0] , UV3[1] )
            NewFace.loops[2][Layer].uv = ( UV4[0] , UV4[1] )

            return NewFace

    UV1 = ( float(UV1[0]) , (float(UV1[1])*-1)+1 )
    UV2 = ( float(UV2[0]) , (float(UV2[1])*-1)+1 )
    UV3 = ( float(UV3[0]) , (float(UV3[1])*-1)+1 )
    UV4 = ( float(UV4[0]) , (float(UV4[1])*-1)+1 )

    NewFace.loops[3][Layer].uv = ( UV1[0] , UV1[1] )
    NewFace.loops[0][Layer].uv = ( UV2[0] , UV2[1] )
    NewFace.loops[1][Layer].uv = ( UV3[0] , UV3[1] )
    NewFace.loops[2][Layer].uv = ( UV4[0] , UV4[1] )

    return NewFace

def AddMat(normalmap, obj, Tex, Color='None'):

    if Color == 'None':
        name = Tex
    else:
        name = (Tex+' ['+Color[0][0:5]+' '+Color[1][0:5]+' '+Color[2][0:5]+' '+Color[3][0:5]+']')

    bpyCount = bpy.data.materials.find(name)
    objCount = obj.data.materials.find(name)

    if(bpyCount > -1):
        # bpy.data.materials[bpyCount].use_shadeless != shadeless
        # bpy.data.materials[bpyCount].use_shadeless = shadeless

        if(objCount == -1):
            obj.data.materials.append(bpy.data.materials[bpyCount])

        return

    mat = bpy.data.materials.new(name)
    mat.use_nodes = True

    node_tree = mat.node_tree
    nodes = node_tree.nodes
    output = 'None'

    for node in nodes:
        nodes.remove(node)

    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    # bsdf.inputs[0].default_value = (float(Color[0]), float(Color[1]), float(Color[2]), float(Color[3]) if float(Color[3]) > 0 else -float(Color[3]))

    # mat.use_shadeless = shadeless
    # mtex.texture_coords = 'UV'
    mix = nodes.new("ShaderNodeMixRGB")
    mix.inputs[1].default_value = (float(Color[0]), float(Color[1]), float(Color[2]), float(Color[3]) if float(Color[3]) > 0 else -float(Color[3]))
    node_texture = nodes.new("ShaderNodeTexImage")
    node_texture.image = bpy.data.textures[bpy.data.textures.find(Tex)].image
    node_texture.projection = "BOX"
    # node_texture.coords = 'UV'
    output = nodes.new("ShaderNodeOutputMaterial")

    if normalmap:
        norm = nodes.new("ShaderNodeBump") # sorry wrapperup
        norm.inputs[0].default_value = 0.4
        node_tree.links.new(norm.inputs[2], node_texture.outputs['Alpha'])
        node_tree.links.new(norm.outputs[0], bsdf.inputs['Normal'])

    if(Color == 'None'):
        mat.diffuse_color = (0.5, 0.5, 0.5, 1)
    else:
        mat.diffuse_color = (float(Color[0]), float(Color[1]), float(Color[2]), float(Color[3]) if float(Color[3]) > 0 else -float(Color[3]))
        node_tree.links.new(bsdf.inputs['Base Color'], mix.outputs['Color'])
        node_tree.links.new(mix.inputs[0], node_texture.outputs['Alpha'])
       # node_tree.links.new(mix.inputs[1], bsdf.outputs['BSDF'])
        node_tree.links.new(mix.inputs[2], node_texture.outputs['Color'])
        node_tree.links.new(output.inputs[0], bsdf.outputs['BSDF'])

    obj.data.materials.append(mat)
    return

def SetMat(obj, NewFace, Tex, Color='None'):

    if Color == 'None':
        MCount = obj.data.materials.find(Tex)
    else:
        MCount = obj.data.materials.find(Tex+' ['+Color[0][0:5]+' '+Color[1][0:5]+' '+Color[2][0:5]+' '+Color[3][0:5]+']')

    NewFace.material_index = MCount
    return

def AddBrick(blPath, filePath, BrickName, PosX, PosY, PosZ, Angle, Color, Print, Rendering, normalmap, joinbricks, BLSCol):
    import re
    import bmesh
    pattern = re.compile("BLS_*")

    if Rendering == 0:
        return

    filepath = os.path.join(blPath + "BLS_Bricks", BrickName + '.blb')
    

    file = open(filepath)

    line = file.readline()
    line = file.readline()

    if line == 'BRICK':
        return {'Brick importer does not handle cubic type'}

    # mesh, obj
    mesh = bpy.data.meshes.new("BLS_" + BrickName + '_m') 
    obj = bpy.data.objects.new("BLS_" + BrickName, mesh)
    obj.show_transparent = True
    BLSCol.objects.link(obj)

    # bmesh
    global bmesh
    bmesh.new()
    bmesh.from_mesh(mesh)
    Layer = bmesh.loops.layers.uv.new()

    while line:
        if 'TEX:' in line:
            Tex = line.replace('TEX:','').replace('\n','')

            AddTex(blPath, Tex)

            POSH = file.readline().replace('\n','') #Position Header
            POS1 = (' '.join(file.readline().split())).split()
            POS2 = (' '.join(file.readline().split())).split()
            POS3 = (' '.join(file.readline().split())).split()
            POS4 = (' '.join(file.readline().split())).split()

            NewFace = AddFace(bmesh, POS1, POS2, POS3, POS4)

            UVH = file.readline().replace('\n','') # UV Header
            UV1 = (' '.join(file.readline().split())).split()
            UV2 = (' '.join(file.readline().split())).split()
            UV3 = (' '.join(file.readline().split())).split()
            UV4 = (' '.join(file.readline().split())).split()

            NewFace = AddUV(NewFace, UV1, UV2, UV3, UV4, Layer, Tex, Angle)

            CNH = file.readline().replace('\n','') # Color or Normal Header

            if CNH == 'COLORS:':
                C1 = (' '.join(file.readline().split())).split()
                C2 = (' '.join(file.readline().split())).split()
                C3 = (' '.join(file.readline().split())).split()
                C4 = (' '.join(file.readline().split())).split()
                H = file.readline().replace('\n','') # Normal Header

                AddMat(normalmap, obj, Tex, C1)
                SetMat(obj, NewFace, Tex, C1)
            else:
                AddMat(normalmap, obj, Tex, Color)
                SetMat(obj, NewFace, Tex, Color)
            
            

        try:
            line = file.readline()
        except StopIteration:
            break

    file.close()
    print("Created mesh for brick %s!" % BrickName)
    bmesh.to_mesh(mesh)

    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='TOGGLE')
    bpy.ops.mesh.normals_make_consistent(inside=True)
    bpy.ops.mesh.select_all(action='TOGGLE')
    bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.transform.rotate(value=((-1.5708)*float(Angle)*-1))
    bpy.ops.transform.translate(value=(float(PosX)*2, float(PosY)*2, float(PosZ)*2))

    bpy.ops.object.transform_apply(rotation=True)
    bpy.ops.object.select_all(action='TOGGLE')

    if joinbricks:
        for ob in bpy.context.visible_objects:
            if ob.type != 'MESH':
                continue

            match = pattern.match(ob.name)
            if match == None:
                print("No match for %s"  % ob.name)
            else:
                print("Found matched object %s!" % match.group())
                ob.select_set(True)

        bpy.ops.object.join()
        # deselect everything before the next iteration
        bpy.ops.object.select_all(action='DESELECT')
        
    return

def ImportBLS(blPath, filePath, joinbricks=1, normalmap=0, centerz=0):
    linecount = 0
    saveName = path_leaf(filePath).replace('.bls', '')
    print("------[BLS Importer]------")
    print("Blockland directory: %s" % blPath)
    print("Save file: %s" % filePath)
    print("Join Brick Meshes: %s" % joinbricks)
    print("Use Normal Maps: %s" % normalmap)
    print("Center Z: %s" % centerz)
    BLSCol = bpy.data.collections.new(saveName)
    bpy.context.scene.collection.children.link(BLSCol)
    file = open(filePath)
    line = file.readline() #This is a Blockland save file.  You probably shouldn't modify it cause you'll screw it up.
    DescCount = file.readline() #Description Count

    for i in range(0,int(DescCount)):
        line = file.readline()

    col = []
    if linecount == 0:
        for c in range(0,64):
            col.append(file.readline().split())
            print("Read color %s!" % c)

    while line:
        if 'Linecount' in line:
            linecount = 1
            line = file.readline()

        if '+-' not in line:
            if linecount == 1:
                SaveLine = line.replace("  "," None ").split("\"")

                NAME = SaveLine[0] #Name
                POSX = SaveLine[1].split()[0] #X 1
                POSY = SaveLine[1].split()[1] #Y 2
                POSZ = SaveLine[1].split()[2] #Z 3

                ANGLE = SaveLine[1].split()[3] #Angle 4

                BASE = SaveLine[1].split()[4] #isBaseplate 5
                COLOR = SaveLine[1].split()[5] #Color ID 6
                PRINT = SaveLine[1].split()[6] #PRINT 7

                FX = SaveLine[1].split()[7] #Color FX 8
                SHAPE = SaveLine[1].split()[8] #Shape FX 9

                RAY = SaveLine[1].split()[9] #Raycasting 10
                COL = SaveLine[1].split()[10] #Colliding 11
                REN = SaveLine[1].split()[11] #Rendering 12

                AddBrick(blPath, filePath, NAME,
                POSX, POSY, POSZ,
                ANGLE, col[int(COLOR)], PRINT, int(REN), normalmap, joinbricks, BLSCol)
        try:
            line = file.readline()
        except StopIteration:
            print("Reached end of file!")
            break

    starter = 0
    PosX = 0
    PosY = 0
    PosZ = 0
    PosX2 = 0
    PosY2 = 0
    PosZ2 = 0

    for ob in bpy.data.objects:
        if starter == 0:
            PosX = ob.location[0] + ob.dimensions[0]/2
            PosX2 = ob.location[0] - ob.dimensions[0]/2
            PosY = ob.location[1] + ob.dimensions[1]/2
            PosY2 = ob.location[1] - ob.dimensions[1]/2
            PosZ = ob.location[2] + ob.dimensions[2]/2
            PosZ2 = ob.location[2] - ob.dimensions[2]/2
            starter = 1
        else:
            if ob.location[0] + ob.dimensions[0]/2 > PosX:
                PosX = ob.location[0] + ob.dimensions[0]/2
            if ob.location[0] - ob.dimensions[0]/2 < PosX2:
                PosX2 = ob.location[0] - ob.dimensions[0]/2
            if ob.location[1] + ob.dimensions[1]/2 > PosY:
                PosY = ob.location[1] + ob.dimensions[1]/2
            if ob.location[1] - ob.dimensions[1]/2 < PosY2:
                PosY2 = ob.location[1] - ob.dimensions[1]/2
            if ob.location[2] + ob.dimensions[2]/2 > PosZ:
                PosZ = ob.location[2] + ob.dimensions[2]/2
            if ob.location[2] - ob.dimensions[2]/2 < PosZ2:
                PosZ2 = ob.location[2] - ob.dimensions[2]/2

    Center = ((PosX+PosX2)/2 ,(PosY+PosY2)/2 ,(PosZ+PosZ2)/2)


    for o in bpy.data.objects:
        o.location[0] = o.location[0] - Center[0]
        o.location[1] = o.location[1] - Center[1]

        if centerz == 1:
            o.location[2] = o.location[2] - Center[2]

    file.close()
    return {'FINISHED'}

#filePath = 'C:/Users/siba/Documents/Blockland/saves/aa.bls'
#ImportBLS(filePath)