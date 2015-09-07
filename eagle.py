import csv
import re
from nameparser import HumanName
import argparse
from sets import Set
import lxml.html as lxml
import re
import sys
import os
import traceback
from nameparser.config import CONSTANTS

class eagle:
	def __init__(self, directory, args):
		self.files = []
		self.args = args
		for root, dirs, files in os.walk(directory):
			
			for f in files:
				
				if not f.endswith("txt"): self.files.append(os.path.join(root,f))

		CONSTANTS.titles.remove('guru')

	def process(self, r_node):
		person = {'First Name': '', 'Last Name': '', 'Phone #s': '', 'Email': '',
					'Move-In Date': '', 'Source 1': '', 'Source 2': '', 'Property': prop}
	def write(self):
		pass


	def run(self):
		print "Property Name\tFirst Name\tLast Name\tPhone Numbers\tEmail\tMove-In Date\tSource 1\tSource 2"
		count = 0
		for i, f in enumerate(self.files, 1):
			people = []
			
			try:
				node = lxml.parse(f)
				sys.stderr.write("Working on %s: %s of %s\n" % (f, i, len(self.files)))
				"""
				for subnode in node.xpath("//td[@class='LeaseVarianceHousehold_x0020_name']//text()"):
					name = HumanName(subnode.encode('ascii', 'ignore').strip().split(";")[0])
					name.capitalize()
					print "%s\t%s\t%s" % (subnode.encode('ascii', 'ignore').strip(), name.first, name.last)
				"""
				prop = node.xpath("//div[@class='CompanySite']//text()")[0].encode('ascii', 'ignore')

				for subnode in node.xpath("//tr[not(@class='DetailsHeader')]"):
					firsts = subnode.xpath("./td[@class='LeaseVarianceFirst_x0020_Name']/text()")
					lasts = subnode.xpath("./td[@class='LeaseVarianceLast_x0020_Name']/text()")
					f_name = subnode.xpath("./td[@class='LeaseVarianceHousehold_x0020_name']/text()")
					person = {}
					for item in zip(firsts, lasts):
						person = {'First Name': '', 'Last Name': '', 'Phone #s': '', 'Email': '',
									'Move-In Date': '', 'Source 1': '', 'Source 2': '', 'Property': prop}
						person['raw'] = re.sub('[\t\r\n]', '', item[1].strip())
						person['raw'] += ", %s" % re.sub('[\t\r\n]', '', item[0].strip())
						first = re.split(' and |&', item[0].encode('ascii', 'ignore'))[0].lower()
						last = re.split(' and |&', item[1].encode('ascii', 'ignore'))[0].lower()
						name = HumanName(first + " " + last)
						name.capitalize()
						
						person['First Name'] = name.first
						person['Last Name'] = name.last
						try:
							number = subnode.xpath("./td[@class='LeaseVarianceCell_x0020_Phone']/text()")[0].encode('ascii', 'ignore').strip()
							if len(number) > 0: person['Phone #s'] += "Cell: %s;" % number
						except:
							pass
						try:
							number = subnode.xpath("./td[@class='LeaseVarianceHome_x0020_Phone']/text()")[0].encode('ascii', 'ignore').strip()
							if len(number) > 0: person['Phone #s'] += "Home: %s;" % number
						except:
							pass
						try:
							number = subnode.xpath("./td[@class='LeaseVarianceWork_x0020_Phone']/text()")[0].encode('ascii', 'ignore').strip()
							if len(number) > 0: person['Phone #s'] += "Work: %s;" % number
						except:
							pass
						try:
							source = subnode.xpath("./td[@class='LeaseVariance_x0031_st_x0020_Phone_x0020_Type']/text()")[0].encode('ascii', 'ignore').strip()
							number = subnode.xpath("./td[@class='LeaseVariance_x0031_st_x0020_Phone_x0020_Number']/text()")[0].encode('ascii', 'ignore').strip()
							if len(number) > 0 and len(source) > 0: person['Phone #s'] += "%s: %s;" % (source, number)
						except:
							pass
						try:
							source = subnode.xpath("./td[@class='LeaseVariance_x0032_nd_x0020_Phone_x0020_Type']/text()")[0].encode('ascii', 'ignore').strip()
							number = subnode.xpath("./td[@class='LeaseVariance_x0032_nd_x0020_Phone_x0020_Number']/text()")[0].encode('ascii', 'ignore').strip()
							if len(number) > 0 and len(source) > 0: person['Phone #s'] += "%s: %s;" % (source, number)
						
						except:
							pass

						if person['Phone #s'].endswith(";"): person['Phone #s'] = person['Phone #s'][:-1]

						try:
							email = subnode.xpath("./td[@class='LeaseVarianceE-mail']/text()")[0].encode('ascii', 'ignore').strip()
							if len(email) > 0: person['Email'] = email
						except:
							pass
						try:
							mid = subnode.xpath("./td[@class='LeaseVarianceMove-in_x0020_date']/text()")[0].encode('ascii', 'ignore').strip()
							if len(mid) > 0: person['Move-In Date'] = mid
						except:
							pass
						try:
							s1 = subnode.xpath("./td[@class='LeaseVariance_x0031_st_x0020_advertising_x0020_source']/text()")[0].encode('ascii', 'ignore').strip()
							if len(s1) > 0: person['Source 1'] = s1
						except:
							pass
						try:
							s2 = subnode.xpath("./td[@class='LeaseVariance_x0032_nd_x0020_advertising_x0020_source']/text()")[0].encode('ascii', 'ignore').strip()
							if len(s2) > 0: person['Source 2'] = s2
						except:
							pass
						try:
							s1 = subnode.xpath("./td[@class='LeaseVariancePrimary_x0020_advertising_x0020_source']/text()")[0].encode('ascii', 'ignore').strip()
							if len(s1) > 0: person['Source 1'] = s1
						except:
							pass
						try:
							s2 = subnode.xpath("./td[@class='LeaseVarianceSecondary_x0020_advertising_x0020_source']/text()")[0].encode('ascii', 'ignore').strip()
							if len(s2) > 0: person['Source 2'] = s2
						except:
							pass
						
						#print "%s\t%s\t%s" % (item[0].encode('ascii', 'ignore') + " " + item[1].encode('ascii', 'ignore'), name.first, name.last)
					
					for item in f_name:
						person = {'First Name': '', 'Last Name': '', 'Phone #s': '', 'Email': '',
									'Move-In Date': '', 'Source 1': '', 'Source 2': '', 'Property': prop}
						
						text = item
						person['raw'] = re.sub('[\t\n\r]', '', text.strip())
						name = HumanName(text.encode('ascii', 'ignore').strip().split(";")[0])
						name.capitalize()
						person['First Name'] = name.first
						person['Last Name'] = name.last
						try:
							number = subnode.xpath("./td[@class='LeaseVarianceCell_x0020_Phone']/text()")[0].encode('ascii', 'ignore').strip()
							if len(number) > 0: person['Phone #s'] += "Cell: %s;" % number
						except:
							pass
						try:
							number = subnode.xpath("./td[@class='LeaseVarianceHome_x0020_Phone']/text()")[0].encode('ascii', 'ignore').strip()
							if len(number) > 0: person['Phone #s'] += "Home: %s;" % number
						except:
							pass
						try:
							number = subnode.xpath("./td[@class='LeaseVarianceWork_x0020_Phone']/text()")[0].encode('ascii', 'ignore').strip()
							if len(number) > 0: person['Phone #s'] += "Work: %s;" % number
						except:
							pass
						try:
							source = subnode.xpath("./td[@class='LeaseVariance_x0031_st_x0020_Phone_x0020_Type']/text()")[0].encode('ascii', 'ignore').strip()
							number = subnode.xpath("./td[@class='LeaseVariance_x0031_st_x0020_Phone_x0020_Number']/text()")[0].encode('ascii', 'ignore').strip()
							if len(number) > 0 and len(source) > 0: person['Phone #s'] += "%s: %s;" % (source, number)
						except:
							pass
						try:
							source = subnode.xpath("./td[@class='LeaseVariance_x0032_nd_x0020_Phone_x0020_Type']/text()")[0].encode('ascii', 'ignore').strip()
							number = subnode.xpath("./td[@class='LeaseVariance_x0032_nd_x0020_Phone_x0020_Number']/text()")[0].encode('ascii', 'ignore').strip()
							if len(number) > 0 and len(source) > 0: person['Phone #s'] += "%s: %s;" % (source, number)
						
						except:
							pass

						if person['Phone #s'].endswith(";"): person['Phone #s'] = person['Phone #s'][:-1]

						try:
							email = subnode.xpath("./td[@class='LeaseVarianceE-mail']/text()")[0].encode('ascii', 'ignore').strip()
							if len(email) > 0: person['Email'] = email
						except:
							pass
						try:
							mid = subnode.xpath("./td[@class='LeaseVarianceMove-in_x0020_date']/text()")[0].encode('ascii', 'ignore').strip()
							if len(mid) > 0: person['Move-In Date'] = mid
						except:
							pass
						try:
							s1 = subnode.xpath("./td[@class='LeaseVariance_x0031_st_x0020_advertising_x0020_source']/text()")[0].encode('ascii', 'ignore').strip()
							if len(s1) > 0: person['Source 1'] = s1
						except:
							pass
						try:
							s2 = subnode.xpath("./td[@class='LeaseVariance_x0032_nd_x0020_advertising_x0020_source']/text()")[0].encode('ascii', 'ignore').strip()
							if len(s2) > 0: person['Source 2'] = s2
						except:
							pass
						try:
							s1 = subnode.xpath("./td[@class='LeaseVariancePrimary_x0020_advertising_x0020_source']/text()")[0].encode('ascii', 'ignore').strip()
							if len(s1) > 0: person['Source 1'] = s1
						except:
							pass
						try:
							s2 = subnode.xpath("./td[@class='LeaseVarianceSecondary_x0020_advertising_x0020_source']/text()")[0].encode('ascii', 'ignore').strip()
							if len(s2) > 0: person['Source 2'] = s2
						except:
							pass
						
						
						#print "%s\t%s\t%s" % (name.strip(), name.first, name.last)
					if len(person) > 0: people.append(person)
			
			except Exception as inst:
				traceback.print_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])

			if not self.args.raw:
				with open("A-LIST.csv", 'a') as w_file:
					if len(people) > 0:
						for person in people:
							s1 = person['Source 1'].lower()
							s2 = person['Source 2'].lower()

							if ('apartment' in s1 and 'list' in s1) or ('apartment' in s2 and 'list' in s2):

								w_file.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (person['Property'], person['First Name'], person['Last Name'], person['Phone #s'], person['Email'], person['Move-In Date'], person['Source 1'], person['Source 2']))
							else:
								print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (person['Property'], person['First Name'], person['Last Name'], person['Phone #s'], person['Email'], person['Move-In Date'], person['Source 1'], person['Source 2'])
			else:
				 with open("RAW_(%s).csv" % (count/100000), 'a') as a_file:
				 	if len(people) > 0:
				 		for person in people:

				 			s1 = person['Source 1']
				 			s2 = person['Source 2']
				 			source = ''
				 			if len(s1) > 0: source = s1
				 			elif len(s2) > 0: source = s2

				 			a_file.write("%s\t%s\t%s\n" % (person['raw'].encode('ascii', 'ignore'), source, person['Property']))
				 			count += 1


			people = []


					

			
			#print node.xpath("//div[@class='CompanySite']/text()")[0]

def main():
	parser = argparse.ArgumentParser(description='')

	parser.add_argument('infile', nargs='?', type=str)

	parser.add_argument('-r', '--raw', action='store_true', default=False)

	parser.add_argument('--name', action='store_true', default=False)

	parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)

	args = parser.parse_args()

	if args.name:
		CONSTANTS.titles.remove('guru')

		with open(args.infile, 'r') as r_file:
			reader = csv.reader(r_file, delimiter="\t")
			writer = csv.writer(args.outfile)
			out = []
			for row in reader:
				name = re.sub('[\t\r\n]', '', row[0].strip()).encode('ascii', 'ignore').lower()
				name = HumanName(name)
				name.capitalize()
				writer.writerow([row[0], name.last, name.first])

		
	else:
		eagle(args.infile, args).run()


if __name__ == '__main__':
	main()