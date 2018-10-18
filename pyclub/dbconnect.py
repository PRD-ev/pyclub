import pymysql
from pymysql import escape_string
from flask_login._compat import unicode

__author__ = "Tomasz Lakomy"

def create_db():
	"""Function creates database from file create-database_pyclub.py"""
	c, conn = connection()
	c.execute("SOURCE sql/create-database_pyclub.sql")
	c.close()
	conn.close()

def connection():
	conn = pymysql.connect(host='localhost',
			       user='tykaz',
			       password='',
			       db='pyclub',
			       charset='utf8mb4',
			       cursorclass=pymysql.cursors.DictCursor)
	c = conn.cursor()
	return c, conn

def create_user(first_name, last_name, email, password):
	"""Function creates user"""
	c, conn = connection()
	c.execute("INSERT INTO user (first_name, last_name, email, password) VALUES"
			  "(%s, %s, %s, %s)"
			  , (escape_string(first_name), escape_string(last_name), escape_string(email), escape_string(password))
	)
	conn.commit()
	c.close()
	conn.close()

def create_organization(name, contact):
	"""Function creates organization"""
	c, conn = connection()
	c.execute("INSERT INTO organization (name, contact) VALUES"
			  "(%s, %s)"
			  , (escape_string(name), escape_string(contact))
	)
	conn.commit()
	c.close()
	conn.close()

def create_club(info, organization_id):
	"""Function creates club"""
	c, conn = connection()
	c.execute("INSERT INTO club (info, organization_id) VALUES"
			  "(%s, %s)"
			  , (escape_string(info), escape_string(str(organization_id)))
	)
	conn.commit()
	c.close()
	conn.close()

def create_event(date, info, club_id):
	"""Function creates event"""
	c, conn = connection()
	c.execute("INSERT INTO event (date, info, club_id) VALUES"
			  "(%s, %s)"
			  , (escape_string(date), escape_string(info), escape_string(str(club_id)))
	)
	conn.commit()
	c.close()
	conn.close()

def create_event_membership(userid, eventid, own_clubid):
	c, conn = connection()
	c.execute('INSERT INTO event_membership (user_id, event_id, own_club_id VALUES'
			  '(%s, %s, %s)' 
			  , (escape_string(str(userid)), escape_string(str(eventid)), escape_string(str(own_clubid)))
	)
	conn.commit()
	c.close()
	conn.close()

def create_club_membership(userid, clubid):
	c, conn = connection()
	c.execute('INSERT INTO club_membership (user_id, club_id) VALUES'
			  '(%s, %s)'
			  , (escape_string(str(userid)), escape_string(str(clubid)))
	)	
	conn.commit()
	c.close()
	conn.close()

def get_user(userkey):
	"""Function takes userid and returns dict with data from database"""
	c, conn = connection()
	c.execute("SELECT * FROM user WHERE iduser=%s or email=%s", (escape_string(str(userkey)), escape_string(str(userkey))))
	user_data = User()
	user_data.update(c.fetchone())
	c.close()
	conn.close()
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
	def id(self):
		c, conn = connection()
		iduser = c.execute('SELECT iduser FROM user WHERE ', self)
		c.close()
		conn.close()
		return iduser

def get_organization(organizationkey):
	c, conn = connection()
	c.execute("SELECT * FROM organization WHERE idorganization=%s or name=%s", (escape_string(str(organizationkey)), escape_string(organizationkey)))
	organization_data = c.fetchone()
	c.close()
	conn.close()
	return organization_data

def get_club(clubid):
	c, conn = connection()
	c.execute("SELECT * FROM club WHERE idclub=%s", (escape_string(str(clubid))))
	club_data = c.fetchone()
	c.close()
	conn.close()
	return club_data

def get_event(eventid):
	c, conn = connection()
	c.execute("SELECT * FROM event WHERE idevent=%s", (escape_string(str(eventid))))
	event_data = c.fetchone()
	c.close()
	conn.close()
	return event_data

def get_event_membership(membershipdata):
	c, conn = connection()
	c.execute('SELECT * FROM event_membership WHERE user_id=%s or event_id=%s or event_club_id=%s', (escape_string(str(membershipdata)), escape_string(str(membershipdata)), escape_string(str(membershipdata))))
	membershipdata = c.fetchall()
	c.close()
	conn.close()
	return membershipdata

def get_club_membership(membershipdata):
	c, conn = connection()
	c.execute('SELECT * FROM club_membership WHERE user_id=%s or club_id=%s', (escape_string(str(membershipdata)), escape_string(str(membershipdata))))
	membershipdata = c.fetchall()
	c.close()
	conn.close()
	return membershipdata

def confirm_email():
	c, conn = connection()
	c.execute('INSERT INTO user (email_confirm) values (1)')
	c.close()
	conn.close()