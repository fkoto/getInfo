class Mapper:
    def __init__(self, mode):
        self.mode = mode

    def doMappingNode(self, cluster, numOfProcs, ppr):


        return []

    def doMappingSlot(self, cluster, numOfProcs, ppr):
        return []

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
