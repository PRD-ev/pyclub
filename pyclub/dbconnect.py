import pymysql
from pymysql import escape_string
from flask_login._compat import unicode
from datetime import datetime, timedelta

__author__ = "Tomasz Lakomy"

def connection():
	"""Function connects to database"""
	conn = pymysql.connect(host='localhost',
			       user='tykaz',
			       password='',
			       db='pyclub',
			       charset='utf8mb4',
			       cursorclass=pymysql.cursors.DictCursor)
	c = conn.cursor()
	return c, conn

def create_user(first_name, last_name, email, password):
	"""Function takes first name, last name, email and password and creates user in database"""
	c, conn = connection()
	c.execute("INSERT INTO user (first_name, last_name, email, password) VALUES"
			  "(%s, %s, %s, %s)"
			  , (escape_string(first_name), escape_string(last_name), escape_string(email), escape_string(password))
	)
	conn.commit()
	c.close()
	conn.close()

def create_organization(name, contact):
	"""Function takes name and contact and creates organization in database"""
	c, conn = connection()
	c.execute("INSERT INTO organization (name, contact) VALUES"
			  "(%s, %s)"
			  , (escape_string(name), escape_string(contact))
	)
	conn.commit()
	c.close()
	conn.close()

def create_club(info, organization_id, name):
	"""Function takes info and organization id, creates and assigns club to organization in database"""
	c, conn = connection()
	c.execute("INSERT INTO club (info, organization_id, name) VALUES"
			  "(%s, %s, %s)"
			  , (escape_string(info), escape_string(str(organization_id)), escape_string(name))
	)
	conn.commit()
	c.close()
	conn.close()

def create_event(date, info, club_id):
	"""Function takes date (yyyy-mm-dd hh:mm:ss) information and club id, creates event and assigns to club in database"""
	c, conn = connection()
	c.execute("INSERT INTO event (date, info, club_id) VALUES"
			  "(%s, %s, %s)"
			  , (escape_string(str(date)), escape_string(info), escape_string(str(club_id)))
	)
	conn.commit()
	c.close()
	conn.close()

def create_event_membership(userid, eventid):
	"""Function takes user id, event id and club which is owner of the event and assigns user to event"""
	c, conn = connection()
	c.execute('INSERT INTO event_membership (user_id, event_id) VALUES'
			  '(%s, %s)'
			  , (escape_string(str(userid)), escape_string(str(eventid)))
	)
	conn.commit()
	c.close()
	conn.close()

def create_club_membership(userid, clubid):
	"""Function takes user id, club id and assigns user to that club"""
	c, conn = connection()
	c.execute('INSERT INTO club_membership (user_id, club_id) VALUES'
			  '(%s, %s)'
			  , (escape_string(str(userid)), escape_string(str(clubid)))
	)
	conn.commit()
	c.close()
	conn.close()

def del_user(userid):
	"""Function takes user's id and deletes it from database
		tip: check dependencies before deleting
	"""
	c, conn = connection()
	c.execute('DELETE FROM user WHERE iduser=%s', (escape_string(str(userid))))
	conn.commit()
	c.close()
	conn.close()

def del_organization(organizationid):
	"""Function takes organization's id and deletes it from database
		tip: check dependencies before deleting
	"""
	c, conn = connection()
	c.execute('DELETE FROM organization WHERE idorganization=%s', (escape_string(str(organizationid))))
	conn.commit()
	c.close()
	conn.close()

def del_club(clubid):
	"""Function takes club's id and deletes it from database
		tip: check dependencies before deleting
	"""
	c, conn = connection()
	c.execute('DELETE FROM club WHERE idclub=%s', (escape_string(str(clubid))))
	conn.commit()
	c.close()
	conn.close()

def del_event(eventid):
	"""Function takes event's id and deletes it from database
		tip: check dependencies before deleting
	"""
	c, conn = connection()
	c.execute('DELETE FROM event WHERE idevent=%s', (escape_string(str(eventid))))
	conn.commit()
	c.close()
	conn.close()

def del_user_from_club(userid, clubid):
	"""Functions takes user's id and club's id and removes user from that club"""
	c, conn = connection()
	c.execute('DELETE FROM club_membership WHERE user_id=%s and club_id=%s', (escape_string(str(userid)), escape_string(str(userid))))
	conn.commit()
	c.close()
	conn.close()

def del_user_from_event(userid, eventid):
	"""Functions takes user's id and event's id and removes user from that event"""
	c, conn = connection()
	c.execute('DELETE FROM event_membership WHERE user_id=%s and event_id=%s', (escape_string(str(userid)), escape_string(str(userid))))
	conn.commit()
	c.close()
	conn.close()

def get_user(userkey):
	"""Function takes user's id or user's email and returns dict with data from database"""
	c, conn = connection()
	c.execute("SELECT * FROM user WHERE iduser=%s or email=%s", (escape_string(str(userkey)), escape_string(str(userkey))))
	execute = (c.fetchone())
	if execute is None:
		return None
	user_data = User()
	user_data.update(execute)
	c.close()
	conn.close()
	user_data.id = user_data['iduser']
	return user_data

class User(dict):
	def is_authenticated(self):
		return True
	def is_active(self):
		return True
	def is_anonymus(self):
		return True
	def get_id(self):
		return unicode(self['iduser'])
	def userid(self, userkey):
		self.id = userkey

def get_organization_by_name(organizationname):
	"""Function takes organization name and returns dict with organization's data"""
	c, conn = connection()
	c.execute("SELECT * FROM organization WHERE name=%s", escape_string(organizationname))
	organization_data = c.fetchone()
	c.close()
	conn.close()
	return organization_data

def get_organization_by_id(organizationid):
	"""Function takes organization id and returns dict with organization's data"""
	c, conn = connection()
	c.execute("SELECT * FROM organization WHERE idorganization=%s", escape_string(str(organizationid)))
	organization_data = c.fetchone()
	c.close()
	conn.close()
	return organization_data

def get_club(clubname):
	"""Function takes club name and returns club data"""
	c, conn = connection()
	c.execute("SELECT * FROM club WHERE name=%s", escape_string(str(clubname)))
	club_data = c.fetchone()
	c.close()
	conn.close()
	return club_data

def get_club_by_organization(organizationid):
	c, conn = connection()
	c.execute("SELECT name FROM club WHERE organization_id=%s", escape_string(str(organizationid)))
	club_data = c.fetchall()
	c.close()
	conn.close()
	return club_data

def get_event(eventid):
	"""Functions takes event id and returns event data"""
	c, conn = connection()
	c.execute("SELECT * FROM event WHERE idevent=%s", escape_string(str(eventid)))
	event_data = c.fetchone()
	c.close()
	conn.close()
	return event_data

def get_event_membership(eventid):
	"""Function takes userid or eventid and returns event membership"""
	c, conn = connection()
	c.execute('SELECT * FROM event_membership WHERE event_id=%s', escape_string(str(eventid)))
	eventid = c.fetchall()
	c.close()
	conn.close()
	return eventid

def get_user_to_event_membership(userid):
	c, conn = connection()
	c.execute('SELECT * FROM event_membership WHERE user_id=%s', escape_string(str(userid)))
	userid = c.fetchall()
	c.close()
	conn.close()
	return userid

def get_club_membership(clubid):
	"""Function takes clubid and returns club membership"""
	c, conn = connection()
	c.execute('SELECT * FROM club_membership WHERE club_id=%s', escape_string(str(clubid)))
	clubid = c.fetchall()
	c.close()
	conn.close()
	return clubid

def get_user_to_club_membership(userid):
	c, conn = connection()
	c.execute('SELECT * FROM club_membership WHERE user_id=%s', escape_string(str(userid)))
	userid = c.fetchall()
	c.close()
	conn.close()
	return userid

def get_event_next_week():
	"""Functions shows events from the next week
			returns: list with events planned to next week
	"""
	today = datetime.today()
	weekday = today.weekday()
	days_to = 6 - weekday
	start_time = today + timedelta(days=days_to)
	end_time = start_time + timedelta(days=7)
	c, conn = connection()
	c.execute('SELECT idevent FROM event WHERE date>%s and date<=%s', (start_time, end_time))
	event_data = c.fetchall()
	c.close()
	conn.close()
	return event_data

def get_event_current_week():
	"""Functions shows events from the current week
	
			returns: list with events planned to current week
	"""
	today = datetime.today()
	weekday = today.weekday()
	days_left = 6-weekday
	time = today + timedelta(days=days_left)
	c, conn = connection()
	c.execute('SELECT idevent FROM event WHERE date<%s and date>%s', (time, today))
	event_data = c.fetchall()
	c.close()
	conn.close()
	return event_data

def get_event_next_month():
	"""Functions shows events from the current week
	
			returns: list of events planned to next month
	"""
	today = datetime.today()
	time = today + timedelta(days=30)
	c, conn = connection()
	c.execute('SELECT idevent FROM event WHERE date<=%s and date>%s', (time, today))
	event_data = c.fetchall()
	c.close()
	conn.close()
	return event_data

def get_further_events(userid):
	""" """
	c, conn = connection()
	today = datetime.today()
	c.execute('SELECT idevent FROM event WHERE date>=%s', (today))
	event_data = c.fetchall()
	c.close()
	conn.close()
	return event_data

def confirm_email(mail):
	'''Function confirms user's mail'''
	c, conn = connection()
	c.execute('UPDATE user SET email_confirm=1 WHERE email=%s', escape_string(str(mail)))
	conn.commit()
	c.close()
	conn.close()

def give_admin(userid):
	c, conn = connection()
	c.execute('UPDATE user SET admin=1 WHERE iduser=%s', (escape_string(str(userid))))
	conn.commit()
	c.close()
	conn.close()

def change_mail(userid, new_mail):
	c, conn = connection()
	c.execute('UPDATE user SET email=%s WHERE iduser=%s', (escape_string(new_mail), escape_string(str(userid))))
	c.execute('UPDATE user SET email_confirm=0 WHERE iduser=%s', escape_string(str(userid)))	
	conn.commit()
	c.close()
	conn.close()

def change_event_info(eventid, new_info):
	c, conn = connection()
	c.execute('UPDATE event SET info=%s WHERE idevent=%s', (escape_string(new_info), escape_string(str(str(eventid)))))
	conn.commit()
	c.close()
	conn.close()

def change_organization_contact(organizationid, new_contact):
	c, conn = connection()
	c.execute('UPDATE organization SET contact=%s WHERE idorganization=%s', (escape_string(new_contact), escape_string(str(str(organizationid)))))
	conn.commit()
	c.close()
	conn.close()

def change_user_password(userid, new_password):
	c, conn = connection()
	c.execute('UPDATE user SET password=%s WHERE iduser=%s', (escape_string(new_password), escape_string(str(str(userid)))))
	conn.commit()
	c.close()
	conn.close()

def change_event_date(eventid, new_date):
	c, conn = connection()
	c.execute('UPDATE event SET date=%s WHERE idevent=%s', (escape_string(new_date), escape_string(str(str(eventid)))))
	conn.commit()
	c.close()
	conn.close()
