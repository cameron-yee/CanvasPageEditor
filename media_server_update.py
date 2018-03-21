import ftplib

if __name__ == '__main__':
	ftp = ftplib.FTP('***REMOVED***', '***REMOVED***', '***REMOVED***')
	ftp.cwd('media/canvas/mhs/te/css')
	file = open('/Users/cameronyee/Desktop/canvas/courses/mhs/resources/te/styles/css/concat/concat.css','rb')
	print(file)
	ftp.storbinary('STOR /Users/cameronyee/Desktop/canvas/courses/mhs/resources/te/styles/css/concat/concat.css', file)
	file.close()
	session.quit()
	
	

