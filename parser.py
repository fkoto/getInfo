import argparse
import sys

class Parser():
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Generating a mapping for a mpi proccess.')
        self.parser.add_argument('-core', '--core', dest = 'cores', type=int, default=1,
                                 help='Number of cores per slot')
        self.parser.add_argument('-host', '-H', '--host', nargs='*', help='Hosts on which to run application')
        self.parser.add_argument('-hostfile', '--hostfile', '-machinefile', '--machinefile',
                                 type=argparse.FileType('r'), help='File containing information on the nodes')
        self.parser.add_argument('-c', '-n', '--n', '-np', dest='procs', type=int, default=1, help='Number of processes to launch')
        self.parser.add_argument('-map-by', '--map-by', default='node', type=str, help='Mapping of processes.')
        self.parser.add_argument('-nooversubscribe', '--nooversubscribe', action='store_true'
                                 , help='Do not oversubscribe any nodes')
        self.parser.add_argument('-bynode', '--bynode', action='store_true'
                                 , help='assign processes one per node, cycling in a RR fashion')
        self.parser.add_argument('-rank-by', '--rank-by', default='slot', choices=['slot', 'core', 'node']
                                 , type=str, help='Ranking of processes.')
        self.parser.add_argument('-rf', '--rankfile', type=argparse.FileType('r'), help='Provide a ranking file')
        self.parser.add_argument('-o', '--outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout,
                                 help='Where final result will be printed. (default: stdout)')
        self.parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode.')
        self.parser.add_argument('args', nargs=argparse.REMAINDER)  # gather rest of items in a list

    def getParser(self):
        return self.parser
