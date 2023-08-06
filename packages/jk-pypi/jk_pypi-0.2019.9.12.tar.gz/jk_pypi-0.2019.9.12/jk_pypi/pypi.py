


import sys
import os
import urllib.request
from bs4 import BeautifulSoup

from jk_utils import Version



class PyPi(object):

	def __init__(self):
		self.__serverURL = "https://pypi.org/"
		self.__baseURL = self.__serverURL + "project/"

		with urllib.request.urlopen(self.__serverURL) as response:
			rawHTML = response.read()
			assert len(rawHTML) > 0
	#

	def getModuleVersion(self, moduleName:str) -> Version:
		assert isinstance(moduleName, str)

		try:
			with urllib.request.urlopen(self.__baseURL + moduleName) as response:
				rawHTML = response.read()
				soup = BeautifulSoup(rawHTML, "html.parser")
				xH1 = soup.find("h1", {
					"class": "package-header__name"
				})
				assert xH1
				s = xH1.text.strip()
				assert len(s) > 0
				pos = s.find(" ")
				assert pos > 0
				return Version(s[pos+1:].strip())
				
		except Exception as ee:
			return None
	#

#





