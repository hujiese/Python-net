#!/usr/bin/env python3

content = ''
with open('readfile.txt', 'r') as f:
    content = f.read()
    print('open for read...')
    print(content)
	
with open('writefile.txt', 'w') as f:
	f.write(content)
	print('write ok ...')