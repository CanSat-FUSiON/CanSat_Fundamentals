import mdlreddetect as r
import os 

abspath = os.path.dirname(__file__)

if __name__ == '__main__':
    sampleimage = str(abspath)+"/images/sample_origin.jpg"
    r.main(sampleimage)