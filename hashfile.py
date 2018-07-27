#!/usr/bin/env python

# creates a filename using various fields in a CSV
# strips filename of common words and special characters


import csv
import sys
import os
import re
import urllib2
import shutil

import hashlib



allowedfmt = [ 'jpg', 'jpeg', 'wav', 'png', 'gif',
               'mp4', 'mpg', 'mpeg', 'wmv',
               'pdf', 'mp3', 'wav'] 



def hash_a_file(filename):
    
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()

    try:
        with open(filename, 'rb') as afile:
            buf = afile.read(BLOCKSIZE)
            while len(buf) > 0:
                hasher.update(buf)
                buf = afile.read(BLOCKSIZE)

        fhash = hasher.hexdigest()
    except EnvironmentError:
        # parent of IOError, OSError *and* WindowsError where available
       fhash = 'Error' 
       print 'Error, not found: %s' % filename
       
        
    #print(fhash)

    return fhash

# 1 Status
# 2 Comments/ Suggestion
# 3 Local URL
# 4 SHA1 hash
# 5 Org/Dup. Check
# 6 YYYY
# 7 Source ID
# 8 Accession Number
# 9 Internal ID / Seq ID
# 10 Unique Resource ID
# 11 Title
# 12 Org/Dup. Check
# 13 Creator
# 14 Date.Created
# 15 Coverage.Temporal
# 16 Coverage.Spatial
# 17 Publisher
# 18 Description
# 19 Language
# 20 File type
# 21 Content Type
# 22 Format
# 23 Copyright
# 24 Keyword/ Subject




def hashedfile(row):

    global allowedfmt
    
    # replace % characters in URL eg %20 by space
    urlpath = urllib2.unquote(row[3])  
    urlprefix = "http://10.129.50.5/nvli/data/"
    
    # Strip urlprefix to find the relative path in local partition
    srcfile = re.sub(urlprefix,'',urlpath)
    
    # the local partition
    srcdir = "/NFSMount/SV-Patel_Data/nvli"
    srcpath = '/'.join([srcdir,srcfile])


    fmt = row[22].lower().strip()

    hrow = []

    name,ext = os.path.splitext(srcpath)
    ext = ext.lstrip('.')

    if ext != fmt:
        print 'Warning, ext (%s) does not match format (%s) for %s' % (ext,fmt,srcpath)
        return hrow
    

    if fmt not in allowedfmt:
        print 'Caution, format not imported: %s for %s' % (fmt,srcpath)
        return hrow

    
    print 'Hashing %s ' % srcpath
    sys.stdout.flush()

    filehash = hash_a_file(srcpath)


    if (filehash != 'Error'):
        hrow = map(str.strip,row)
        hrow[11]  = hrow[11].rstrip('.') # remove trailing period in title
        
        #hrow.insert(4,filehash)
        hrow[4] = filehash

    return hrow


###############################  Main Script ###############################

if (len(sys.argv) != 2):
  print "Provide input file to process"
  print sys.argv[0] + " filename.csv\n"
  sys.exit(0)


inpfilename=sys.argv[1]
outfilename="hashed-" + inpfilename


with open(inpfilename,'r') as inpf, open(outfilename,'wb') as outf:

    inpreader  = csv.reader(inpf, delimiter=',')
    hashwriter = csv.writer(outf, delimiter=',')

    header = next(inpreader,None);
    for i in range(len(header)):
        print i, header[i]
    outheader = header

    #outheader.insert(22,"SHA1 hash")
    hashwriter.writerow(outheader)

    
    nrows = 0
    for irow in inpreader:
        result = hashedfile(irow)
        if result:
            hashwriter.writerow(result)
            nrows += 1

print
print '===================================================='
print 'Processed', nrows, "rows"
print 'Use', outfilename, "to sort and remove duplicates"
print

    
        
