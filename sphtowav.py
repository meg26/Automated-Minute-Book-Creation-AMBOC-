import os
from sphfile import SPHFile


path = 'F:\\TEDLIUM_release1\\TEDLIUM_release1\\test\\sph\\'  # Path of folder containing .sph files

folder = os.fsencode(path)

filenames = []
folderpath = []
outputfile = []

for file in os.listdir(folder):
    filename = os.fsdecode(file)
    if filename.endswith( ('.sph') ): # whatever file types you're using...
        filenames.append(filename)

length = int(len(filenames))
print(length)


for i in range(length):
    fpath = os.path.join(path+filenames[i])
    folderpath.append(fpath)
    outpath = os.path.join(filenames[i][:-4]+".wav")
    outputfile.append(outpath)

j=0
for i in range(length):
    sph =SPHFile(folderpath[i])
    sph.write_wav(outputfile[i], 20.00, 320.00 ) # Customize the period of time to crop
    if(i%100==0):
        print(length-i);
print("All Done!")
