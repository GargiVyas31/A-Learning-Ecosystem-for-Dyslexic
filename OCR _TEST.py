import requests
import json


def ocr_space_file(filename, overlay=False, api_key='6a8ff7d36d88957', language='eng'):
    """ OCR.space API request with local file.
        Python3.5 - not tested on 2.7
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.content.decode()


def ocr_space_url(url, overlay=False, api_key='6a8ff7d36d88957', language='eng'):
    """ OCR.space API request with remote file.
        Python3.5 - not tested on 2.7
    :param url: Image url.
    :param overlay: Is OCR.space overlay required in your response.
                    Defaults to False.
    :param api_key: OCR.space API key.
                    Defaults to 'helloworld'.
    :param language: Language code to be used in OCR.
                    List of available language codes can be found on https://ocr.space/OCRAPI
                    Defaults to 'en'.
    :return: Result in JSON format.
    """

    payload = {'url': url,
               'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    r = requests.post('https://api.ocr.space/parse/image',
                      data=payload,
                      )
    return r.content.decode()


# Use examples:
test_file = ocr_space_file(filename='ocr.jpg', language='pol')
#test_url = ocr_space_url(url='http://i.imgur.com/31d5L5y.jpg')

print(test_file)

# print(test_url)
print(test_file[19])
ini_string = json.dumps(test_file)
print ("initial 1st dictionary", ini_string)
print ("type of ini_object", type(ini_string))

print("\n ")
final_dictionary = json.loads(ini_string)
print ("final dictionary", str(final_dictionary))
print ("type of final_dictionary", type(final_dictionary))

bad_chars=['\\r']

chg = ['\\n']

if 'ParsedText' in final_dictionary:
    print("hi")
    print(final_dictionary.index('ParsedText'))
    print(final_dictionary.index('ErrorMessage'))
    print(final_dictionary[final_dictionary.index('ParsedText')+12:final_dictionary.index('ErrorMessage')-2])
    final_dictionary = final_dictionary[final_dictionary.index('ParsedText')+12:final_dictionary.index('ErrorMessage')-2]

for i in bad_chars:
    final_dictionary = final_dictionary.replace(i,' ')
   
for i in chg :
    final = final_dictionary.replace(i, ' \n')

print("\n")
print(final)