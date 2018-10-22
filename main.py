import os

p = os.popen('dir')
print(p.read())