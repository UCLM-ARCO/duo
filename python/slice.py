# -*- mode: python; coding: utf-8 -*-

import Ice

slice_dir = "/usr/share/slice"
Ice.loadSlice("-I{0} --all {0}/duo/duo_idm.ice ".format(slice_dir))
import DUO
