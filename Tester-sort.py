import sorter

lst = ['1:0:0', '0:1:1', '1:0:2', '0:1:3', '1:1:3',
       '0:0:0', '0:0:1', '1:0:1', '0:0:2', '0:1:3', '0:1:0',
       '1:1:0', '0:0:3', '1:0:3', '1:1:2', '1:1:3', '0:1:2',
       '1:1:1']

y = sorter.Sorter('core')

cnt = 0
for el in y.compare(lst):
    print str(cnt) + ' ' + el
    cnt += 1
