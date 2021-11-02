from ctypes import sizeof
import re
matches=re.search(r'(\.{1}\w\w\w)','file.txt')
if matches!=None:
    print('yes')
