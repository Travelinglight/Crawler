import re
import requests
import shutil
import time

def savePic(url):
    print '////////////////////////////////////'
    start_time = time.time()
    dup = 'image' + re.findall(r'/[^/]*$', url)[0]
    pattern = '\.(jpg|JPG|jpeg|JPEG|png|PNG|tif|TIF|tiff|TIFF|bmp|BMP)'
    if re.findall(pattern, dup) == []:
        return
    elapsed_time = time.time() - start_time
    print '/ regexp: ' + str(elapsed_time)
    start_time = time.time()
    response = requests.get(url, stream=True)
    elapsed_time = time.time() - start_time
    print '/ request: ' + str(elapsed_time)
    start_time = time.time()
    with open(dup, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    elapsed_time = time.time() - start_time
    print '/ write: ' + str(elapsed_time)
    del response
