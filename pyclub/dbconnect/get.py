from pymysql import escape_string
from datetime import datetime, timedelta
from pyclub.dbconnect.main import connection, User

__author__ = "Tomasz Lakomy"

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

def get_event(eventname):
	"""Functions takes event id and returns event data"""
	c, conn = connection()
	c.execute("SELECT * FROM event WHERE name=%s", escape_string(str(eventname)))
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
	membership = c.fetchall()
	c.close()
	conn.close()
	return membership

def get_club_membership(clubid):
	"""Function takes clubid and returns club membership"""
	c, conn = connection()
	c.execute('SELECT * FROM club_membership WHERE club_id=%s', escape_string(str(clubid)))
	users = c.fetchall()
	c.close()
	conn.close()
	users_list = []
	for user in users:
		users_list.append(user["user_id"])
	return users_list

	
def get_user_to_club_membership(userid):
	c, conn = connection()
	c.execute('SELECT * FROM club_membership WHERE user_id=%s', escape_string(str(userid)))
	membership = c.fetchall()
	c.close()
	conn.close()
	return membership

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
