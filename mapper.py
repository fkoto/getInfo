class Mapper:
    def __init__(self, mode):
        self.mode = mode

    def doMappingNode(self, cluster, numOfProcs, ppr):
        res = []
        i = 0
        while True:
            for nod in cluster.createNodeGenerator():
                try:
                    if nod.generator is None:
                        #first pass from node
                        nod.generator = nod.createSlotGenerator()
                        nod.curSlot = nod.generator.next()

                    if nod.curSlot.generator is None:
                        #first pass from slot
                        nod.curSlot.generator = nod.curSlot.createCoreGenerator()

                    #get next core
                    while True:
                        coreId = ''
                        try:
                            coreId = nod.curSlot.generator.next()
                        except StopIteration:
                            print 'Slot ' + str(nod.curSlot.id) + ' of node ' + nod.id + ' exhausted. Moving on'

                        if coreId == '':
                                nod.curSlot = nod.generator.next()
                                if nod.curSlot.generator is None:
                                    nod.curSlot.generator = nod.curSlot.createCoreGenerator()

                        else:
                            break

                    if len(res) < numOfProcs:
                        res.append(coreId.id)
                    else:
                        return res

                except StopIteration:
                    print 'Node ' + nod.id + ' out of slots. Moving on'
                    continue

    def doMappingSlot(self, cluster, numOfProcs, ppr):
        res = []
        while True:
            for nod in cluster.createNodeGenerator():
                for sl in nod.createSlotGenerator():
                    if sl.generator is None:
                        #first pass
                        sl.generator = sl.createCoreGenerator()

                    try:
                        coreId = sl.generator.next()
                        #print coreId.id
                        if len(res) < numOfProcs:
                            res.append(coreId.id)
                        else:
                            return res
                    except StopIteration:
                        print 'Slot ' + str(sl.id) + 'of node ' + nod.id + ' exhausted. Moving on.'



    def doMappingCore(self, cluster, numOfProcs):
        res = []
        for nod in cluster.createNodeGenerator():
            for sl in nod.createSlotGenerator():
                for cor in sl.createCoreGenerator():
                    if len(res) < numOfProcs:
                        res.append(cor.id)
                    else:
                        return res
        return res

    def doMapping(self, cluster, numOfProcs, ppr=1):
        if self.mode == 'node':
            return self.doMappingNode(cluster, numOfProcs, ppr)
        elif self.mode == 'slot':
            return self.doMappingSlot(cluster, numOfProcs, ppr)
        elif self.mode == 'core':
            return self.doMappingCore(cluster, numOfProcs)
