class RankFiler:

    def __init__(self, file, out):
        self.inputFile = file
        self.outfile = out

    def parseRankFile(self):
        self.outfile.write("\n##########OUTPUT##############\n")
        for line in self.inputFile:
            #print (line)

            if not line:
                return

            parts = line.split('=')

            rank_dirty = parts[0]
            node_dirty = parts[1]
            slot = parts[-1]

            rank = rank_dirty.split()[-1]
            node = node_dirty.split()[0]
            mapping = ('0:' + str(slot) + ':' + str(node)).replace('\n', '')

            self.outfile.write(str(rank) + ' ' + mapping + '\n')
