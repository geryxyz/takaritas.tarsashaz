import datetime
import random
import pdb
import io

list_of_flat = [1,2,3,4,5,6,7,8]
name_of_months = ['január', 'február', 'március', 'április', 'május', 'június', 'július', 'augusztus', 'szeptember', 'október', 'november', 'december']

def generate_list(duration):
	index = 0
	start_day = first_monday
	whole_list = []
	per_flat = {}
	while start_day.year == current_year:
		end_day = start_day + duration - datetime.timedelta(days=1)
		current_flat = current_rank_inner[index % len(list_of_flat)]
		if current_flat not in per_flat:
			per_flat[current_flat] = []
		period = (start_day, end_day)
		per_flat[current_flat].append(period)
		whole_list.append((current_flat, period))
		#print("flat #%d -> %s - %s" % (current_flat, period[0], period[1]))
		index += 1
		start_day += duration
	return whole_list, per_flat

def create_month_matrix(whole_list):
	month_matrix = {}
	for item in whole_list:
		month = item[1][0].month
		if month not in month_matrix:
			month_matrix[month] = {}
		flat = item[0]
		month_matrix[month][flat] = item[1]
	return month_matrix

def write_table(output_file, month_matrix):
	output_file.write('<table>\n')
	output_file.write('<th>')
	output_file.write(''.join(['<td>%d. lakás</td>' % flat for flat in list_of_flat]))
	output_file.write('</th>\n')
	for month, periods in month_matrix.items():
		output_file.write('<tr>')
		output_file.write('<td>')
		output_file.write(name_of_months[month-1])
		output_file.write('</td>')
		for flat in list_of_flat:
			output_file.write('<td>') 
			if flat in periods:
				output_file.write('%s - %s' % (periods[flat][0].strftime('%m. %d.'), periods[flat][1].strftime('%m. %d.')))
			output_file.write('</td>') 
		output_file.write('</tr>\n')
	output_file.write('</table>\n')

def write_html_init(output_file):
	output_file.write('<!doctype html>\n')
	output_file.write('<html>\n')
	output_file.write('<head>\n')
	output_file.write('<link rel="stylesheet" type="text/css" href="theme.css">\n')
	output_file.write('</head>\n')
	output_file.write('<body>\n')

def write_html_teardown(output_file):
	output_file.write('</body>\n')
	output_file.write('</html>\n')

def write_per_flat(output_file, per_flat_list):
	output_file.write('<div class="multi">')
	for flat in list_of_flat:
		periods = per_flat_list[flat]
		output_file.write('<div class="per_flat">') 
		output_file.write('<h2>%d. lakás</h2>\n' % flat)
		output_file.write('<ol>\n')
		for period in periods:
			output_file.write('<li>%s - %s</li>' % period)
		output_file.write('</ol>\n')
		output_file.write('</div>')
	output_file.write('</div>')

def write_current(output_file, whole_list):
	output_file.write('<p class="current">')
	output_file.write('<script>')
	if datetime.datetime.now().date() < first_monday:
		print("DEMO MODE") 
		output_file.write("""
			document.write("DEMO MODE ");
			now = new Date(2019, 1, 19, 0,0,0,0);""")
	else:
		output_file.write("""
			now = new Date();""")
	for flat, period in whole_list:
		start = period[0]
		stop = period[1]
		output_file.write("""
			start = new Date("%s");
			stop = new Date("%s");
			if (start <= now && now <= stop) {
				document.write("Jelenleg a %d. lakás feladata.");
			}""" % (start.strftime('%Y-%m-%d'), stop.strftime('%Y-%m-%d'), flat))
	output_file.write('</script>')
	output_file.write('</p>')

if __name__ == '__main__':
	current_year = datetime.datetime.now().year
	first_monday = datetime.date(current_year, 1, 1)
	while first_monday.weekday() != 0:
		first_monday += datetime.timedelta(days=1)
	print("first monday is: %s" % first_monday)

	#comment these, rerun, set to new values
	current_rank_inner = [3, 6, 5, 1, 8, 2, 4, 7]
	current_rank_outer = [6, 5, 1, 2, 3, 8, 4, 7]

	if not current_rank_inner or not current_rank_outer:
		current_rank_inner = [i for i in list_of_flat]
		current_rank_outer = [i for i in list_of_flat]
		random.shuffle(current_rank_inner)
		random.shuffle(current_rank_outer)
	print("order for inner cleaning: " + ", ".join(map(str,current_rank_inner)))
	print("order for outer cleaning: " + ", ".join(map(str,current_rank_outer)))

	inner_all, inner_per_flat = generate_list(datetime.timedelta(days=7))
	outer_all, outer_per_flat = generate_list(datetime.timedelta(days=14))

	with io.open('inner_all_flat.html', 'w', encoding='utf-8') as all_flat:
		write_html_init(all_flat)

		all_flat.write('<a href="index.html">Vissza a kezdő oldalra.</a>\n')

		all_flat.write('<h1>Lépcsőház takarítás beosztása</h1>')
		all_flat.write('<p>Az adott lakás lakói felelősek a takarításért a táblázatban megadott időszakban.<br/>Idei véletlenszerű sorrend: %s</p>' % ', '.join(['%d. lakás' % flat for flat in current_rank_inner]))
		month_matrix = create_month_matrix(inner_all)
		write_table(all_flat, month_matrix)
		
		all_flat.write('<p><img style="width:100px" src="qrcode.png"/>A beosztás elérhető az interneten is: https://geryxyz.github.io/takaritas.tarsashaz/</p>')

		write_html_teardown(all_flat)

	with io.open('outer_all_flat.html', 'w', encoding='utf-8') as all_flat:
		write_html_init(all_flat)

		all_flat.write('<a href="index.html">Vissza a kezdő oldalra.</a>\n')

		all_flat.write('<h1>Udvar és előkert takarítás beosztása</h1>')
		all_flat.write('<p>Az adott lakás lakói felelősek a takarításért a táblázatban megadott időszakban.<br/>Idei véletlenszerű sorrend: %s</p>' % ', '.join(['%d. lakás' % flat for flat in current_rank_outer]))
		month_matrix = create_month_matrix(outer_all)
		write_table(all_flat, month_matrix)
		
		all_flat.write('<p><img style="width:100px" src="qrcode.png"/>A beosztás elérhető az interneten is: https://geryxyz.github.io/takaritas.tarsashaz/</p>')

		write_html_teardown(all_flat)

	with io.open('inner_per_flat.html', 'w', encoding='utf-8') as per_flat:
		write_html_init(per_flat)
		
		per_flat.write('<a href="index.html">Vissza a kezdő oldalra.</a>\n')

		per_flat.write('<h1>Lépcsőház takarítás beosztása</h1>')
		per_flat.write('<p>Kivágható lakásonkénti beosztása.</p>')
		write_per_flat(per_flat, inner_per_flat)
		
		write_html_teardown(per_flat)

	with io.open('outer_per_flat.html', 'w', encoding='utf-8') as per_flat:
		write_html_init(per_flat)
		
		per_flat.write('<a href="index.html">Vissza a kezdő oldalra.</a>\n')

		per_flat.write('<h1>Udvar és előkert takarítás beosztása</h1>')
		per_flat.write('<p>Kivágható lakásonkénti beosztása.</p>')
		write_per_flat(per_flat, outer_per_flat)
		
		write_html_teardown(per_flat)

	with io.open('index.html', 'w', encoding='utf-8') as index:
		write_html_init(index)

		index.write('<h1>Lépcsőház takarítás beosztása</h1>\n')
		write_current(index, inner_all)

		index.write('<h2>Részletes beosztás</h2>\n')
		index.write('<p>Lépcsőház takarítás teljes (minden lakás) beosztása <a href="inner_all_flat.html">ide kattintva</a> érhető el.</p>\n')
		index.write('<p>Lépcsőház takarítás lakásonkénti beosztása <a href="inner_per_flat.html">ide kattintva</a> érhető el.</p>\n')

		index.write('<h1>Udvar és előkert takarítás beosztása</h1>\n')
		write_current(index, outer_all)

		index.write('<h2>Részletes beosztás</h2>\n')
		index.write('<p>Udvar és előkert takarítás teljes (minden lakás) beosztása <a href="outer_all_flat.html">ide kattintva</a> érhető el.</p>\n')
		index.write('<p>Udvar és előkert takarítás lakásonkénti beosztása <a href="outer_per_flat.html">ide kattintva</a> érhető el.</p>\n')

		index.write('<img style="width:200px" src="qrcode.png"/>')

		write_html_teardown(index)