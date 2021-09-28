import os
import glob

path =  "./productsImage"
files = glob.glob(path + '/*')
for fl in files:
    os.rename(fl, os.path.join(path, os.path.basename(fl)[:-7] + '.jpg'))
    print(os.path.basename(fl))
