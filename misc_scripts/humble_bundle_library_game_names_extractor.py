# try:
#     import Image
# except ImportError:
#     from PIL import Image
# import pytesseract
#
# # pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
# # Include the above line, if you don't have tesseract executable in your PATH
# # Example tesseract_cmd: 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'
#
# print(pytesseract.image_to_string(Image.open('/home/j/Temp/pic2')))
# print(pytesseract.image_to_string(Image.open('/home/j/Temp/out1')))
# print(pytesseract.image_to_string(Image.open('test-european.jpg'), lang='fra'))

from tesserocr import PyTessBaseAPI

images = ['home/j/Temp/pic2']

with PyTessBaseAPI() as api:
    for img in images:
        api.SetImageFile(img)
        print(api.GetUTF8Text())
        print(api.AllWordConfidences())
# api is automatically finalized when used in a with-statement (context manager).
# otherwise api.End() should be explicitly called when it's no longer needed.