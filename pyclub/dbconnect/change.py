from pymysql import escape_string
from pyclub.dbconnect.main import connection

__author__ = "Tomasz Lakomy"

def confirm_email(mail):
	'''Function confirms user's mail'''
	c, conn = connection()
	c.execute('UPDATE user SET email_confirm=1 WHERE email=%s', escape_string(str(mail)))
	conn.commit()
	c.close()
	conn.close()

def give_admin(userid):
	'''Function takes userid and gives him all priviliges'''
	c, conn = connection()
	c.execute('UPDATE user SET admin=1 WHERE iduser=%s', (escape_string(str(userid))))
	conn.commit()
	c.close()
	conn.close()

def change_mail(userid, new_mail):
	'''Function takes userid and new mail and changes specified user mail'''
	c, conn = connection()
	c.execute('UPDATE user SET email=%s WHERE iduser=%s', (escape_string(new_mail), escape_string(str(userid))))
	c.execute('UPDATE user SET email_confirm=0 WHERE iduser=%s', escape_string(str(userid)))
	conn.commit()
	c.close()
	conn.close()

def change_event_info(eventid, new_info):
	'''Function takes eventid and new info and changes specified event info'''
	c, conn = connection()
	c.execute('UPDATE event SET info=%s WHERE idevent=%s', (escape_string(new_info), escape_string(str(str(eventid)))))
	conn.commit()
	c.close()
	conn.close()

def change_organization_contact(organizationid, new_contact):
	'''Function takes organizationid and new contact and changes specified organization contact'''
	c, conn = connection()
	c.execute('UPDATE organization SET contact=%s WHERE idorganization=%s', (escape_string(new_contact), escape_string(str(str(organizationid)))))
	conn.commit()
	c.close()
	conn.close()

def change_user_password(userid, new_password):
	'''Function takes userid and new password and changes specified user password'''
	c, conn = connection()
	c.execute('UPDATE user SET password=%s WHERE iduser=%s', (escape_string(new_password), escape_string(str(str(userid)))))
	conn.commit()
	c.close()
	conn.close()

def change_event_date(eventid, new_date):
	'''Function takes eventid and new date and changes specified event date'''
	c, conn = connection()
	c.execute('UPDATE event SET date=%s WHERE idevent=%s', (escape_string(new_date), escape_string(str(str(eventid)))))
	conn.commit()
	c.close()
	conn.close()

def give_club_ownership(userid, clubid):
	'''Function takes userid and clubid and set user as owner of that club'''
	c, conn =  connection()
	c.execute('UPDATE club SET owner_id=%s WHERE idclub=%s', (escape_string(str(userid)), escape_string(str(clubid))))
	conn.commit()
	c.close()
	conn.close()

def give_event_ownership(userid, eventid):
	'''Function takes userid and eventid and set user as owner of that event'''
	c, conn =  connection()
	c.execute('UPDATE event SET owner_id=%s WHERE idevent=%s', (escape_string(str(userid)), escape_string(str(eventid))))
	conn.commit()
	c.close()
	conn.close()

def give_organization_ownership(userid, organizationid):
	'''Function takes userid and organizationid and set user as owner of that organization'''
	c, conn =  connection()
	c.execute('UPDATE organization SET owner_id=%s WHERE idorganization=%s', (escape_string(str(userid)), escape_string(str(organizationid))))
	conn.commit()
	c.close()
	conn.close()
