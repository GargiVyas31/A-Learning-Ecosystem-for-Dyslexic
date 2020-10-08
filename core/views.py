from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from django.conf import settings
from .forms import BookForm
from .models import Book
import PyPDF2
import docx2txt
import PIL
import requests
import json

from PIL import Image
import pytesseract
from gingerit.gingerit import GingerIt

import requests
#import language_check  #d65b3aed-7fc9-4fd7-8674-3bd2ccae55be
from PyDictionary import PyDictionary
import json
from bs4 import BeautifulSoup
from autocorrect import spell
import urllib.request
import os

import pyttsx3

class Home(TemplateView):
    template_name = 'home.html'


def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        if 'pdf' in fs.url(name):



            pdfFileObj = open('media/'+name, 'rb')

            # creating a pdf reader object
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

            # printing number of pages in pdf file
            print(pdfReader.numPages)

            # creating a page object
            pageObj = pdfReader.getPage(0)

            # extracting text from page
            content=pageObj.extractText()
            context['url'] = fs.url(name)
            context['content'] = content

            # closing the pdf file object
            pdfFileObj.close()

            return render(request, 'upload.html', context)
        else:
            # extract text
            text = docx2txt.process(uploaded_file)

            context['content'] = text
            return render(request, 'upload.html', context)
    return render(request, 'upload.html')





def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'upload_book.html', {
        'form': form
    })




class UploadBookView(CreateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('class_book_list')
    template_name = 'upload_book.html'
def dictionary(request):
    dictionary=PyDictionary()

    if request.method == 'POST':
        name1=request.POST.get('dictionary1')
        mean = dictionary.meaning(name1)

        context = {

        'name':name1,'mean':mean
        }

        return render(request,'dictionary.html',context)
    return render(request,'dictionary.html')
def correction(request):
    overlay=False
    api_key='6a8ff7d36d88957'
    language='eng'
    if request.method == 'POST':
        myfile = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        #filename="C:/Users/maitr/Desktop/django-upload-example-master/django-upload-example-master/"+uploaded_file
        #filename=type(filename)
        #print(uploaded_file)

        payload = {'isOverlayRequired': overlay,
                   'apikey': api_key,
                   'language': language,
                   }
        with open(filename, 'rb') as f:
            r = requests.post('https://api.ocr.space/parse/image',
                              files={filename: f},
                              data=payload,
                              )
        output=r.content.decode()
        ini_string = json.dumps(output)
        final_dictionary = json.loads(ini_string)
        bad_chars=['\\r']

        chg = ['\\n']

        if 'ParsedText' in final_dictionary:

            final_dictionary = final_dictionary[final_dictionary.index('ParsedText')+12:final_dictionary.index('ErrorMessage')-2]

        for i in bad_chars:
            final_dictionary = final_dictionary.replace(i,' ')

        for i in chg :

            final = final_dictionary.replace(i, ' \n')
        words=[]

        parser = GingerIt()
        words=parser.parse(final)

        #'content':final,
        return render(request,'correction.html',{'content':final,'word':words})

    return render(request,'correction.html')






def texttoimage(request):
    if request.method == 'POST':
        inp=request.POST.get('texttoimage')
        base_url="https://in.images.search.yahoo.com/search/images;_ylt=Awrxi8sw5SteW3QASRa7HAx.;_ylu=X3oDMTB0N2poMXRwBGNvbG8Dc2czBHBvcwMxBHZ0aWQDBHNlYwNwaXZz?p="+inp+"&fr2=piv-web&fr=yfp-t"
        #base_url ="https://www.google.co.in/search?q="+inp+"&source=lnms&tbm=isch&start={}"
        r = requests.get(base_url)
        soup = BeautifulSoup(r.content, 'lxml')
        #print(soup)
        li = soup.find('li', id='resitem-0')
        a=li.find('a')
        image=a.find('img').get('data-src')
        #print(image)
        urllib.request.urlretrieve(image, inp+".jpg")



        '''base_url ="http://www.google.co.in/search?tbm=isch&sxsrf=ACYBGNRl3MJpPlBzdHWExksyWkgDRbEORA%3A1579930922038&source=hp&biw=1522&bih=726&ei=KdUrXpTaPLmQ4-EPjaqX0Aw&q="+inp+""
        r = requests.get(base_url)
        soup = BeautifulSoup(r.content, 'lxml')
        p=soup.find('img').get('src')
        print(p)
        urllib.request.urlretrieve(p, inp+".jpg")'''
        return render(request,'texttoimage.html',{'image':image})
    return render(request,'texttoimage.html')
def speech(request):
    language = 'en'
    mytext="hello gargi"
    if request.method == 'POST':
        #mytext = request.POST['mytext']
        speed = request.POST['choice']
        uploaded_file = request.FILES['mytext']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        if 'pdf' in fs.url(name):



            pdfFileObj = open('media/'+name, 'rb')

            # creating a pdf reader object
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

            # printing number of pages in pdf file
            print(pdfReader.numPages)

            # creating a page object
            pageObj = pdfReader.getPage(0)

            # extracting text from page
            content=pageObj.extractText()
            #context['url'] = fs.url(name)
            #context['content'] = content

            # closing the pdf file object
            pdfFileObj.close()


        else:
            # extract text
            text = docx2txt.process(uploaded_file)


        engine = pyttsx3.init()
        rate = engine.getProperty('rate')
        volume = engine.getProperty('volume')


        if speed==50:
            print("speed"+speed)
            engine.setProperty('rate', rate+200)
            print("speedafter"+speed)
        else:
            print("speed"+speed)
            engine.setProperty('rate', rate-20)




# testing
        engine.say(text)
        #engine.say("Thank you, Geeksforgeeks")
        engine.runAndWait()

        return render(request, 'speech.html')
    return render(request, 'speech.html')
def stop(request):
        engine = pyttsx3.init()
        engine.stop()
        return render(request, 'speech.html')

def Scene(request):
    print("Hi")
    if request.method == 'POST':
        print("Scene")
        inp=request.POST.get('scene')

        os.system('python /media/gargi/FreeAgent GoFlex Drive/Text_to_scene_generation-master/Text_to_scene_generation-master/temp.py '+inp)
    return render(request,'scene.html')





'''if request.method == 'POST':
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        uploaded_file = request.FILES['image']

        # Create an image object of PIL library
        image = Image.open(uploaded_file)

        # pass image into pytesseract module
        # pytesseract is trained in many languages
        image_to_text = pytesseract.image_to_string(image, lang='eng')
        image_to_text.lower()




        text=image_to_text.split(" ")
        #words=[]

        parser = GingerIt()
        words=parser.parse(final)

        print(text)'''
