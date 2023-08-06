#
# A class to load samples from JSON file
#

import json
import os


class SampleFile:


    def load(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, '.\samples.json')

        return self.loadFile(filename)


    def loadFile(self, path):
        with open(path) as jsonfile:
            samples = json.load(jsonfile)

        return samples
