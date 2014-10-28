import requests
import bs4
import re
import xlwt
import xlrd
import sys
from os import listdir
from os.path import isfile, join


root_url = "http://www.granadatile.com/portfolio/"

def get_customers_links(root_url):
	response = requests.get(root_url)
	soup = bs4.BeautifulSoup(response.text)
	customers_list = soup.select('a[href^=?user]')
	users = [a.attrs.get('href') for a in customers_list]
	dates = [a.next_element.next_element.get_text() for a in customers_list]
	return zip(dates,users)


def get_customer_data(date, user):
	customer_data = {}
	response = requests.get(root_url + user)
	soup = bs4.BeautifulSoup(response.text)
	customer_data['date'] = date
	customer_data['user'] = soup.select('tr > td > div')[0].get_text().rsplit(':')[1][:-4]
	customer_data['name'] = soup.select('tr > td > div')[0].get_text().rsplit(':')[2][:-7]
	customer_data['address'] = soup.select('tr > td > div')[0].get_text().rsplit(':')[3][:-5]
	customer_data['phone'] = soup.select('tr > td > div')[0].get_text().rsplit(':')[4][:-5]
	customer_data['email'] = soup.select('tr > td > div')[0].get_text().rsplit(':')[5][:-7]
	customer_data['company'] = soup.select('tr > td > div')[0].get_text().rsplit(':')[6]
	tiles_list = soup.find_all(title=re.compile("Send to Granada Tile"))
	final_tile_list = []
	for tile in tiles_list:
		final_tile_list.append(tile.next_element)
	customer_data['tiles'] = final_tile_list
	return customer_data


def combine():
	xlsfiles = [ f for f in listdir('xls') if isfile(join('xls',f)) ]
	wkbk = xlwt.Workbook()
	outsheet = wkbk.add_sheet('Granada tiles')
	outrow_idx = 0
	firstfile = True
	for f in xlsfiles:
		insheet = xlrd.open_workbook('xls/' + f).sheets()[0]
		for row_idx in xrange(0 if firstfile else 1, insheet.nrows):
			for col_idx in xrange(insheet.ncols):
				outsheet.write(outrow_idx, col_idx, insheet.cell_value(row_idx, col_idx))
			outrow_idx += 1
		firstfile = False
	wkbk.save(r'boaz.xls')


def main(file_start):
	a = get_customers_links(root_url)
	file_start = int(file_start)
	file_end = int(file_start) + 200
#	counter = 1
#	while counter < 16:
	totalrow = 0
	book = xlwt.Workbook(encoding='utf8')
	sheet = book.add_sheet('Granada tiles', cell_overwrite_ok=True)
	header_style = xlwt.easyxf('font:height 280, color blue, bold 1; border: bottom thick;')
	sheet.write(0, 0, 'DATE', header_style)
	sheet.write(0, 1, 'USER', header_style)
	sheet.write(0, 2, 'NAME', header_style)
	sheet.write(0, 3, 'ADDRESS', header_style)
	sheet.write(0, 4, 'PHONE', header_style)
	sheet.write(0, 5, 'EMAIL', header_style)
	sheet.write(0, 6, 'COMPANY', header_style)
	sheet.write(0, 7, 'TILES', header_style)
	for i in a[file_start:file_end]:
		totalrow += 1
		print totalrow,
		x = get_customer_data(i[0], i[1])
		headers = ("user", "name", "address", "phone", "email", "company", "tiles")
		sheet.write(totalrow, 0, x['date'])
		sheet.write(totalrow, 1, x['user'])
		sheet.write(totalrow, 2, x['name'])
		sheet.write(totalrow, 3, x['address'])
		sheet.write(totalrow, 4, x['phone'])
		sheet.write(totalrow, 5, x['email'])
		sheet.write(totalrow, 6, x['company'])
		sheet.write(totalrow, 7, x['tiles'])
	book.save('xls/boaz' + str(file_start) + '-' + str(file_end) + '.xls')
	print "Finish reading from %d to %d successfully." % (file_start, file_end)
#	file_start = file_end
#	file_end += 200
#	counter += 1


if __name__=="__main__":
	if len(sys.argv) < 2:
		print 'You need to provide arguments [like: digit or "combine"]'
		sys.exit(1)
	elif sys.argv[1].isdigit():
		main(sys.argv[1])
	elif sys.argv[1] == 'combine':
		combine()
	else:
		print 'Wrong argument, digit or "combine" only.'
		sys.exit(1)
