from users import show_dict, month
import urllib2
from lxml import html
from datetime import datetime
from send_mail import send_mail

current_day = datetime.now().day
current_month = datetime.now().strftime("%B")
if len(current_month) > 3:
	current_month = current_month[:3]+ "."
current_year = datetime.now().year


def set_episode_structure(text):
	"""
	Set episode structure

	Reciving text : S1, Ep10
	Output : S01E10
	"""
	# CONDITION : IF EMPTY THEN RETURN
	if not text:
		return

	# CONDITION : IF ", " IN TEXT
	if ", " in text:

		# Split by ", " 
		# if season is in one digit "1 or 2" replace by "01, 02"
		# if Episode in single digit "5 or 6" replace by "05, 06" and "Ep" by "E"
		episode = text.split(", ")
		if len(episode[0]) == 2:
			episode[0] = episode[0].replace("S", "S0")
		if len(episode[1]) == 3:
			episode[1] = episode[1].replace("Ep", "E0")
		elif len(episode[1]) == 4:
			episode[1] = episode[1].replace("Ep", "E")

		return ''.join(episode)

def get_release_dates(show):
	"""
	get release dates of specific year of specific shows.

	Scraping data from imdb
	"""

	try:
		# Get webpage from imdb
		source = urllib2.urlopen(show_dict[show]).read()

		# Store show name in season_name
		season_name = show

		# MAke a lxml tree
		tree = html.document_fromstring(source)

		seasons = tree.cssselect("div.seasons-and-year-nav")

		# Get all links and get the link of current year so we can parse all episode of current year list
		for links in  seasons[0].iterlinks():
			if str(current_year) in links[2]:
				href = links[2]

		href =  "http://www.imdb.com"+ href

		# Get Page for listing of all the episodes of current year
		source = urllib2.urlopen(href).read()

		tree = html.document_fromstring(source)

		# get air date so we can add episodes that will come in future ( after current date)
		airdate = tree.cssselect("div.info div.airdate")
		is_date = False

		# open a text file as "show.txt" to write season name seasonNo and Episodde no to come
		f = open("/home/gaurav/workspace/show-scrapper/showdir/"+season_name+".txt", "wb")
		print season_name
		# Get episode No
		for date in airdate:
			season_ep = set_episode_structure(date.getparent().getprevious().cssselect("a div")[1].text)

			if not is_date:
				date =  date.text.strip().split()
				date[1] = month[date[1]]
				date[2] = date[2].replace('20', '')
				d = ("/").join(date)
				season_date = datetime.strptime(d, '%d/%m/%y')
				if season_date > datetime.now():
					is_date = True
					f.write(season_name+ " "+season_ep+ "\n")
				else:
					print season_date
			else:
				f.write(season_name+ " "+season_ep+ "\n")
		if not is_date:
			f.write("no info")

	except Exception as e:
		print e