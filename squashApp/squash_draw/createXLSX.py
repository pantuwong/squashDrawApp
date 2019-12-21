import xlsxwriter

def createXLSXSchedule( data, path):
	# Create an new Excel file and add a worksheet.
	workbook = xlsxwriter.Workbook('{}/schedule_{}.xlsx'.format( path, data['date'].replace('/','_',3) ))
	worksheet = workbook.add_worksheet()

	# Set size of column
	worksheet.set_column( 'A:A', 3 )
	worksheet.set_column( 'B:B', 8 )
	worksheet.set_column( 'C:C', 18 )
	worksheet.set_column( 'D:D', 8 )
	worksheet.set_column( 'E:E', 2 )
	worksheet.set_column( 'F:F', 8 )
	worksheet.set_column( 'G:G', 18 )
	worksheet.set_column( 'H:H', 8 )

	# Merge cell to create title
	merge_format = workbook.add_format({
		'border': 1,
		'align': 'center',
		'valign': 'vcenter',
		'fg_color': '#003366',
		'font_color': 'white',
		'font_name': 'Calibri',
		'font_size': 28,
	})
	worksheet.merge_range('B1:H3', 'Whakatane Ladder Competition', merge_format)

	# Merge cell to create date
	merge_format = workbook.add_format({
		'bold': True,
		'align': 'center',
		'valign': 'center',
		'fg_color': 'white',
		'font_color': 'black',
		'font_name': 'Calibri',
		'font_size': 14
	})
	worksheet.merge_range('B4:H5', 'Draw: {}'.format( data['date'] ), merge_format)

	# Merge cell to create Junior and Senior Title
	merge_format = workbook.add_format({
		'bold': 1,
		'border': 2,
		'align': 'center',
		'valign': 'vcenter',
		'fg_color': '#003366',
		'font_color': 'white',
		'font_name': 'Calibri',
		'font_size': 11,
	})
	worksheet.merge_range('B6:D6', 'Seniors', merge_format)
	worksheet.merge_range('F6:H6', 'Juniors', merge_format)

	# set E6 with color
	blue_bg_border = workbook.add_format({'fg_color':'#003366', 'border':2})
	worksheet.write('E6', '', blue_bg_border)

	# write match data
	base_row = 7
	style1 = workbook.add_format({'left':2, 'top':2, 'right':1, 'bottom':1, 'align':'center', 'valign':'vcenter'})
	style2 = workbook.add_format({'left':1, 'top':2, 'right':1, 'bottom':1, 'align':'center', 'valign':'vcenter'})
	style3 = workbook.add_format({'left':1, 'top':2, 'right':2, 'bottom':1, 'align':'center', 'valign':'vcenter'})
	style4 = workbook.add_format({'left':2, 'top':1, 'right':1, 'bottom':1, 'align':'center', 'valign':'vcenter'})
	style5 = workbook.add_format({'left':1, 'top':1, 'right':1, 'bottom':1, 'align':'center', 'valign':'vcenter'})
	style6 = workbook.add_format({'left':1, 'top':1, 'right':2, 'bottom':1, 'align':'center', 'valign':'vcenter'})
	style7 = workbook.add_format({'left':2, 'top':1, 'right':1, 'bottom':1, 'align':'center', 'valign':'vcenter'})
	style8_ok = workbook.add_format({'left':1, 'top':1, 'right':1, 'bottom':1, 'align':'left', 'valign':'vcenter', 'fg_color':'#99CCFF'})
	style8_break = workbook.add_format({'left':1, 'top':1, 'right':1, 'bottom':1, 'align':'left', 'valign':'vcenter', 'fg_color':'#FF8080'})
	style9 = style5 = workbook.add_format({'left':1, 'top':1, 'right':2, 'bottom':1, 'align':'left', 'valign':'vcenter'})
	style10 = workbook.add_format({'left':2, 'top':1, 'right':1, 'bottom':2, 'align':'center', 'valign':'vcenter'})
	style11 = workbook.add_format({'left':1, 'top':1, 'right':1, 'bottom':2, 'align':'left', 'valign':'vcenter'})
	style12 = workbook.add_format({'left':1, 'top':1, 'right':2, 'bottom':2, 'align':'center', 'valign':'vcenter'})
	
	for index in range(max(len(data['senior']),len(data['junior']))):
		# add senior
		if index <= len(data['senior'])-1:
			worksheet.write('B'+str(base_row), 'Position', style1)
			worksheet.write('C'+str(base_row), '', style2)
			worksheet.write('D'+str(base_row), 'Score', style3)
			worksheet.write('B'+str(base_row+1),data['senior'][index]['p1rank'], style4)
			worksheet.write('C'+str(base_row+1),data['senior'][index]['p1name'], style5)
			worksheet.write('D'+str(base_row+1),data['senior'][index]['p1score'], style6)
			worksheet.write('B'+str(base_row+2), '', style7)
			if data['senior'][index]['break_rule']:
				worksheet.write('C'+str(base_row+2), data['senior'][index]['time'], style8_break)
			else:
				worksheet.write('C'+str(base_row+2), data['senior'][index]['time'], style8_ok)
			worksheet.write('D'+str(base_row+2), '', style9)
			worksheet.write('B'+str(base_row+3),data['senior'][index]['p2rank'], style10)
			worksheet.write('C'+str(base_row+3),data['senior'][index]['p2name'], style11)
			worksheet.write('D'+str(base_row+3),data['senior'][index]['p2score'], style12)
		
		# add junior
		if index <= len(data['junior'])-1:
			worksheet.write('F'+str(base_row), 'Position', style1)
			worksheet.write('G'+str(base_row), '', style2)
			worksheet.write('H'+str(base_row), 'Score', style3)
			worksheet.write('F'+str(base_row+1),data['junior'][index]['p1rank'], style4)
			worksheet.write('G'+str(base_row+1),data['junior'][index]['p1name'], style5)
			worksheet.write('H'+str(base_row+1),data['junior'][index]['p1score'], style6)
			worksheet.write('F'+str(base_row+2), '', style7)
			if data['junior'][index]['break_rule']:
				worksheet.write('G'+str(base_row+2), data['junior'][index]['time'], style8_break)
			else:
				worksheet.write('G'+str(base_row+2), data['junior'][index]['time'], style8_ok)
			worksheet.write('H'+str(base_row+2), '', style9)
			worksheet.write('F'+str(base_row+3),data['junior'][index]['p2rank'], style10)
			worksheet.write('G'+str(base_row+3),data['junior'][index]['p2name'], style11)
			worksheet.write('H'+str(base_row+3),data['junior'][index]['p2score'], style12)

		base_row += 4

	workbook.close()

# data = {
# 	'date': '23/10/2019',
# 	'senior':[
# 		{
# 			'p1rank': '1',
# 			'p1name': 'p1s',
# 			'p1score': '',
# 			'time': '1:00PM',
# 			'p2rank': '2',
# 			'p2name': 'p2s',
# 			'p2score': '',
# 			'break_rule': False

# 		},
# 		{
# 			'p1rank': '3',
# 			'p1name': 'p1ss',
# 			'p1score': '',
# 			'time': '1:30PM',
# 			'p2rank': '4',
# 			'p2name': 'p2ss',
# 			'p2score': '',
# 			'break_rule': True

# 		}
# 	],
# 	'junior':[
# 		{
# 			'p1rank': '1',
# 			'p1name': 'p1s',
# 			'p1score': '',
# 			'time': '2:00PM',
# 			'p2rank': '2',
# 			'p2name': 'p2s',
# 			'p2score': '',
# 			'break_rule': False

# 		},
# 	]
# }

# createXLSXSchedule( data, './')