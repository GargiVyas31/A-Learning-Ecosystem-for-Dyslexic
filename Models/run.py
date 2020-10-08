
import sys
import subprocess
import bpy
import pickle
fp=open("gem_data.dat","rb")

data=pickle.load(fp)
for i in sys.argv[5:]:
    print("i",i)
    file_loc="D:/Text_to_scene_generation-master/Text_to_scene_generation-master/models-OBJ/models/"+i
    imported_object =  bpy.ops.import_scene.obj(filepath=file_loc)
    unit=float(data["wss."+i[:-4]]["unit"][0])
    obj_object=bpy.context.selected_objects[0]
    obj_object.delta_scale=(unit,unit,unit)
    bpy.ops.export_scene.obj(filepath="modified_"+i)
    #bpy.ops.object.delete()
    print("Done")
subprocess.call(['python','Models/1_Preprocessing.py',"modified_"+sys.argv[5],"modified_"+sys.argv[6]])
print("Done after combining")
