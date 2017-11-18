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



