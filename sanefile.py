#!/usr/bin/env python

# creates a filename using various fields in a CSV
# strips filename of common words and special characters


import csv
import sys
import os
import re
import urllib2
import shutil
import magic
import mimetypes


def sanefilename(strlist):
    filename = '-'.join(strlist).lower()

    # verbs, adjectives, prepositions, others from
    # https://en.wikipedia.org/wiki/Most_common_words_in_English
    prunewords = " be have do say get make go know take see come think look want give use find tell ask work seem feel try leave call good new first last long great little own other old right big high different small large next early young important few bad same able to of in for on with at by from up about into over after beneath under above others the and a that it not he as you this but his they her she or an will my all would there their via per since vs onto off is before like very most mostly and to"
    prunewordlist = prunewords.split()
    
    
    #print len(prunewordlist), prunewordlist
    #sys.exit(0)

    # \b for begin or end of word, | is logical OR
    # "\ba\b|\ban\b|\bas\b" for a, an as
    prepregex =  r"\b" + r"\b|\b".join(prunewordlist) + r"\b"
    spaceregex = r"\s"
    hypregex = r"-+"
    splcharegex = r'[\\~!@#$%^&*(){}<>?/|.,;:`\[\]+_="\']+'

    filename = re.sub(prepregex,'',filename)
    filename = re.sub(spaceregex,'-',filename)
    filename = re.sub(splcharegex,'',filename)
    filename = re.sub(hypregex,'-',filename)
    return filename

def extnmap(defext):
    extmap = {
        ".jpe" :  ".jpg",
        ".m1v" :  ".mpeg",
        ".asf" :  ".wmv"
        }
    # return the mapped extension, or itself
    return extmap.get(defext,defext)

# Input header                           # output header        
# 0  Assignee                            # 0  Unique ID (in local context)
# 1  Status                              # 1  Filename (relative)
# 2  Comment/Remark                      # 2  SHA1
# 3  Local URL                           # 3  Title 
# 4  SHA1 Hash                           # 4  Creator           
# 5  YYYY                                # 5  Date              
# 6  Source ID                           # 6  Coverage.Temporal 
# 7  Accession Number                    # 7  Coverage.Spatial  
# 8  Internal ID / Seq ID                # 8  Publisher         
# 9  Unique Resource ID                  # 9  Description       
# 10 Title                               # 10 Language          
# 11 Creator                             # 11 File type         
# 12 Date.Created                        # 12 Content Type      
# 13 Coverage.Temporal                   # 13 Format            
# 14 Coverage.Spatial                    # 14 Copyright         
# 15 Publisher                           # 15 Keyword/ Subject 
# 16 Description           
# 17 Language              
# 18 File type             
# 19 Content Type          
# 20 Format                
# 21 Copyright             
# 22 Keyword/ Subject      


def makesane(row):
   
    # replace % characters in URL eg %20 by space
    urlpath = urllib2.unquote(row[3])
    urlprefix = "http://10.129.50.5/nvli/data/"
    
    # Strip urlprefix to find the relative path in local partition
    srcfile = re.sub(urlprefix,'',urlpath)
    
    # the local partition
    srcdir = "/NFSMount/SV-Patel_Data/nvli"
    srcpath = '/'.join([srcdir,srcfile])

    title = row[10].strip()
    title = title.rstrip('.')
    title = title.strip()

    # mimetypes library does not seem to use magic, so this does not work
    #fmt = mimetypes.guess_extension(mimetypes.guess_type(srcpath)[0])

    ## https://github.com/ahupp/python-magic
    ## pip install python-magic

    try:
        ext = mimetypes.guess_extension(magic.from_file(srcpath,mime=True))
    except EnvironmentError:
        # parent of IOError, OSError *and* WindowsError where available
        # print 'Error, file not found: %s' % srcpath
        ext = "." + row[20].lower()
    except:
        print "For from_file missing error: pip install python-magic"
        sys.exit(0)
    
    # some standard mappings where the default provided by python is
    # not conventional (eg: .jpe for .jpeg or .jpg
    ext = extnmap (ext)

    # rename the original extension to that of magic
    row[20] = ext.lstrip('.')
        

    # made from uniq ID, title and extension
    filename = sanefilename([title]) # remove common words
    # get the first n words of title
    filename = '-'.join(filename.split('-')[:6])

    # prefix and suffix
    filename = sanefilename([row[9], filename]) + ext
    #filename = sanefilename([row[9], title]) + ext
    # because sanefilename strips . from filename

    # source 
    sourceid = row[6]
    dirname = sanefilename([sourceid])
    # create a subdir for each hyphenated part of uniq ID
    dirname = re.sub(r"-",'/',dirname) 

    relpath = 'archive/' + dirname + '/' + filename

    

    destroot = "/NFSMount/sardar/files"
    destpath = '/'.join([destroot, relpath])

    dirname = os.path.dirname(destpath)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    
    #os.rename is a mv and needs permissions to delete srcpath
    print 'Copying from %s to \n\t%s ' % (srcpath,destpath)
    sys.stdout.flush()

    try: 
        shutil.copyfile(srcpath,destpath)
        sane = [row[9],relpath,row[4]] + row[10:]
    # eg. src and dest are the same file
    except shutil.Error as e:
        print('Error: %s' % e)
        sane = "Error"
    # eg. source or destination doesn't exist
    except IOError as e:
        print('Error: %s, %s' % (srcpath, e.strerror))
        sane = "Error"


    #sane = [filename]
    return sane


###############################  Main Script ###############################

if (len(sys.argv) != 2):
  print "Provide input file to process"
  print sys.argv[0] + " filename.csv\n"
  sys.exit(0)


inpfilename=sys.argv[1]
outfilename="processed-" + inpfilename


with open(inpfilename,'r') as inpf, open(outfilename,'wb') as outf:

    inpreader  = csv.reader(inpf, delimiter=',')
    sanewriter = csv.writer(outf, delimiter=',')

    header = next(inpreader,None);

    for i in range(len(header)):
        print i, header[i]
    #sys.exit(0)

    outheader = [ "Unique ID",
                  "Filename",
                  "SHA1 hash",
                  "Title",
                  "Creator",
                  "Date",
                  "Coverage.Temporal",
                  "Coverage.Spatial",
                  "Publisher",
                  "Description",
                  "Language",
                  "File type",
                  "Content Type",
                  "Format",
                  "Copyright",
                  "Keyword/Subject",
    ]
    sanewriter.writerow(outheader)

    
    nrows = 0
    for irow in inpreader:
        result = makesane(irow)
        if (result != "Error"):
            sanewriter.writerow(result)
            nrows += 1

print
print '===================================================='
print 'Processed', nrows, "rows"
print 'Use', outfilename, "in the migrate module"
print

