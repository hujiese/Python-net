#!/usr/bin/env python3

content = ''
with open('pic.jpg', 'rb') as f:
    content = f.read()
    print('open for read...')
	
with open('write.jpg', 'wb') as f:
	f.write(content)
	print('write ok ...')