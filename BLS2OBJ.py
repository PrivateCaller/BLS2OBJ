#
## Based on the Blender Add-On by Ahead: https://github.com/Ahe4d/io_mesh_bls
#

from sys import argv
from os.path import splitext, basename, sep
from os.path import join as path_join
import bpy, time

def GetPureFilename(path):
    return basename(splitext(path)[0])

def AddFace(bmesh, POS1, POS2, POS3, POS4):
    POS1 = ( float(POS1[0]) , float(POS1[1]) , (float(POS1[2])/2.5) )
    POS2 = ( float(POS2[0]) , float(POS2[1]) , (float(POS2[2])/2.5) )
    POS3 = ( float(POS3[0]) , float(POS3[1]) , (float(POS3[2])/2.5) )
    POS4 = ( float(POS4[0]) , float(POS4[1]) , (float(POS4[2])/2.5) )

    Vert1 = bmesh.verts.new(POS1)
    Vert2 = bmesh.verts.new(POS2)
    Vert3 = bmesh.verts.new(POS3)
    Vert4 = bmesh.verts.new(POS4)

    return bmesh.faces.new( (Vert1,Vert2,Vert3,Vert4) )

def AddBrick(brick_name, pos_x, pos_y, pos_z, angle, collision, blb_folder, bls_collection):
    import bmesh

    if not collision:
        print(f"Brick named {brick_name} has no collision, skipping...")
        return

    with open(path_join(blb_folder, f'{brick_name}.blb'), encoding="cp1252") as file:
        line = file.readline() #Skip first line.
        if file.readline() == 'BRICK': #Second line, brick type.
            print(f"Brick #{brick_name} is unsupported cubic type, skipping...")

        #Define a mesh and bpy object for the brick, link it to the BLS collection.
        mesh = bpy.data.meshes.new(brick_name)
        obj = bpy.data.objects.new(brick_name, mesh)
        #obj.show_transparent = True
        bls_collection.objects.link(obj)

        global bmesh
        bm = bmesh.new() #This bmesh will store the faces from the .BLB file.
        bm.from_mesh(mesh)

        for line in file:
            #Found a position header in the BLB file, copy the verticies and apply them to the mesh as a face.
            #UVs and Normals are ignored to save processing time and far more importantly, RAM.
            if 'POSITION:' in line:
                POS1 = (' '.join(file.readline().split())).split()
                POS2 = (' '.join(file.readline().split())).split()
                POS3 = (' '.join(file.readline().split())).split()
                POS4 = (' '.join(file.readline().split())).split()
                AddFace(bm, POS1, POS2, POS3, POS4)

    bm.to_mesh(mesh) #Inject the faces from the bmesh into out bpy.data mesh.
    bm.free()

    #Ditching the "bpy.ops.transform" calls significantly speeds up the program, but ditching all "bpy.ops" calls
    #makes processing Pyramid drop from 2 hours and 10 minutes to 55 seconds.
    obj.rotation_mode = 'XYZ'
    obj.rotation_euler[2] += (-1.5708)*float(angle)*-1
    obj.location.x += float(pos_x)*2
    obj.location.y += float(pos_y)*2
    obj.location.z += float(pos_z)*2

    #print(f"Processed {brick_name}")

def ImportBLS(bls_file, blb_folder):
    bpy.ops.wm.read_factory_settings(use_empty=True) #Get rid of the default cube and stuff.
    bls_collection = bpy.data.collections.new(GetPureFilename(bls_file))
    scene = bpy.context.scene
    scene.collection.children.link(bls_collection)

    with open(bls_file, encoding="cp1252") as file:
        file.readline() #This is a Blockland save file.  You probably shouldn't modify it cause you'll screw it up.
        for _ in range(0,int(file.readline())): #Read the number of lines in the description, then skip them.
            file.readline()
        for _ in range(0,64): #Colorset declaration, skip this as well.
            file.readline()

        #We've reached the Linecount. Read it, then process that many bricks.
        for _ in range(0, int(file.readline().split()[1])): 
            line = file.readline()
            if not line.startswith('+-'):
                SaveLine = line.replace("  "," None ").split("\"")
                INFO = SaveLine[1].split()

                NAME = SaveLine[0] #Name
                POSX = INFO[0] #X 1
                POSY = INFO[1] #Y 2
                POSZ = INFO[2] #Z 3

                ANGLE = INFO[3] #Angle 4
                COL = INFO[10] #Colliding 11

                AddBrick(NAME, POSX, POSY, POSZ, ANGLE, COL, blb_folder, bls_collection)

    #Not sure what all this stuff does, but I assume it's moving stuff into position.
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

def run(bls_file, blb_folder, output_folder):
    start_time = time.time()
    ImportBLS(bls_file, blb_folder)
    output_obj = path_join(output_folder,f'{GetPureFilename(bls_file)}.obj')

    bpy.ops.wm.obj_export(filepath=output_obj, check_existing=False, export_normals=False, export_uv=False, export_materials=False, export_triangulated_mesh=True)
    print(f'.OBJ creation time (seconds): {time.time() - start_time}')
    return output_obj

if __name__ == "__main__":
    if "--" in argv: #Being run with standalone Blender argument, get Python args after the "--" delimiter.
        args = argv[argv.index("--"):]
        run(args[1], args[2], args[3])
    else: #Being run with Blender as a Python module, get args after the filename.
        run(argv[1], argv[2], argv[3])
