import struct
import imghdr
import os
import string
import csv
import collections

rootdir = '/Users/marco/code/resized/BlueText_resized/'
out_csv = r"/Users/marco/code/resized/csv/csv/"
path = "http://ec2-54-162-126-13.compute-1.amazonaws.com"
input_city='Pittsburgh'
def get_image_size(fname):
    '''Determine the image type of fhandle and return its size.
    from draco'''
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            return
        if imghdr.what(fname) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return
            width, height = struct.unpack('>ii', head[16:24])
        elif imghdr.what(fname) == 'gif':
            width, height = struct.unpack('<HH', head[6:10])
        elif imghdr.what(fname) == 'jpeg':
            try:
                fhandle.seek(0) # Read 0xff next
                size = 2
                ftype = 0
                while not 0xc0 <= ftype <= 0xcf:
                    fhandle.seek(size, 1)
                    byte = fhandle.read(1)
                    while ord(byte) == 0xff:
                        byte = fhandle.read(1)
                    ftype = ord(byte)
                    size = struct.unpack('>H', fhandle.read(2))[0] - 2
                # We are at a SOFn block
                fhandle.seek(1, 1)  # Skip `precision' byte.
                height, width = struct.unpack('>HH', fhandle.read(4))
            except Exception: #IGNORE:W0703
                return
        else:
            return
        return width, height
    
i = 1
current_dir = ''
lines = []
group_lines = []

for subdir, dirs, files in os.walk(rootdir):
	#print(subdir)
	city_name= subdir.split('/')[6].split('_')[0] #get_city_name(subdir)
	
	if city_name != input_city:
		
		continue
	
	for file in files:
		if "jpg" not in file:
			continue

		if "thumb" in subdir: 
			continue

		directory = subdir.split('/')[-1]
		print(current_dir)
		if current_dir != directory:
			if current_dir != '':
				with open(out_csv + "group_" + current_dir.split(sep='\\')[1].split(sep="_")[0] + ".csv", 'w') as f:  			
					w = csv.writer(f)
					w.writerow(["order","set_key","file_path","thumbnail","width","height"])

					for line in lines:
						w.writerow(line)

			lines = []
			current_dir = directory
			i=1
			city = current_dir.split(sep='\\')[0].split(sep="_")[0]
			group_lines.append([city, city + " Redlining Documents", city + " Redlining Documents from " + current_dir, path + ":3000/dcic_docs/" + os.path.join(directory, file), path + ":3000", 2])            

		width, height = get_image_size(os.path.join(subdir, file))
		lines.append([i-1, city, path + ":3000/dcic_docs/" + os.path.join(directory, file), path + ":3000/dcic_docs/" + directory + "/thumb/" + file, str(width), str(height)])            
		i += 1

		if city == 'Warren':
			with open(out_csv + "group_" + current_dir.split(sep='\\')[1].split(sep="_")[0] + ".csv", 'w') as f:        
				w = csv.writer(f)
				w.writerow(["order","set_key","file_path","thumbnail","width","height"])

				for line in lines:
					w.writerow(line)


with open(out_csv + "groups.csv", 'w') as f:        
    w = csv.writer(f)
    w.writerow(["key","name","description","cover_image_url","external_url","retire_count"])
    for line in group_lines:
        w.writerow(line)