import io
import requests
import re
import time
import pyscreenshot as ImageGrab

from google.cloud import vision
from google.cloud.vision import types
from PIL import Image
from collections import Counter


class TriviaHQBot(object):
    def __init__(self, path):
        self.path = path

    def detect_text(self, path):
        """Detects text in the file."""
        client = vision.ImageAnnotatorClient()

        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)

        response = client.text_detection(image=image)
        texts = response.text_annotations
        return texts[0].description if texts else ''

    def crop(self, coords, saved_location):
        """
        @param image_path: The path to the image to edit
        @param coords: A tuple of x/y coordinates (x1, y1, x2, y2)
        @param saved_location: Path to save the cropped image
        """
        image_obj = Image.open(self.path)
        cropped_image = image_obj.crop(coords)
        cropped_image.save(saved_location)

    def proccessCroppedPhoto(self, coords, name):
        self.crop(coords, name)
        return self.detect_text(name)

    def answerQuestion(self):
        start = time.time()
        question = self.proccessCroppedPhoto((10, 234, 948, 704), 'question.jpg').replace('\n', " ")
        answers = self.proccessCroppedPhoto((22, 724, 938, 1200), 'answer.jpg').split('\n')[:-1]
        print(question)
        print(answers)
        googleResult = self.googleSearch(question)
        for answer in answers:
            print(answer, googleResult.count(answer.lower()))
        print('It took', time.time() - start, 'seconds to run.')

    def googleSearch(self, param):
        payload = {'key': 'ENTER KEY HERE', 'cx': 'ENTER KEY HERE', 'q': param}
        r = requests.get('https://www.googleapis.com/customsearch/v1', params=payload)
        result = r.json()['items']
        resultStrings = ''
        for i in result:
            if i['title']:
                resultStrings += i['title'].replace('\n', ' ').lower()
            if i['snippet']:
                resultStrings += i['snippet'].replace('\n', ' ').lower()
        return resultStrings



if __name__ == '__main__':
    im = ImageGrab.grab(bbox=(940,0,1440,899)).convert("RGB") # X1,Y1,X2,Y2
    im.save('james1243.jpg')
    bot = TriviaHQBot('james1243.jpg')
    bot.answerQuestion()
