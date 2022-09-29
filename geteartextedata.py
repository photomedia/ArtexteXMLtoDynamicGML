import urllib.request, urllib.error

#TN - December 2019 - Upgrade Script to Python3

#artists = "Dille+curtin+lambeth+tata"
#usage: python geteartextedata.py -a "Dille+curtin+lambeth+tata" -o data_humanist_photography.xml

#all data
#usage: python geteartextedata.py -m "all" -o all_eartexte.xml

#keywords="photography+photograhie"
#usage: python geteartextedata.py -k "photography+photographie" -o kw_photography_photographie.xml

#simple search for "Bibliographical+record+included+in+Felicity+Tayler%27s+research+and+cataloging+project"
#usage: python geteartextedata.py -x "Bibliographical+record+included+in+Felicity+Tayler%27s+research+and+cataloging+project" -o x_cataloguing_project.xml
#https://e-artexte.ca/cgi/facet/simple2?cache=&amp;exp=0%7C1%7C%7Carchive%7C-%7Cq%3A%3AALL%3AIN%3A"+xkeywords+"%7C-%7C&amp;output=ArtexteXML&amp;_action_export_redir=1

import sys, getopt

def main(argv):
   artists = ''
   outputfile = ''
   mode =''
   keywords =''
   xkeywords = ''
   try:
      opts, args = getopt.getopt(argv,"ha:k:x:m:o:",["artists=","keywords=","xkeywords=","mode=","ofile="])
   except getopt.GetoptError:
      print ('geteartextedata.py -a <artists> -k <keywords> -m <all> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('geteartextedata.py -a <artists> -k <keywords> -x <xapian keywords> -m <all> -o <outputfile>')
         sys.exit()
      elif opt in ("-a", "--artists"):
         artists = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
      elif opt in ("-m", "--mode"):
         mode = arg
      elif opt in ("-k", "--keywords"):
         keywords = arg
      elif opt in ("-x", "--xkeywords"):
         xkeywords = arg
		
      #print 'Artists string is ', artists
      #print 'Output file is ', outputfile
      #print 'Mode is ', mode
      #print 'Keywords are', keywords
   if artists != '':
      try:
         requesturl = "https://e-artexte.ca/cgi/search/archive/advanced/export_artexte_XML.xml?screen=Search&dataset=archive&_action_export=1&output=XML&exp=0%7C1%7C-date%2Fcontributors_name%2Ftitle%7Carchive%7C-%7Cartists%3Aartists%3AANY%3AIN%3A"+artists+"%7C-%7Ceprint_status%3Aeprint_status%3AANY%3AEQ%3Aarchive%7Cmetadata_visibility%3Ametadata_visibility%3AANY%3AEQ%3Ashow&n="
         print ('downloading artists query'+artists)
         print ('into file', outputfile)
         resp = urllib.request.urlopen(requesturl)
         f = open(outputfile, 'wb')
         f.write(resp.read())
         # - this would be to print it out: print resp.read()
         f.close()
      except IOError as e:
         print ("Error: " + format(str(e)))
   elif mode == 'all':
      try:
         requesturl = "https://e-artexte.ca/cgi/search/advanced/export_artexte_XML.xml?screen=Public%3A%3AEPrintSearch&_action_export=1&output=XML&exp=0%7C1%7C-date%2Fcontributors_name%2Ftitle%7Carchive%7C-%7Cfull_text_status%3Afull_text_status%3AANY%3AEQ%3Apublic+restricted+none%7C-%7Ceprint_status%3Aeprint_status%3AALL%3AEQ%3Aarchive%7Cmetadata_visibility%3Ametadata_visibility%3AALL%3AEX%3Ashow&n="
         print ('downloading all data from e-artexte')
         print ('into file', outputfile)
         resp = urllib.request.urlopen(requesturl)
         f = open(outputfile, 'wb')
         f.write(resp.read())
         # - this would be to print it out: print resp.read()
         f.close()
      except IOError as e:
         print ("Error: " + format(str(e)))
   elif keywords != '':
      try:
         requesturl = "https://e-artexte.ca/cgi/search/archive/advanced/export_artexte_XML.xml?screen=Search&dataset=archive&_action_export=1&output=XML&exp=0%7C1%7C-date%2Fcontributors_name%2Ftitle%7Carchive%7C-%7Ckw%3Akw%3AANY%3AIN%3A"+keywords+"%7C-%7Ceprint_status%3Aeprint_status%3AANY%3AEQ%3Aarchive%7Cmetadata_visibility%3Ametadata_visibility%3AANY%3AEQ%3Ashow&n="
         print ('downloading keyword query', keywords)
         print ('into file', outputfile)
         resp = urllib.request.urlopen(requesturl)
         f = open(outputfile, 'wb')
         f.write(resp.read())
         # - this would be to print it out: print resp.read()
         f.close()
      except IOError as e:
         print ("Error: " + format(str(e)))
   elif xkeywords != '':
      try:
         requesturl = "https://e-artexte.ca/cgi/facet/simple2?cache=&amp;exp=0%7C1%7C%7Carchive%7C-%7Cq%3A%3AALL%3AIN%3A"+xkeywords+"%7C-%7C&amp;output=ArtexteXML&amp;_action_export_redir=1";
         print ('downloading xapian (simple) keyword query', xkeywords)
         print ('into file', outputfile)
         resp = urllib.request.urlopen(requesturl)
         f = open(outputfile, 'wb')
         f.write(resp.read())
         # - this would be to print it out: print resp.read()
         f.close()
      except IOError as e:
         print ("Error: " + format(str(e)))

if __name__ == "__main__":
   main(sys.argv[1:])