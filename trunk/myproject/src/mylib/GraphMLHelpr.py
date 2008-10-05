from  xml.dom import minidom
class GraphMLHelpr(object):
    def __init__(self):
        object.__init__(self)
        self.inputXML = ""
    def readXML(self,filename):
        try:
            fileReader = open(str(filename))
            lines = fileReader.readlines()
            inputText = ""
            for line in lines:
                inputText += line
            fileReader.close()
            self.inputXML = xml.dom.minidom.parseString(inputText)
        except IOError:
            print "No file"
    def getNodes(self):
        resultNode = []
        nodes = self.inputXML.getElementsByTagName('node')
        for node in nodes:
            resultNode.append(node.attributes['id'].value)
        return resultNode
    def saveXML(self,filepath,graphWidget):
        xmlDefine = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xmlRoot     = \
'<graphml xmlns="http://graphml.graphdrawing.org/xmlns" \
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" \
xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns \
http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">\n'
        #first version not support directed graph
        
        xmlGraph       = '\t<graph id="G" edgedefault="undirected">\n'
        xmlGraphTail   = '\t</graph>\n'
        xmlTail        = '</graphml>\n'
        xmlNode        = ''
        xmlEdge        = ''
        graph          = graphWidget.getGraph()
        for node in graph:
            xmlNode += '\t\t<node id="%s"/>\n'%(node)
        edges = graphWidget.getEdges()
        for edge in edges:
            xmlEdge += '\t\t<edge source="%s" target="%s"/>\n'%(edge)
        xmlResult = xmlDefine+xmlRoot+xmlGraph+\
                    xmlNode+xmlEdge+\
                    xmlGraphTail+xmlTail
        fileWritr = open(filepath,"w")
        fileWritr.write(xmlResult)
        fileWritr.close()
