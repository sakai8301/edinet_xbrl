# coding: utf-8

#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License. See accompanying LICENSE file.

import os
from edinet_xbrl.ufocatcher_util import UfoCatcherUtil
from time import sleep
import urllib.request


class EdinetXbrlDownloader(object):
    @staticmethod
    def download(url, target_dir):
        file_name = "{0}/{1}".format(target_dir, url.split("/")[-1])
        if not os.path.exists(file_name):
            urllib.request.urlretrieve(url, file_name)
            return True
        return False

    @classmethod
    def download_by_ticker(cls, ticker, target_dir, wait_sec=1.0, type_of_document=""):
        response = UfoCatcherUtil.request(ticker)
        for url in UfoCatcherUtil.generate_edinet_xbrl_url(response.text):
            if not cls.__is_type_of_document(url, type_of_document):
                continue
            if cls.download(url, target_dir):
                sleep(wait_sec)

    @staticmethod
    def __is_type_of_document(url, type_of_document):
        """
        Specify the Type of document of url
        If you don't want to specify the type of document -> type_of_document = ""
        """
        if type_of_document == "":
            return True
        return type_of_document in url.split('-')
