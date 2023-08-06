name= "rnest_test"
from PIL import Image
import requests
from io import BytesIO

response = requests.get('https://dejartehuellaconunseisyuncuatro.files.wordpress.com/2014/02/img_20140212_194129.jpg')
img = Image.open(BytesIO(response.content))

def tedigo():
    a=6
    b=4
    print('Con un {0} y un {1}, la cara de tu retrato'.format(a,b))

def tepinto():
    return img

tedigo()
tepinto()