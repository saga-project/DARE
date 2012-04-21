import os
PWD = os.path.dirname(os.path.realpath(__file__))

os.system("/bin/date")
strrr = "sed -e 's/USERNAME/%s/'  -e 's/YOUR_ALLOCATION/%s/'  -e 's/THORN_NAME/%s/'  -e 's@RESOURCE_CACTUS_WD@%s@'  < %s > %s " %( 'smaddi2','aghdsjkf' , 'ein.th', '/fhdas/fdkafhg/', PWD+'/def.local.ini', PWD+ '/newskdf.ini')
print strrr
os.system(strrr)