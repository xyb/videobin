# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4
# Written 2009 by j@mailb.org

import os
from os.path import exists, join, dirname, abspath
import sys

import simplejson


class TheoraEnc:
    ffmpeg2theora = 'ffmpeg2theora'
    settings = '-p videobin'
    def __init__(self, inputFile, outputFile):
        self.inputFile = inputFile
        self.outputFile = outputFile

    def commandline(self):
        cmd = '%s --frontend %s "%s" ' % (
            self.ffmpeg2theora,
            self.settings,
            self.inputFile.replace("'", "\'")
            )
        if self.outputFile:
            cmd += ' -o "%s"' % self.outputFile.replace('"', '\"')
        cmd += ' --no-upscaling -F30'
        cmd += ' >/dev/null 2>&1'
        return cmd

    def encode(self):
        cmd = self.commandline()
        print cmd
        sts = os.system(cmd)
        if sts == 0:
            return True
        else: #encoding failed
            return False

