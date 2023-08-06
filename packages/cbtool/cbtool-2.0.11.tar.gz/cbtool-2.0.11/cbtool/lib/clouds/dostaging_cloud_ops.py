#!/usr/bin/env python

#/*******************************************************************************
# Copyright (c) 2015 DigitalOcean, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0
#
#/*******************************************************************************

'''
    Created on May 17, 2018
    DigitalOcean Internal Stage2 Object Operations Library
    @author: Michael R. Hines
'''
from lib.auxiliary.code_instrumentation import trace, cbdebug, cberr, cbwarn, cbinfo, cbcrit

from doprod_cloud_ops import DoprodCmds 
from libcloud_common import LibcloudCmds

from libcloud.common.digitalocean import DigitalOcean_v2_Connection
DigitalOcean_v2_Connection.host = "api.s2r1.internal.digitalocean.com"

class DostagingCmds(DoprodCmds) :
    @trace
    def __init__ (self, pid, osci, expid = None) :
        LibcloudCmds.__init__(self, pid, osci, expid = expid, \
                              provider = "DIGITAL_OCEAN", \
                              num_credentials = 1, \
                              use_ssh_keys = True, \
                              # This is the only difference right now
                              use_volumes = False, \
                              tldomain = "digitalocean.com", \
                             )
    
    @trace
    def get_description(self) :
        return "DigitalOcean Internal Stage2 Cloud"
