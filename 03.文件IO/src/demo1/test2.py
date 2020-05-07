#!/usr/bin/env python3

content = ''
# with open('readfile.txt', 'r', encoding='gbk') as f:
with open('readfile.txt', 'r') as f:
	print('open for read...')
	for line in f.readlines():
		content += line.strip()
		
print(content)

# with open('writefile.txt', 'w', encoding='gbk') as f:
with open('writefile.txt', 'w') as f:
	f.write(content)
	print('write ok ...')