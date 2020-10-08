import spacy
import neuralcoref
import csv
import nltk
import json,os
import time

nlp = spacy.load("en_core_web_sm")
nlp = spacy.load('en')
neuralcoref.add_to_pipe(nlp)
doc = nlp("The ball is underneath the table and it is beside the cat")
nouns =[]

visited = []
landmark = []
prep = []
trajector = []

with open('Spatial_Relation_test.txt','w'): pass


def dfs(visited, graph, node):

    global landmark, prep, trajector

    if node not in visited:
        if node.dep_ is "prep" :
            prep.append(node.text)

        if node.dep_ is "pobj":
            landmark.append(node.text)
            nouns.append(node.text)
        if node.dep_ is "nsubj" :
            trajector.append(node.text)
            nouns.append(node.text)

        if node.dep_ is "attr":
            trajector.append(node.text)
            nouns.append(node.text)
        if  node.dep_ is "nsubjpass" :
            trajector.append(node.text)
            nouns.append(node.text)

        visited.append(node)

        for neighbour in node.children:
            dfs(visited, graph, neighbour)

def specialcase1(string):
    global landmark, prep, trajector

    for t in nlp(string):
        if t.dep_ is "nsubj" or t.dep_ is "attr" or t.dep_ is "nsubjpass":
            trajector.append(t.text)
            nouns.append(t.text)
        if t.dep_ is "pobj":
            landmark.append(t.text)
            nouns.append(t.text)
    prep = landmark[0]
    landmark = landmark[-1]
    with open('Spatial_Relation_test.txt', 'a', newline='') as file:
            S=trajector[0]+" "+prep[0]+" "+landmark[0]+"."
            file.write(S)

    # print("Trajector",trajector)
    # print("Prep",prep)
    # print("Landmark",landmark)


def first_call(string):
    # print("1")
    global prep, landmark, trajector
    trajector =[]
    prep= []
    landmark =[]

    if "left" in string or "right" in string or "front" in string or "behind" in string:
        specialcase1(string)
    else:
        graph = nlp(string)
        for t in range(len(graph)):
            if graph[t].dep_ ==  "ROOT" :
                root = graph[t]
                break
        dfs(visited, graph, root)
        with open('Spatial_Relation_test.txt', 'a', newline='') as file:
            S=trajector[0]+" "+prep[0]+" "+landmark[0]+"."
            file.write(S)
        print("Trajector",trajector)
        print("Prep",prep)
        print("Landmark",landmark)

def start(doc):
    # doc = nlp("The book is on the table and a pen is lying beside it. A cake is on the desk and a bottle of salt is placed beside it.")
    if doc._.has_coref:
        # print(type(doc._.coref_resolved))
        print(doc._.coref_resolved)
        doc = doc._.coref_resolved

    sentences = str(doc).split(". ")

    # print("Sentences",sentences)
    for string in sentences:
        # print("HERE",string)
        if "and" in string:
            p = string.split("and")
            # print("p0",p[0])
            # print("p1",p[1])

            if "is" in p[0] and "is" in p[1]:
                s1 = str(p[0])
                s2 = str(p[1])
                # print(s1)
                # print(s2)
                first_call(s1)
                # print("NEXT")
                first_call(s2)

            elif "is" in p[1]:
                s1 = p[1].split("is")
                s2 = str(p[0])+"is"+str(s1[1])
                s3 = p[1]
                # print(s2)
                # print(s3)
                first_call(s2)
                # print("NEXT")
                first_call(s3)

            else:
                s1=p[0].split("is")
                s2 = str(s1[0])+ "is" + str(p[1])
                s3 = p[0]
                # print(s2)
                # print(s3)
                first_call(s2)
                # print("NEXT")
                first_call(s3)

        else:
            first_call(string)
# start()
'''with open('NLP2_test.txt', "r") as f:
    for line in f:
        # print("Line",line)
        doc = nlp(line)
        start(doc)'''
start(doc)
noun_extracted=list(set(nouns))
#print(noun)

#nouns=open('Nouns1.txt',"r")
#n=list(nouns.read().split(','))
#print(n)
with open("new_nouns_ids.txt", 'r') as f:
    d = json.load(f)
noun_id=open("nouns_and_IDs.txt",'w')
#nouns=['cake','tabble']
ids=[]
sim={}
# for i in noun_extracted:
#     print("HEREEEEE")
#     try:
#         ids.append(d[i])
#         ni=i+" "+d[i]
#         noun_id.write(ni)
#         noun_id.write("\n")
#     except:
#         for j in d:
#             cos=nltk.edit_distance(i,j)
#             sim[cos]=j
#
#         simi=sorted(sim)
#         sid=sim[simi[0]]
#         ids.append(d[sid])
#         ni=j+" "+d[sid]
#         noun_id.write(ni)
#         noun_id.write("\n")
    # noun_id.write(ni)
    # noun_id.write("\n")

for i in noun_extracted:
    print('HERRRRRR')
    if i in d:
        ids.append(d[i])
        ni=i+" "+d[i]
        noun_id.write(ni)
        noun_id.write("\n")
    else:
        for j in d:
            cos=nltk.edit_distance(i,j)
            sim[cos]=j

        simi=sorted(sim)
        sid=sim[simi[0]]
        ids.append(d[sid])
        ni=j+" "+d[sid]
        noun_id.write(ni)
        noun_id.write("\n")

print(ids)
time.sleep(10)
os.system('blender blank.blend')
#--python blender_modified_room2.py')
