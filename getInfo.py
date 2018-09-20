#!/usr/bin/python

import sorter
import mapper
import clusterClasses
import parser
import sys

parser = parser.Parser()
myParser = parser.getParser()

args = myParser.parse_args()

if len(sys.argv) == 1:
    print myParser.print_help()
    exit(1)
else:
    print args


if args.rankfile is not None:
    print 'rank file mode is not yet functional! Exiting'
    exit(1)

if args.host is not None:
    print 'host arg is specified!'
    temp1 = []
    temp2 = []
    for el in args.host:
        if (',' in el):
            temp1.extend(el.split(','))
        else:
            temp2.append(el)

    args.host = temp2
    args.host.extend(temp1)

#get cluster parameters
myCluster = clusterClasses.Cluster()

if args.hostfile is not None:
    print 'hostfile is specified!'
    myCluster.getNodesFromHostFile(args.hostfile, args.cores)
    myCluster.printClusterDetails()

    if args.host is not None:
        print 'also host is specified!'
        ind = []
        for el in myCluster.nodes:
            if el.id in args.host:
                ind.append(el)

        myCluster.nodes = ind
        print 'final cluster'
        myCluster.printClusterDetails()
elif args.hostfile is None and args.host is not None:
    numOfSlots = input('Please specify number of slots on each host:')

    for host in args.host:
        nod = clusterClasses.Node(host, numOfSlots=numOfSlots, numOfCoresPerSlot=args.cores)
        myCluster.nodes.append(nod)
else:
    #hostfile is None and host is None
    numOfNodes = input('Please specify number of host on the cluster:')
    numOfSlots = input('Please specify number of slots on each host:')

    for i in range(numOfNodes):
        nod = clusterClasses.Node('node' + str(i), numOfSlots=numOfSlots, numOfCoresPerSlot=args.cores)
        myCluster.nodes.append(nod)

#myCluster.printClusterDetails() # print num of components per node
myCluster.printClusterDetails(True) # print all ids of cluster

if args.nooversubscribe:
    print 'No oversubscription requested!'
    if (args.procs > myCluster.countClusterResources()):
        print ('Cluster cannot handle that many processes! (disable no-oversubscription flag)')
        exit()

#Get mapping and ranking parameters
if args.bynode is True:
    print 'By node!'
    mapmode = 'node'
    rankmode = 'node'
    ppr = 1
else:
    print 'map-by ' + args.map_by
    print 'rank-by ' + args.rank_by

    if ':' in args.map_by:
        split = args.map_by.split(':')
        ppr = split[1]
        mapmode = split[-1]
    else:
        mapmode = args.map_by
        ppr = 1

    rankmode = args.rank_by


myMapper = mapper.Mapper(mapmode)
myRanker = sorter.Sorter(rankmode)

print 'Initiating ' + str(args.procs) + ' processes'
mapIds = myMapper.doMapping(myCluster, args.procs, ppr)

finalIds = myRanker.compare(mapIds)

args.outfile.write("\n##########OUTPUT##############\n")

cnt = 0
for el in finalIds:
    args.outfile.write(str(cnt) + ' ' + el +'\n')
    cnt += 1

