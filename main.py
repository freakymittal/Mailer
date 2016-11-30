import lib
from lib.extractor.merge import file_merge
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from pyisemail import is_email
def file_read(input_file, mode='r', split=''):
	result = []
	for line in open(input_file, mode):
		result.append(line.replace('\n',"").split(split) if split else line.replace('\n',""))
	return result
def make_connections(credentials):
	i = 0
	connections = []
	for row in credentials:
		try:
			connections.append(lib.smtplib.SMTP(row[2], row[3]))
			connections[i].ehlo()
			connections[i].starttls()
			connections[i].login(row[0],row[1])
			connections[i].set_debuglevel(0)
		except IOError:
			print IOError
		i += 1
	return connections
credentials = file_read('credential.txt', 'r', ',')
subject = file_read('subject.txt')
done = open("done.txt", "a+", 0)
file_merge("./whitelist/", "whitelist") #Combines whitelists if more than one.
whitelist = file_read('./whitelist/whitelist.txt')
ifdone = file_read('done.txt')
connections = make_connections(credentials)
with open('message.txt', 'r') as myfile:
	message = myfile.read()
invalid_emails = open("./whitelist/whitelist.txt", "a+", 0)
if len(lib.os.listdir('./recipients/'))>0:
	if len(lib.os.listdir('./recipients/'))>1:
		lib.emailextractor('./recipients/')
else:
	print "Please add atleast one file which includes some Email addresses."
j = 0
def send_mail():
	msg = MIMEMultipart()
	msg['Subject'] = lib.choice(subject)
	msg['From'] = credentials[j][0]
	msg['To'] = line
	msg.attach(MIMEText(message, 'html'))
	for file in lib.os.listdir("./attachments/"):
		with open("./attachments/" + file, "rb") as f:
			part = MIMEApplication(f.read(), Name=lib.os.path.basename(file))
			part['Content-Disposition'] = 'attachment; filename="%s"' % lib.os.path.basename(file)	
			msg.attach(part)
	try:
		connections[j].sendmail(credentials[j][0], line, msg.as_string())
		print "Sent to " + line
		done.write(line+"\n")
		ifdone.append(line)
	except Exception, e:
		print str(e)
if is_email("mayank_mittal@outlook.com", check_dns=True):
	for line in open('./recipients/Emails.txt','r'):
		if(j >= len(credentials)):
			j = 0
		line = line.replace('\n', "")
		if (line not in whitelist) and (line not in ifdone):
			if is_email(line, check_dns=True):
				send_mail()
				j += 1
			else:
				invalid_emails.write(line+"\n")
else:
	for line in open('./recipients/Emails.txt','r'):
		if(j >= len(credentials)):
			j = 0
		line = line.replace('\n', "")
		if (line not in whitelist) and (line not in ifdone):
				send_mail()
				j += 1
