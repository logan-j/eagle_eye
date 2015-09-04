from glob import glob
import csv
import re
from nameparser import HumanName
import argparse
from sets import Set
import lxml.html as lxml
import re
import sys

class eagle:
	def __init__(self, directory):
		self.files = []

		for folder in glob(directory + "/*"):
			for f in glob(folder + "/*"):
				if not f.endswith("txt"): self.files.append(f)

	def process(self):
		pass
	def write(self):
		pass


	def run(self):
		for i, f in enumerate(self.files, 1):
			try:
				node = lxml.parse(f)
				sys.stderr.write("Working on: %s of %s\n" % (i, len(self.files)))
				for subnode in node.xpath("//td[@class='LeaseVarianceHousehold_x0020_name']//text()"):
					name = HumanName(subnode.encode('ascii', 'ignore').strip().split(";")[0])
					name.capitalize()
					print "%s\t%s" % (name.first, name.last)
				for subnode in node.xpath("//tr[not(@class='DetailsHeader')]"):
					firsts = subnode.xpath(".//td[@class='LeaseVarianceFirst_x0020_Name']//text()")
					lasts = subnode.xpath(".//td[@class='LeaseVarianceLast_x0020_Name']//text()")

					for item in zip(firsts, lasts):
						first = re.split(' and |&', item[0].encode('ascii', 'ignore'))[0].lower()
						last = re.split(' and |&', item[1].encode('ascii', 'ignore'))[0].lower()
						name = HumanName(first + " " + last)
						name.capitalize()
						print "%s\t%s" % (name.first, name.last)
					"""
					if firsts > lasts:
						for name in firsts[len(firsts) - len(lasts):]:
							print f, "%s\tNot Provided" % name
					elif lasts < firsts:
						for name in lasts[len(lasts) - len(firsts):]:
							print f, "Not Provided\t%s" % name
					"""

			except Exception as inst:
				print f, str(inst)
			#print node.xpath("//div[@class='CompanySite']/text()")[0]

def main():
	parser = argparse.ArgumentParser(description='')

	parser.add_argument('infile', nargs='?', type=str)

	args = parser.parse_args()

	eagle(args.infile).run()


if __name__ == '__main__':
	main()