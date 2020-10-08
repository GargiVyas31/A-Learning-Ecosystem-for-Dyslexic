import bpy
import pickle

print("File blender_scene.py called")

fp_data = open("gem_data.dat", 'rb')
fin = open("extracted_models.txt", 'r')
fnouns_id = open("nouns_and_IDs.txt", 'r')
fsent = open("Sentence.txt", 'r')
fout = open("Prep_nouns.txt1", 'w')

data = pickle.load(fp_data)

models = fin.read()
models = models.split(' ')
print(models)

line1 = fnouns_id.readline().split(" ")
nouns = list()
ids = list()
for j in range(len(models)-1):
	print(line1)
	nouns.append(line1[0])
	ids.append(line1[1])
	line1 = fnouns_id.readline().split(" ")
print("\n\n\n\n")
print(nouns)
print(ids)
print("\n\n\n\n")

placement_prepositions = {'right':['right'], 'up':['above', 'on', 'top'], 'left':['left'], 'down':['beneath', 'below', 'under']}
prepositions = ['right', 'left', 'up', 'down', 'above', 'below', 'on', 'beneath', 'top', 'front', 'back']

sentence = fsent.read().split(' ')
print(sentence)

prev_noun = ''
pres_noun = ''
last_prep = ''
prep_mapping = dict()
for n in range(len(sentence)):
	print(sentence[n])
	if sentence[n] in nouns:
		prev_noun = sentence[n]
		# pres_noun = sentence[n]
		break
print(n)
# print(pres_noun)
for p in range(n+1, len(sentence)):
	if sentence[p] in prepositions:
		for j in range(p+1, len(sentence)):
			if sentence[j] in nouns:
				print(sentence[j], sentence[p], prev_noun)
				break
	elif sentence[p] in nouns:
		prev_noun = sentence[p]
	# 	# last_prep = sentence[p]
	# 	# prep_mapping[last_prep].append([])
	# 	print(prev_noun, sentence[p], end = ' ')
	# 	fout.write(prev_noun + ' ' + sentence[p] + ' ')
	# elif sentence[p] in nouns:
	# 	print(sentence[p])
	# 	fout.write(sentence[p] + '\n')
	# 	prev_noun = sentence[p]

fout.close()

path = "/media/gargi/FreeAgent GoFlex Drive/Text_to_scene_generation-master/Text_to_scene_generation-master/models-OBJ/models/"
x_dims_count = 0
y_dims_count = 0
z_dims_count = 0

fnouns_preps = open("Prep_nouns.txt", 'r')  # change
data1 = fnouns_preps.read()
data1 = data1.split('\n')

new_models = list()
placed_models = dict()
print("\n\n\n\n")
data1.pop()
print(data1)
for i in data1:
	line2 = i.split(' ')
	print(line2)
	# ----------- RIGHT PLACEMENT ------------
	if line2[1] == 'right':
		print("test")
		id1 = ids[nouns.index(line2[0])]
		id1 = id1.strip()
		id2 = ids[nouns.index(line2[2])]
		id2 = id2.strip()
		# new_models.append(id1)
		# new_models.append(id2)
		# placed_models[id1] = list()
		# placed_models[id2] = list()
		full_id = 'wss.' + id1
		dims = data[full_id]['dims']
		rotation_info = data[full_id]['up']
		unit = float(data[full_id]['unit'][0])
		x_rot = 0
		y_rot = 0
		z_rot = 0
		model_id = id1 + '.obj'
		model_path = path + model_id
		# imported_object = bpy.ops.import_scene.obj(filepath=model_path)
		# print("Object", model_id, "imported")
		# obj_object = bpy.context.selected_objects[0]
		# # obj_object.location = (x_scale/1000,y_scale/1000,0)
		# obj_object.delta_scale = (unit, unit, unit)
		# obj_object.rotation_euler = (x_rot, y_rot, z_rot)
		# bpy.ops.object.origin_set(type = 'GEOMETRY_ORIGIN')
		if id1 not in placed_models:
			imported_object = bpy.ops.import_scene.obj(filepath=model_path)
			print("Object", model_id, "imported")
			obj_object = bpy.context.selected_objects[0]
			# obj_object.location = (x_scale/1000,y_scale/1000,0)
			obj_object.delta_scale = (unit, unit, unit)
			obj_object.rotation_euler = (x_rot, y_rot, z_rot)
			bpy.ops.object.origin_set(type = 'GEOMETRY_ORIGIN')
			obj_object.location = (0, 0, 0)
			x_dims_count += (float(dims[0]))/200
			y_dims_count += (float(dims[1]))/200
			z_dims_count += (float(dims[2]))/200
			placed_models[id1] = (0, 0, 0)
		else:
			print("\n\nMODEL", id1, "ALREADY IMPORTED\n\n")
			x_dims_count = placed_models[id1][0] + (float(dims[0]))/200
			y_dims_count = placed_models[id1][1] + (float(dims[1]))/200
			z_dims_count = placed_models[id1][2] + (float(dims[2]))/200

		full_id = 'wss.' + id2
		dims = data[full_id]['dims']
		rotation_info = data[full_id]['up']
		unit = float(data[full_id]['unit'][0])
		x_rot = 0
		y_rot = 0
		z_rot = 0
		model_id = id2 + '.obj'
		model_path = path + model_id
		imported_object = bpy.ops.import_scene.obj(filepath=model_path)
		print("Object", model_id, "imported")
		obj_object = bpy.context.selected_objects[0]
		# obj_object.location = (x_scale/1000,y_scale/1000,0)
		obj_object.delta_scale = (unit, unit, unit)
		obj_object.rotation_euler = (x_rot, y_rot, z_rot)
		bpy.ops.object.origin_set(type = 'GEOMETRY_ORIGIN')
		x = x_dims_count + (float(dims[0]))/200
		obj_object.location = (x, 0, 0)
		x_dims_count += (float(dims[0]))/100
		placed_models[id2] = (x, 0, 0)

		# DO NOT DELETE THE FOLLOWING CODE

		# for i in range(len(new_models)):
		# 	# fdims = open("aligned_dims1.txt", 'r')
		# 	# line = fdims.readline().split()
		# 	# while line[0][4:] != models[i]:
		# 	# 	line = fdims.readline().split()
		# 	# print(line[1])
		# 	# dims = line[1].split('\\,')
		# 	full_id = 'wss.' + new_models[i]
		# 	dims = data[full_id]['dims']
		# 	rotation_info = data[full_id]['up']
		# 	unit = float(data[full_id]['unit'][0])
		# 	print(dims)
		# 	print(rotation_info)
		# 	print(unit)
		# 	x_dims = float(dims[0])*unit
		# 	y_dims = float(dims[1])*unit
		# 	z_dims = float(dims[2])*unit
		# 	if '*' in rotation_info:
		# 		x_rot = 0
		# 		y_rot = 0
		# 		z_rot = 0
		# 	# Change the following to account for rotation
		# 	else:   # Normal vector to be converted to euler here
		# 		x_rot = 0
		# 		y_rot = 0
		# 		z_rot = 0
		# 	print(x_dims, y_dims, z_dims)
		# 	print(x_rot, y_rot, z_rot)
		# 	# print("Command went into for loop")
		# 	model_id = new_models[i] + '.obj'
		# 	model_path = path + model_id
		# 	imported_object = bpy.ops.import_scene.obj(filepath=model_path)
		# 	print("Object", model_id, "imported")
		# 	obj_object = bpy.context.selected_objects[0]
		# 	# obj_object.location = (x_scale/1000,y_scale/1000,0)
		# 	obj_object.delta_scale = (unit, unit, unit)
		# 	obj_object.rotation_euler = (x_rot, y_rot, z_rot)

			# saved_location = bpy.context.scene.cursor_location # change
			# bpy.context.scene.cursor_location = (0.0,0.0,0.0) # change
			# bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

			# bpy.ops.object.origin_set(type = 'GEOMETRY_ORIGIN')
			# if i>0:
			# 	# if i==1:
			# 	# y = y_dims_count + y_dims/2
			# 	# obj_object.location = (0, y, 0)
			# 	# y_dims_count += y_dims + 0.3
			# 	# print("Object", i, "location = 0", y, "0\n\n")
			# 	x = x_dims_count + (float(dims[0]))/200
			# 	obj_object.location = (x, 0, 0)

			# 	x_dims_count += (float(dims[0]))/100


			# # else:
			# # 	x_dims_count += (x_dims/2) + 0.3
			# # 	y_dims_count += (y_dims) + 0.3
			# # 	z_dims_count += (z_dims/2) + 0.3

			# else:
			# 	if
			# 	x_dims_count += (float(dims[0]))/200
			# 	y_dims_count += (float(dims[1]))/200
			# 	z_dims_count += (float(dims[2]))/200

print(placed_models)

fin.close()
fp_data.close()
