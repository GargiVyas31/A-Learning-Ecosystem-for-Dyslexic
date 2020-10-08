# File created

fin = open("new_meta1.txt", 'r')
fout = open("unit.txt", 'w')


line = fin.readline()
# print(line)
count = 0
# num = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
while count < 12287:
# while count < 10:
	line = fin.readline()
	line = line.split('\t')
	# count+=1
	print(count)
	if(len(line[6]) > 1):
		# print(line[0], line[15])
		fout.write(line[0])
		fout.write('\t')
		for x in line[6]:
			if x != '"':
				x = x.lower()
				fout.write(x)
	else:
		fout.write(line[0])
		fout.write('\t')
		fout.write("*")
	fout.write('\n')
	# check = 0
	# check1 = 0
	# category = ""
	# for i in range(len(line)):
	# 	if line[i] == ',':
	# 		check += 1
	# 		continue
	# 	elif check > 0:
	# 		if line[i+1] == '"':
	# 			category = category + line[i]
	# 			break
	# 		elif line[i+1] == 'n':
	# 			if line[i+2] in num:
	# 				print("check1")
	# 				break
	# 		else:
	# 			category = category + line[i]

	# print(category)
	count += 1

print("DATA WRITTEN")
fin.close()
fout.close()