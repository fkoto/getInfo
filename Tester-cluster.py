import clusterClasses
import mapper
import sorter

myCluster = clusterClasses.Cluster()
mapper = mapper.Mapper('core')
mySorter = sorter.Sorter('node')

infile = open('./hostFile-example', 'r')
myCluster.getNodesFromHostFile(infile)

myCluster.printClusterDetails()

print myCluster.nodes[3].id

for i in myCluster.nodes[3].createSlotGenerator():
    print i.id
#
# ids = mapper.doMapping(myCluster, 4)
#
# for el in ids:
#     print el
#
# ids = mySorter.compare(ids)
#
# for el in ids:
#     print el

mygenerator = myCluster.nodes[3].createSlotGenerator()
print('-----------------')
print mygenerator.next().id
print mygenerator.next().id