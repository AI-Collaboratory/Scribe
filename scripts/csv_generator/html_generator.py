import struct
import imghdr
import os
import string
import csv
import collections

rootdir = '/Users/myeong/git/DCIC_text/BlueText'
out_csv = r"/Users/myeong/git/DCIC_text/html/"

    
i = 1
current_dir = ''
lines = []

for subdir, dirs, files in os.walk(rootdir):
    for file in files:     
        if "jpg" not in file:
            continue
        
        if "thumb" in subdir: 
            continue

        directory = subdir.split('/')[-1]
        
        if current_dir != directory:    
            if current_dir != '':                
                with open(out_csv + "group_" + current_dir.split(sep='_')[0] + ".html", 'w') as f:        
#                     w = csv.writer(f)
                    
                    for line in lines:
#                         w.writerow(line)
                        f.write(line)
                    
            lines = []
            current_dir = directory
            i=1
            city = current_dir.split(sep='_')[0]          
        
        lines.append("<img class=preserve src=\"../../dcic_docs/" + os.path.join(directory, file) + "\" rel=group1 />")            
        i += 1
        
        if city == 'Warren':
            with open(out_csv + "group_" + current_dir.split(sep='_')[0] + ".html", 'w') as f:        
#                 w = csv.writer(f)                
                
                for line in lines:
                    f.write(line)


