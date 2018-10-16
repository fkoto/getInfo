class Mapper:
    def __init__(self, mode, printer):
        self.mode = mode
        self.printer = printer

    def doMappingNode(self, cluster, numOfProcs, ppr):
        res = []

        while True:
            for nod in cluster.createNodeGenerator():
                if nod.exhausted:
                    continue
                try:
                    if nod.generator is None:
                        #first pass from node
                        nod.generator = nod.createSlotGenerator()
                        nod.curSlot = nod.generator.next()

                    if nod.curSlot.generator is None:
                        #first pass from slot
                        nod.curSlot.generator = nod.curSlot.createCoreGenerator()

                    #get next core
                    for iter_ppr in range(int(ppr)):
                        while True:
                            coreId = ''
                            try:
                                coreId = nod.curSlot.generator.next()
                            except StopIteration:
                                self.printer.doprint('Slot ' + str(nod.curSlot.id) + ' of node ' + nod.id +
                                                     ' exhausted. Moving on')
                                nod.curSlot.generator = None

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
                    self.printer.doprint('Node ' + nod.id + ' out of slots. Moving on')
                    nod.generator = None
                    nod.exhausted = True
                    continue

            exhaustionFlag=True
            for nod in cluster.createNodeGenerator():  # if all nodes exhausted. break and start oversubscription mode.
                if not nod.exhausted:
                    exhaustionFlag=False
                    break
            if exhaustionFlag:
                print("All nodes exhausted!")
                break

        while True:  # repeat for oversubscription
            for nod in cluster.createNodeGenerator():
                try:
                    if nod.generator is None:
                        # first pass from node
                        nod.generator = nod.createSlotGenerator()
                        nod.curSlot = nod.generator.next()

                    if nod.curSlot.generator is None:
                        # first pass from slot
                        nod.curSlot.generator = nod.curSlot.createCoreGenerator()

                    # get next core
                    for iter_ppr in range(int(ppr)):
                        while True:
                            coreId = ''
                            try:
                                coreId = nod.curSlot.generator.next()
                            except StopIteration:
                                self.printer.doprint('Slot ' + str(nod.curSlot.id) + ' of node ' + nod.id +
                                                     ' exhausted. Moving on')
                                nod.curSlot.generator = None

                            if coreId == '':
                                    nod.curSlot = nod.generator.next()
                                    if nod.curSlot.generator is None:
                                        nod.curSlot.generator = nod.curSlot.createCoreGenerator()

                            else:
                                break

                        if len(res) < numOfProcs:
                            res.append('o' + coreId.id)
                        else:
                            return res

                except StopIteration:
                    self.printer.doprint('Node ' + nod.id + ' out of slots. Moving on')
                    nod.generator = None
                    continue

    def doMappingSlot(self, cluster, numOfProcs, ppr):
        res = []
        while True:
            for nod in cluster.createNodeGenerator():
                if nod.exhausted:
                    continue

                for sl in nod.createSlotGenerator():
                    if sl.generator is None:
                        #first pass
                        sl.generator = sl.createCoreGenerator()

                    for iter_ppr in range(int(ppr)):
                        try:
                            coreId = sl.generator.next()

                            if len(res) < numOfProcs:
                                res.append(coreId.id)
                            else:
                                return res
                        except StopIteration:
                            self.printer.doprint('Slot ' + str(sl.id) + ' of node ' + nod.id + ' exhausted. Moving on.')
                            sl.generator = None
                            sl.exhausted = True
                            break

                nodExhaustion = True
                for sl in nod.createSlotGenerator():  # check if node is exhausted
                    if not sl.exhausted:
                        nodExhaustion = False
                        break

                nod.exhausted = nodExhaustion  # check if node is exhausted

            clusterExhaustion = True
            for nod in cluster.createNodeGenerator():
                if not nod.exhausted:
                    clusterExhaustion = False
                    break

            if clusterExhaustion:
                break

        while True:  # oversubscription mode
            for nod in cluster.createNodeGenerator():
                for sl in nod.createSlotGenerator():
                    if sl.generator is None:
                        #first pass
                        sl.generator = sl.createCoreGenerator()

                    for iter_ppr in range(int(ppr)):
                        try:
                            coreId = sl.generator.next()
                            #print coreId.id
                            if len(res) < numOfProcs:
                                res.append('o' + coreId.id)
                            else:
                                return res
                        except StopIteration:
                            self.printer.doprint('Slot ' + str(sl.id) + ' of node ' + nod.id + ' exhausted. Moving on.')
                            sl.generator = None
                            break


    def doMappingCore(self, cluster, numOfProcs):
        res = []
        for nod in cluster.createNodeGenerator():  # first normal pass
            for sl in nod.createSlotGenerator():
                for cor in sl.createCoreGenerator():
                    if len(res) < numOfProcs:
                        res.append(cor.id)
                    else:
                        return res
        while True:
            for nod in cluster.createNodeGenerator():  # oversubscription mode
                for sl in nod.createSlotGenerator():
                    for cor in sl.createCoreGenerator():
                        if len(res) < numOfProcs:
                            res.append('o' + cor.id)
                        else:
                            return res

    def doMapping(self, cluster, numOfProcs, ppr=1):
        if self.mode == 'node':
            return self.doMappingNode(cluster, numOfProcs, ppr)
        elif self.mode == 'slot':
            return self.doMappingSlot(cluster, numOfProcs, ppr)
        elif self.mode == 'core':
            return self.doMappingCore(cluster, numOfProcs)
