#
# A class to load samples from JSON file
#

import json
import os


class SampleFile:

    @property
    def file_path(self): 
        dirname = os.path.dirname(__file__)
        path = os.path.join(dirname, '.\samples.py')
        return path 


    def load(self):
        return self.load_file(self.file_path)


    def load_file(self, path):
        with open(path) as jsonfile:
            samples = json.load(jsonfile)

        return samples
