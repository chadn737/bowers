#!/usr/local/apps/python/2.7.8/bin/python
import sys
from methylpy.call_mc import build_ref

build_ref([sys.argv[1] + '.fa'], sys.argv[1])

