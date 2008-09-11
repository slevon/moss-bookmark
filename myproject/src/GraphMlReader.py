import xml.dom.minidom

fileReader = open("../inputGraphML/star.xml")
lines = fileReader.readlines()
inputText = ""
for line in lines:
    inputText += line
fileReader.close()



inputXML = xml.dom.minidom.parseString(inputText)
nodes = inputXML.getElementsByTagName('node')
edges = inputXML.getElementsByTagName('edge')
for node in nodes:
    print "Node:",node.attributes['id'].value
for edge in edges:
    print "Edge %s to %s" % (edge.attributes['source'].value,edge.attributes['target'].value)
