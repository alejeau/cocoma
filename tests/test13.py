import os

from model.Paths import Paths
from util.SimPreprocessor import SimPreprocessor

xmls_path = Paths.Maps + 'xml'

for root, dirs, files in os.walk(xmls_path):
    for name in files:
        print((xmls_path + '/' + name).replace("xml", "json"))

json_path = Paths.Maps + "/json"

SimPreprocessor.convert_xmls_to_jsons(xmls_path, json_path)


