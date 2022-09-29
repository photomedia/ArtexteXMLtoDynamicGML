import xml.etree.ElementTree as ET
import csv

filename = "artists.csv"
# opening the file with w+ mode truncates the file
f = open(filename, "w+")
f.close()


filename = "contributors.csv"
# opening the file with w+ mode truncates the file
f = open(filename, "w+")
f.close()

filename = "creators.csv"
# opening the file with w+ mode truncates the file
f = open(filename, "w+")
f.close()

filename = "group-contributors.csv"
# opening the file with w+ mode truncates the file
f = open(filename, "w+")
f.close()

sourcetree = ET.parse('XML/x_periodicals.xml')
targettree = ET.parse('XML/blank-eprints.xml')
sourceroot = sourcetree.getroot()
targetroot = targettree.getroot()
attrib = {}

for elem in sourceroot.findall("eprint"):
    # adding an element to the root node
    targetelement = targetroot.makeelement("eprint", attrib)

    elementToAdd = elem.find('eprintid')
    targetelementid = targetroot.makeelement("eprintid", attrib)
    targetelementid.text = elementToAdd.text
    targetelement.append(targetelementid)

    elementToAdd = elem.find('date')
    targetelementid = targetroot.makeelement("date", attrib)
    targetelementid.text = elementToAdd.text
    targetelement.append(targetelementid)

    elementToAdd = elem.find('publication')
    targetelementid = targetroot.makeelement("publication", attrib)
    targetelementid.text = elementToAdd.text
    targetelement.append(targetelementid)

    
    for subelem in elem.iter('contributors'):
        combinedcontributors = subelem.makeelement("contributors", attrib)
        for subsubelem in subelem.iter('item'):
            combinedcontributors.append(subsubelem)
            with open('contributors.csv', mode='a') as gc_file:
                c_file = csv.writer(gc_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                c_name_family_text=''
                c_name_first_text=''
                c_type_text=''
                c_name_family=subsubelem.find('name/family')
                if c_name_family is not None:
                    c_name_family_text=c_name_family.text
                c_name_first=subsubelem.find('name/given')
                if c_name_first is not None:
                    c_name_first_text=c_name_first.text
                c_type=subsubelem.find('type')
                if c_type is not None:
                    c_type_text=c_type.text
                c_full_name= c_name_family_text+", "+c_name_first_text
                c_file.writerow([c_full_name,c_type_text])
    #for subelem in elem.iter('creators'):
    #    for subsubelem in subelem.iter('item'):
    #        with open('creators.csv', mode='a') as gc_file:
    #            c_file = csv.writer(gc_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #            c_name_family_text=''
    #            c_name_first_text=''
    #            c_name_family=subsubelem.find('name/family')
    #            if c_name_family is not None:
    #                c_name_family_text=c_name_family.text
    #            c_name_first=subsubelem.find('name/given')
    #            if c_name_first is not None:
    #                c_name_first_text=c_name_first.text
    #            c_full_name= c_name_family_text+", "+c_name_first_text
    #            c_file.writerow([c_full_name])
    #        combinedcontributors.append(subsubelem) 
    for subelem in elem.iter('group_contributors'):
        for subsubelem in subelem.iter('item'):
            with open('group-contributors.csv', mode='a') as gc_file:
                gc_file = csv.writer(gc_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                gc_name=subsubelem.find('name')
                gc_name_text=''
                if gc_name is not None:
                    gc_name_text=gc_name.text
                gc_type=subsubelem.find('type')
                if gc_type is not None:
                    gc_type_text=gc_type.text
                gc_file.writerow([gc_name_text, gc_type_text])
            combinedcontributors.append(subsubelem)
    for subelem in elem.iter('artists'):
        for artistitem in subelem.iter('item'):
            artistname=ET.SubElement(artistitem, "name")
            artistname.text=artistitem.text
            with open('artists.csv', mode='a') as artists_file:
                artists_file = csv.writer(artists_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                artists_file.writerow([artistitem.text])
            artistitem.text=''
            combinedcontributors.append(artistitem)
    targetelement.append(combinedcontributors)
    targetroot.append(targetelement)
        
targettree.write('XML/x_periodicals-combined-contributors-artists-groupcontributors.xml', encoding="UTF-8")