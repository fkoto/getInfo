class Core:
    def __init__(self, Id=None):
        #print 'creating core. id=' + str(Id)
        if Id is None:
            self.id = ''
        else:
            self.id = Id


class Slot:
    def __init__(self, Id=None, **kwargs):
        #print 'creating slots. id=' + str(Id)
        #print 'kwargs:{' + str(kwargs) + '}'
        self.generator = None
        if Id is None:
            self.id = ''
        else:
            self.id = Id

        self.parentNodeId = kwargs.get('parentId', -1)

        self.cores = []
        if kwargs.get('numOfCores') is not None:
            for c in range(kwargs.get('numOfCores')):
                temp = Core(str(c) + ':' + str(self.id) + ':' + str(self.parentNodeId))
                self.cores.append(temp)

    def createCoreGenerator(self):
            for core in self.cores:
                yield core


class Node:
    def __init__(self, Id=None, **kwargs):
        self.generator = None
        self.curSlot = None
        if Id is None:
            self.id = ''
        else:
            self.id = Id

        self.maxSlots = kwargs.get('maxSlots', -1)
        self.slots = []
        if kwargs.get('numOfSlots') is not None:
            coresPerSlot =  kwargs.get('numOfCoresPerSlot', 1)
            for sl in range(kwargs.get('numOfSlots')):
                temp = Slot(sl, numOfCores=coresPerSlot, parentId=self.id)
                self.slots.append(temp)

    def setSlots(self, numOfSlots, numOfCoresPerSlot):
        for i in range(numOfSlots):
            temp = Slot(i, numOfCores=numOfCoresPerSlot, parentId=self.id)
            self.slots.append(temp)

    def createSlotGenerator(self):
            for slot in self.slots:
                yield slot


class Cluster:
    def __init__(self, printer):
        self.nodes = []
        self.printer = printer

    def getNodesFromHostFile(self, inputFile, numOfCoresPerSlot=1):
        cnt = 0
        for line in inputFile:
            #print (line)
            line = line.strip()  # remove trailing whitespaces
            if not line or line.startswith('#'):
                cnt += 1
                continue  # ignore comments and empty lines

            numOfCores = 0
            if '#cores=' in line: #get custom arg of num of cores
                parts = line.split('#cores=')
                line = parts[0].strip()
                # print('line after removing #cores: ' + line)
                numOfCores = parts[1].strip().split()[0]
                # print('Read ' + numOfCores + ' as numOfCores')

            line = line.split('#')[0]  # ignore inline comments
            #print (line + ' (after removing comments)')
            splitted = line.split()

            node = Node()
            node.id = splitted[0]

            # a multicore node
            if ' slots=' in line:
                if numOfCores == 0:
                    node.setSlots(int(splitted[1].split('=')[-1]), numOfCoresPerSlot)
                else:
                    node.setSlots(int(splitted[1].split('=')[-1]), int(numOfCores))

            # maxSlots are defined
            if 'max-slots=' in line:
                node.maxSlots = int(splitted[-1].split('=')[-1])
                if len(node.slots) == 0:
                    if numOfCores == 0:
                        node.setSlots(node.maxSlots, numOfCoresPerSlot)
                    else:
                        node.setSlots(node.maxSlots, int(numOfCores))

            # a single core node (neither 'slots' nor 'max-slots' is defined)
            if 'slots' not in line:
                if numOfCores == 0:
                    node.setSlots(1, numOfCoresPerSlot)
                else:
                    node.setSlots(1, int(numOfCores))

            # add to cluster
            #print(node.id)
            #for slot in node.slots:
            #  print 'has->' + str(slot.id) + ' with ' + str(len(slot.cores)) + ' cores'
            self.nodes.append(node)

            #print('ignored:' + str(cnt) + ' lines!')

    def printClusterDetails(self, withIds = False):
        self.printer.doprint("\n########SIMULATION ENV#############", withIds)
        if not withIds:
            for nod in self.nodes:
                self.printer.doprint('Node id=' + str(nod.id))
                slots = len(nod.slots)
                self.printer.doprint('slots=' + str(slots))
                cores = sum(len(i.cores) for i in nod.slots)
                self.printer.doprint('cores=' + str(cores) + '\n')
        else:
            for nod in self.nodes:
                self.printer.doprint('Node id=' + str(nod.id), True)
                for sl in nod.slots:
                    self.printer.doprint('\tSlot id=' + str(sl.id), True)
                    for c in sl.cores:
                        self.printer.doprint('\t\tCore id=' + str(c.id), True)
        self.printer.doprint("###################################\n", withIds)

    def createNodeGenerator(self):
            for node in self.nodes:
                yield node

    def getNextAvailableNode(self):
        try:
            for nod in self.createNodeGenerator():
                return nod
        except StopIteration:
            return None

    def countClusterResources(self):
        resources = 0
        for nod in self.nodes:
            for sl in nod.slots:
                for c in sl.cores:
                    resources +=1
        return resources