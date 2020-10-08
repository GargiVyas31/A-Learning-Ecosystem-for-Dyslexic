# file created
def chint(s):
    try:
        return type(int(s))==int
    except ValueError:
        return False

import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import subprocess
import os,sys
import random
import pickle
from subprocess import call


fp = open("data1.dat", 'rb')
d1 = pickle.load(fp)    ## d1 is a dict

def get_syn_diff(modelID, adjectives):
	fdata = open("data1.dat", 'rb')
	d1 = pickle.load(fdata)    ## d1 is a dict
	tags = list()
	for i in d1:
		if i[4:] == modelID:
			for x in d1[i]['tag']:
				tags.append(x)
			break
	count = 0
	score = 0
	for i in tags:
		print(i)
		tags = i.split()
		for i1 in tags:
			for j in adjectives:
				try:
					w1 = wordnet.synsets(i1)[0]
					w2 = wordnet.synsets(j)[0]
					score = score + w1.wup_similarity(w2)
					count += 1
				except:
					count += 1
	fdata.close()
	if count == 0:
		count += 1
	avg_score = score/count
	return avg_score

print("here")
fp=open("Nouns1.txt",'r')
fsent = open("Sentence.txt", 'w')

nouns=fp.read().split(',')
adj=fp.read().split()
inputt=sys.argv[1:]
print("input",inputt)
#sent=" "
sent=' '.join(str(elem) for elem in inputt)



print("sent",sent)
#sent=input("Enter the Sentence--").lower()
fsent.write(sent)
fsent.close()
new_sent=""
for i in sent.split():
    val=i
    # if not val in stopwords.words('english'):
    new_sent+=val + " "
l=new_sent.split()
lem=WordNetLemmatizer()
l=[lem.lemmatize(word) for word in l]
print(l)
# d=dict()
# count=0
# z=[1]
# while (count!=(len(l))):
#     if not l[count] in nouns:
#         if chint(l[count]):
#             z[0]=int(l[count])
#         else:
#             z.append(l[count])
#     if l[count] in nouns:
#         print(z)
#         if not l[count] in d:
#             d[l[count]]=z
#             print("done")
#         else:
#             d[l[count]][0] +=z[0]
#             d[l[count]].extend(z[1:])
#         z=[1]
#     count+=1

## Changes from here..
d = dict()
mapping = list()
for k in range(len(l)):
	if l[k] in nouns:
		if (k+1 < len(l)) and (l[k+1] in nouns):
			if l[k] not in stopwords.words('english'):
				mapping.append(l[k])
		else:
			d[l[k]] = mapping
			mapping = list()
	else:
		if l[k] not in stopwords.words('english'):
			mapping.append(l[k])


## Changes till here..

print(d)
extracted_nouns = list()
for i in d:
	print(i)
	extracted_nouns.append(i)
fp.close()
print("here1")
fin = open("Nouns1.txt", 'r')
fcsv = open("created_database_category1.txt", 'r')
ftags = open("created_database_tags1.txt", 'r')

line = fcsv.readline().split('\t')
# print(line[1])
categories = line[1].split(',')
# print(categories)

count = 0

# nouns = fin.read().split('\n')
# print(nouns)

nouns_model_id = dict()

while count < 9683:
	line = fcsv.readline().split('\t')
	# print(line[1])
	categories = line[1].split(',')
	categories[-1] = categories[-1].strip()
	categories=[lem.lemmatize(word) for word in categories]

	for x in extracted_nouns:
		# print("check 1")
		if x in categories:
			# print("check 2")
			# print(x, "found in model ID", line[0][4:])
			if x not in nouns_model_id:
				nouns_model_id[x] = list()
				nouns_model_id[x].append(line[0][4:])
			else:
				nouns_model_id[x].append(line[0][4:])
	# print(count, categories)

	count+=1
# print(nouns_model_id)

model_ids = list()

for i in nouns_model_id:
	for j in nouns_model_id[i]:
		model_ids.append(j)


# print("\n\n MODEL IDs\n\n")
# print(model_ids)
# count1 = 0
# import pickle
# fp = open("data1.dat", 'rb')
# d1 = pickle.load(fp)    ## d1 is a dict

for i in d1:
	if i[4:] in model_ids:
		print(i, ":", end = ' ')
		for x in d1[i]['tag']:
			print(x, end = ' ')

		print('\n')
# print(count1)
suitable_models = dict()
for i in d:
	suitable_models[i] = list()
	best_model = nouns_model_id[i][0]
	best_score = get_syn_diff(nouns_model_id[i][0], d[i])
	for j in nouns_model_id[i]:
		score = get_syn_diff(j, d[i])
		if score > best_score:
			best_model = j
	suitable_models[i].append(best_model)

print("\n\n\n\n")

for x in suitable_models:
	print(x, ":", suitable_models[x])

print("here2")
fout = open("extracted_models.txt", 'w')
fout1 = open("nouns_and_IDs.txt", 'w')
models_path = "/media/gargi/FreeAgent GoFlex Drive/Text_to_scene_generation-master/Text_to_scene_generation-master/models-OBJ/models/"
for i in suitable_models:
	model_id = suitable_models[i][0]
	print(model_id)
	fout.write(model_id)
	fout.write(" ")
	fout1.write(i)
	fout1.write(" ")
	fout1.write(model_id)
	fout1.write("\n")
	# os.system("cd " + models_path + '\n' + 'open ' + model_id + '.obj')

fout1.close()
fout.close()
print("here3ss")
os.system('blender blank.blend --python blender_modified_room.py')
'''calllist=[c]
call(c)'''
fin.close()
fcsv.close()
ftags.close()
fp.close()
# fout.close()

'''
from nltk.corpus import wordnet
wordnet.synsets("hello")
wordnet.synset("hi.n.01")
print(w1.wup_similarity(w2))
'''

'''
import pickle
fp = open("data.dat", 'rb')
d = pickle.load(fp)    ## d is a dict
'''
