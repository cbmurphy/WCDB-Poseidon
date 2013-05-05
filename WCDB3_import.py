#!/usr/bin/env python

# -------
# imports
# -------
import sys
import xml.etree.ElementTree as ET
from Query import *
from Login import *

drop_table = [
"""
DROP TABLE IF EXISTS Crisis;""",
"""
DROP TABLE IF EXISTS Organization;""",
"""
DROP TABLE IF EXISTS Person;""",
"""
DROP TABLE IF EXISTS Location;""",
"""
DROP TABLE IF EXISTS HumanImpact;""",
"""
DROP TABLE IF EXISTS ResourceNeeded;""",
"""
DROP TABLE IF EXISTS WaysToHelp;""",
"""
DROP TABLE IF EXISTS ExternalResource;""",
"""
DROP TABLE IF EXISTS CrisisOrganization;""",
"""
DROP TABLE IF EXISTS OrganizationPerson;""",
"""
DROP TABLE IF EXISTS PersonCrisis;""",
"""
DROP TABLE IF EXISTS CrisisKind;""",
"""
DROP TABLE IF EXISTS OrganizationKind;""",
"""
DROP TABLE IF EXISTS PersonKind;"""
]

create_table = [
"""
CREATE TABLE IF NOT EXISTS Crisis (
	id	char(100)		NOT NULL
		PRIMARY KEY,
	name	text			NOT NULL,
	kind	char(100)		NOT NULL
		REFERENCES CrisisKind(id),
	start_date	date		NOT NULL,
	start_time	time,
	end_date	date,
	end_time	time,
	economic_impact	char(100)	NOT NULL
);""",
"""
CREATE TABLE IF NOT EXISTS Organization (
	id		char(100)	NOT NULL
		PRIMARY KEY,
	name		char(100)	NOT NULL,
	kind		char(100)	NOT NULL
		REFERENCES OrganizationKind(id),
	history		text		NOT NULL,
	telephone	char(100) 	NOT NULL,
	fax		char(100) 	NOT NULL,
	email		char(100) 	NOT NULL,
	street_address	char(100) 	NOT NULL,
	locality	char(100) 	NOT NULL,
	region		char(100) 	NOT NULL,
	postal_code	char(100)	NOT NULL,
	country		char(100) 	NOT NULL
);""",
"""
CREATE TABLE IF NOT EXISTS Person (
	id		char(100)	NOT NULL
		PRIMARY KEY,
	first_name	char(100)	NOT NULL,
	middle_name	char(100),
	last_name	char(100)	NOT NULL,
	suffix		char(100),
	kind		char(100)	NOT NULL
		REFERENCES PersonKind(id)
);""",
"""
CREATE TABLE IF NOT EXISTS Location (
	id		int			NOT NULL AUTO_INCREMENT
		PRIMARY KEY,
	entity_type	ENUM('C', 'O', 'P')	NOT NULL,
	entity_id	char(100)		NOT NULL,
	locality	char(100),
	region		char(100),
	country		char(100)
);""",
"""
CREATE TABlE IF NOT EXISTS HumanImpact (
	id		int		NOT NULL	AUTO_INCREMENT
		PRIMARY KEY,
	crisis_id	char(100)	NOT NULL
		REFERENCES Crisis(id),
	type		char(100)	NOT NULL,
	number		int		NOT NULL
);""",
"""
CREATE TABLE IF NOT EXISTS ResourceNeeded (
	id		int 		NOT NULL AUTO_INCREMENT
		PRIMARY KEY,
	crisis_id	char(100)	NOT NULL
		REFERENCES Crisis(id),
	description	text
);""",
"""
CREATE TABLE IF NOT EXISTS WaysToHelp (
	id		int		NOT NULL	AUTO_INCREMENT
		PRIMARY KEY,
	crisis_id	char(100)	NOT NULL
		REFERENCES Crisis(id),
	description	text
);""",
"""
CREATE TABLE IF NOT EXISTS ExternalResource (
	id		int			NOT NULL AUTO_INCREMENT
		PRIMARY KEY,
	entity_type	ENUM('C', 'O', 'P')	NOT NULL,
	entity_id	char(100)		NOT NULL,
	type		ENUM('IMAGE', 'VIDEO', 'MAP', 'SOCIAL_NETWORK', 'CITATION', 'EXTERNAL_LINK') NOT NULL,
	link		text			NOT NULL
);""",
"""
CREATE TABlE IF NOT EXISTS CrisisOrganization (
	id_crisis	char(100)	NOT NULL
		REFERENCES Crisis(id),
	id_organization	char(100)	NOT NULL
		REFERENCES Organization(id),
	PRIMARY KEY (id_crisis, id_organization)
);""",
"""
CREATE TABLE IF NOT EXISTS OrganizationPerson (
	id_organization	char(100)	NOT NULL
		REFERENCES Organization(id),
	id_person	char(100)	NOT NULL
		REFERENCES Person(id),
	PRIMARY KEY (id_organization, id_person)
);""",
"""
CREATE TABLE IF NOT EXISTS PersonCrisis (
	id_person	char(100)	NOT NULL
		REFERENCES Person(id),
	id_crisis	char(100)	NOT NULL
		REFERENCES Crisis(id),
	PRIMARY KEY (id_person, id_crisis)
);""",
"""
CREATE TABLE IF NOT EXISTS CrisisKind (
	id	char(100)	NOT NULL
		PRIMARY KEY,
	name	char(100)	NOT NULL,
	description	text NOT NULL
);""",
"""
CREATE TABLE IF NOT EXISTS OrganizationKind (
	id	char(100)	NOT NULL
		PRIMARY KEY,
	name	char(100)	NOT NULL,
	description	text NOT NULL
);""",
"""
CREATE TABLE IF NOT EXISTS PersonKind (
	id	char(100)	NOT NULL
		PRIMARY KEY,
	name	char(100)	NOT NULL,
	description	text NOT NULL
);"""]


# Utility to get the text from a ElementTree node, return "\"\""
# if there is no text
def get_text(node) :
	return '""' if (node.text is None) else '"' + escape_quote(node.text) + '"'
	
# Utility to escape all double quotes of a string that is used as
# a string literal in a SQL statement.
def escape_quote(s) :
	return s.replace('"', '\\"');

# --------------------------------------------------
# Function that import from an ElementTree into a DB
# --------------------------------------------------
def wcdb3_import(root,drop_all_tables=False,use_current=False):

	'''
	wcdb3_import(xml,drop_all_tables=False,use_current=False)
	Import a valid xml into a database.
	By default, tables will not be dropped upon calling the function.
	Also by default, new values supercede pre-existing ones with the same key.
	'''

	# Login
	c = login()
	# Drop all tables if drop_all_tables = True
	if drop_all_tables:
		for q in drop_table :
			t = query(c, q)
			assert(t is None)	
	# Create the tables
	for q in create_table :
		t = query(c, q)
		assert(t is None)
	# Insert CrisisKind
	for n in root.iter('CrisisKind') :
		# check for existing id
		id = '"' + escape_quote(n.attrib.get('crisisKindIdent')) + '"'
		q = 'SELECT id from CrisisKind where id = %s' %id
		current_id = query(c, q.encode('ascii','replace'))
		# break if already an id and use_current = True
		if current_id and use_current:
			continue
		# name
		name = n.find('Name')
		assert(name is not None)
		name_string = get_text(name)
		# description
		description = n.find('Description')
		assert(description is not None)
		description_string = get_text(description)
		# perform insertion/update
		if not current_id:
			# insert
			q = 'INSERT INTO CrisisKind VALUES (%s, %s, %s)' \
				%(id, name_string, description_string)
			query(c, q.encode('ascii','replace'))
		elif not use_current:
			# update
			q = 'UPDATE CrisisKind set name = %s, description = %s where id = %s' \
				%(name_string, description_string, id)
			query(c, q.encode('ascii','replace'))
		# else keep current entry

	# Insert OrganizationKind
	for n in root.iter('OrganizationKind'):
		# check for existing id
		id = '"' + escape_quote(n.attrib.get('organizationKindIdent')) + '"'
		assert(id is not None)
		q = 'SELECT id from OrganizationKind where id = %s' %id
		current_id = query(c, q.encode('ascii','replace'))
		# break if already an id and use_current = True
		if current_id and use_current:
			continue
		# name
		name = n.find('Name')
		assert(name is not None)
		name_string = get_text(name)
		# description
		description = n.find('Description')
		assert(description is not None)
		description_string = get_text(description)
		# perform insertion/update
		if not current_id:
			# insert
			q = 'INSERT INTO OrganizationKind VALUES (%s, %s, %s)' \
				%(id, name_string, description_string)
			query(c, q.encode('ascii','replace'))
		elif not use_current:
			# update
			q = 'UPDATE OrganizationKind set name = %s, description = %s \
				where id = %s' %(name_string, description_string, id)
			query(c, q.encode('ascii','replace'))
		# else keep current entry
		
	# Insert PersonKind
	for n in root.iter('PersonKind') :
		# check for existing id
		id = '"' + escape_quote(n.attrib.get('personKindIdent')) + '"'
		assert(id is not None)
		q = 'SELECT id from PersonKind where id = %s' %id
		current_id = query(c, q.encode('ascii','replace'))
		# break if already an id and use_current = True
		if current_id and use_current:
			continue
		# name
		name = n.find('Name')
		assert(name is not None)
		name_string = get_text(name)
		# description
		description = n.find('Description')
		assert(description is not None)
		description_string = get_text(description)
		# perform insertion/update
		if not current_id:
			# insert
			q = 'INSERT INTO PersonKind VALUES (%s, %s, %s)' % \
				(id, name_string,description_string)
			query(c, q.encode('ascii','replace'))
		elif not use_current:
			# update
			q = 'UPDATE PersonKind set name = %s, description = %s where id = %s' \
					%(name_string, description_string, id)
			query(c, q.encode('ascii','replace'))
		# else keep current entry
		
	# Insert Crisis
	for n in root.iter('Crisis') :
		# id
		id = '"' + escape_quote(n.attrib.get('crisisIdent')) + '"'
		assert(id is not None)
		# check for existing id
		q = 'SELECT id from Crisis where id = %s;' %id
		current_id = query(c, q.encode('ascii','replace'))
		# break if already an id and use_current = True
		if current_id and use_current:
			continue
		# name
		name = n.find('Name')
		assert(name is not None)
		name_string = get_text(name)
		# kind
		kind = n.find('Kind')
		assert(kind is not None)
		kind_string = '"' + escape_quote(kind.attrib.get('crisisKindIdent')) + '"'
		# start_date_time
		start_date_time = n.find('StartDateTime')
		assert(start_date_time is not None)
		start_date = start_date_time.find('Date')
		assert(start_date is not None)
		start_date_string = '"' + escape_quote(start_date.text) + '"'
		start_time = start_date_time.find('Time')
		start_time_string = 'NULL' if (start_time is None) else \
				'"' + escape_quote(start_time.text) + '"'
		# end_date_time
		end_date_time = n.find('EndDateTime')
		if (end_date_time is None) :
			end_date_string = 'NULL'
			end_time_string = 'NULL'
		else :
			end_date = end_date_time.find('Date')
			assert(end_date is not None)
			end_date_string = '"' + escape_quote(end_date.text) + '"'
			end_time = end_date_time.find('Time')
			end_time_string = 'NULL' if (end_time is None) else \
					'"' + escape_quote(end_time.text) + '"'
		# economic_impact
		economic_impact = n.find('EconomicImpact')
		assert(economic_impact is not None)
		economic_impact_string = get_text(economic_impact) \
			if economic_impact.text != None else '0'
		# perform insertion/update
		if not current_id:
			# insert
			q = 'INSERT INTO Crisis VALUES (%s, %s, %s, %s, %s, %s, %s, %s)' % \
				(id, name_string, kind_string, start_date_string, start_time_string,
				end_date_string, end_time_string, economic_impact_string)
			query(c, q.encode('ascii','replace'))
		elif not use_current:
			# update
			q = 'UPDATE Crisis set name = %s, kind = %s, start_date = %s, start_time = %s, \
				end_date = %s, end_time = %s, economic_impact = %s \
				where id = %s' %(name_string, kind_string, start_date_string, start_time_string,
						end_date_string, end_time_string, economic_impact_string, id)
			query(c, q.encode('ascii','replace'))
		# else keep current entry


	# Insert Organization
	for n in root.iter('Organization') :
		# check for existing id
		id = '"' + escape_quote(n.attrib.get('organizationIdent')) + '"'
		assert(id is not None)
		q = 'SELECT id from Organization where id = %s' %id
		current_id = query(c, q.encode('ascii','replace'))
		# break if already an id and use_current = True
		if current_id and use_current:
			continue
		# name
		name = n.find('Name')
		assert(name is not None)
		name_string = get_text(name)
		# kind
		kind = n.find('Kind')
		assert(kind is not None)
		kind_string = '"' + escape_quote(kind.attrib.get('organizationKindIdent')) + '"'
		# history
		history = n.find('History')
		assert(history is not None)
		history_string = get_text(history)
		# contact_info
		contact_info = n.find('ContactInfo')
		assert(contact_info is not None)
		telephone = contact_info.find('Telephone')
		assert(telephone is not None)
		telephone_string = get_text(telephone)
		fax = contact_info.find('Fax')
		assert(fax is not None)
		fax_string = get_text(fax)
		email = contact_info.find('Email')
		assert(email is not None)
		email_string = get_text(email)
		postal_address = contact_info.find('PostalAddress')
		assert(postal_address is not None)
		street_address = postal_address.find('StreetAddress')
		assert(street_address is not None)
		street_address_string = get_text(street_address)
		locality = postal_address.find('Locality')
		assert(locality is not None)
		locality_string = get_text(locality)
		region = postal_address.find('Region')
		assert(region is not None)
		region_string = get_text(region)
		postal_code = postal_address.find('PostalCode')
		assert(postal_code is not None)
		postal_code_string = get_text(postal_code)
		country = postal_address.find('Country')
		assert(country is not None)
		country_string = get_text(country)
		# perform insertion/update
		if not current_id:
			# insert
			q = 'INSERT INTO Organization VALUES (%s, %s, %s, %s, %s, %s, %s,\
				 %s, %s, %s, %s, %s)' % \
				(id, name_string, kind_string, history_string, telephone_string,
				fax_string, email_string, street_address_string, locality_string,
				region_string, postal_code_string, country_string)	
			query(c, q.encode('ascii','replace'))
		elif not use_current:
			# update
			q = 'UPDATE Organization set name = %s, kind = %s, history = %s, \
				telephone = %s, fax = %s, email = %s, street_address = %s, \
				locality = %s, region = %s postal_code = %s, country = %s \
				where id = %s' \
				%(name_string, kind_string, history_string, telephone_string,
				fax_string, email_string, street_address_string, locality_string,
				region_string, postal_code_string, country_string, id)
			query(c, q.encode('ascii','replace'))
		# else keep current entry

		
	# Insert Person
	for n in root.iter('Person') :
		# check for existing id
		id = '"' + escape_quote(n.attrib.get('personIdent')) + '"'
		assert(id is not None)
		q = 'SELECT id from Person where id = %s' %id
		current_id = query(c, q.encode('ascii','replace'))
		# break if already an id and use_current = True
		if current_id and use_current:
			continue
		# name
		name = n.find('Name')
		assert(name is not None)
		first_name = name.find('FirstName')
		assert(first_name is not None)
		first_name_string = get_text(first_name)
		# middle_name
		middle_name = name.find('MiddleName')
		middle_name_string = 'NULL' if (middle_name is None) else get_text(middle_name)
		# last_name
		last_name = name.find('LastName')
		assert(last_name is not None)
		last_name_string = get_text(last_name)
		# suffix
		suffix = name.find('Suffix')
		suffix_string = 'NULL' if (suffix is None) else get_text(suffix)
		# kind
		kind = n.find('Kind')
		assert(kind is not None)
		kind_string = '"' + escape_quote(kind.attrib.get('personKindIdent')) + '"'
		# perform insertion/update
		if not current_id:
			# insert
			q = 'INSERT INTO Person VALUES (%s, %s, %s, %s, %s, %s)' % \
				(id, first_name_string, middle_name_string, last_name_string,
				suffix_string, kind_string)	
			query(c, q.encode('ascii','replace'))
		elif not use_current:
			# update
			q = 'UPDATE Person set first_name = %s, middle_name = %s, \
				last_name = %s, suffix = %s, kind = %s where id = %s' % \
				(first_name_string, middle_name_string, last_name_string,
				suffix_string, kind_string, id)
			query(c, q.encode('ascii','replace'))
		# else keep current entry

	# Insert Locations of Organizations, Persons, and Crises
	for x in ('Organization', 'Crisis', 'Person'):
		for p in root.iter(x):
			entity_id = '"' + escape_quote(p.attrib.get(x.lower()+'Ident')) + '"'
			for n in p.iter('Location'):
				locality = n.find('Locality')
				locality_string = 'NULL' if (locality is None) else get_text(locality)
				region = n.find('Region')
				region_string = 'NULL' if (region is None) else get_text(region)
				country = n.find('Country')
				country_string = 'NULL' if (country is None) else get_text(country)
				if region_string == 'NULL' and locality_string != 'NULL':
					q = 'SELECT * from Location where entity_id = %s and entity_type = "%s" \
						and country = %s and region is NULL and locality = %s' \
						%(entity_id, x[0], country_string, locality_string)
				elif locality_string == 'NULL' and region_string != 'NULL':
					q = 'SELECT * from Location where entity_id = %s and entity_type = "%s" \
						and country = %s and locality is NULL and region = %s' \
						%(entity_id, x[0], country_string, region_string)
				elif locality_string == 'NULL' and region_string == 'NULL':
					q = 'SELECT * from Location where entity_id = %s and entity_type = "%s" \
						and country = %s and locality is NULL and region is NULL' \
						%(entity_id, x[0], country_string)
				else:
					q = 'SELECT * from Location where entity_id = %s and entity_type = "%s" \
						and country = %s and locality = %s and region = %s' \
						%(entity_id, x[0], country_string, locality_string, region_string)
				if not query(c, q.encode('ascii','replace')):
					q = 'INSERT INTO Location VALUES (NULL, "%s", %s, %s, %s, %s)' % \
						(x[0], entity_id, locality_string, region_string, country_string)
					query(c, q.encode('ascii','replace'))

	# Insert HumanImpact
	for p in root.iter('Crisis') :
		crisis_id = '"' + escape_quote(p.attrib.get('crisisIdent')) + '"'
		for n in p.iter('HumanImpact') :
			tp = n.find('Type')
			assert(tp is not None)
			tp_string = get_text(tp)
			number = n.find('Number')
			assert(number is not None)
			q = 'SELECT * from HumanImpact where crisis_id = %s and type = %s' \
				%(crisis_id, tp_string)
			current = query(c, q.encode('ascii','replace'))
			# insert values
			if not current:
				number_string = number.text if (number.text is not None) else '0'
				q = 'INSERT INTO HumanImpact VALUES (NULL, %s, %s, %s)' % \
					(crisis_id, tp_string, number_string)
				query(c, q.encode('ascii','replace'))
				continue
			# update value if new value is larger
			elif number.text > current[0][3]:
				number_string = number.text if (number.text is not None) else '0'
				print "updating %s with %s" %(current[0][3], number_string)
				q = 'UPDATE HumanImpact set number = %s where id = %s' \
				    %(number_string, current[0][0])
				query(c, q.encode('ascii','replace'))
			# else keep current value

			
	# Insert ResourceNeeded
	for p in root.iter('Crisis') :
		crisis_id = '"' + escape_quote(p.attrib.get('crisisIdent')) + '"'
		for n in p.iter('ResourceNeeded') :
			description_string = get_text(n)
			q = 'SELECT * from ResourceNeeded where crisis_id = %s and description = %s' \
				%(crisis_id, description_string)
			if not query(c, q.encode('ascii','replace')):
				q = 'INSERT INTO ResourceNeeded VALUES (NULL, %s, %s)' \
					%(crisis_id, description_string)
				query(c, q.encode('ascii','replace'))
	
	# Insert WaysToHelp
	for p in root.iter('Crisis'):
		crisis_id = '"' + escape_quote(p.attrib.get('crisisIdent')) + '"'
		for n in p.iter('WaysToHelp') :
			description_string = get_text(n)
			q = 'SELECT * from WaysToHelp where crisis_id = %s and description = %s' \
				%(crisis_id, description_string)
			if not query(c, q.encode('ascii','replace')):
				q = 'INSERT INTO WaysToHelp VALUES (NULL, %s, %s)' \
					%(crisis_id, description_string)
				query(c, q.encode('ascii','replace'))
			
    # Insert ExernalResource for Crisis, Person, and Organization
	for x in ('Crisis', 'Organization', 'Person'):
		for p in root.iter(x):
			entity_id = '"' + escape_quote(p.attrib.get(x.lower()+'Ident')) + '"'
			# check/insert URLs of IMAGES
			q = 'SELECT link from ExternalResource where entity_type = "%s" \
				and type = "IMAGE"' %x[0]
			results = (i[0] for i in query(c, q.encode('ascii','replace')))
			# check if each URL already exists and insert if not
			for n in p.iter('ImageURL'):
				if n.text not in results:
					URL_string = get_text(n)
					q = 'INSERT INTO ExternalResource VALUES \
						(NULL, "%s", %s, "IMAGE", %s)' \
						%(x[0], entity_id, URL_string)
					query(c, q.encode('ascii','replace'))
			# check/insert URLs of VIDEOS
			q = 'SELECT link from ExternalResource where entity_type = "%s" \
				and type = "VIDEO"' %x[0]
			results = (i[0] for i in query(c, q.encode('ascii','replace')))
			# check if each URL already exists and insert if not
			for n in p.iter('VideoURL'):
				if n.text not in results:
					URL_string = get_text(n)
					q = 'INSERT INTO ExternalResource VALUES \
						(NULL, "%s", %s, "VIDEO", %s)' \
						%(x[0], entity_id, URL_string)
					query(c, q.encode('ascii','replace'))
			# check/insert URLs of MAPs
			q = 'SELECT link from ExternalResource where entity_type = "%s" \
				and type = "MAP"' %x[0]
			results = (i[0] for i in query(c, q.encode('ascii','replace')))
			# check if each URL already exists and insert if not
			for n in p.iter('MapURL'):
				if n.text not in results:
					URL_string = get_text(n)
					q = 'INSERT INTO ExternalResource VALUES \
						(NULL, "%s", %s, "MAP", %s)' \
						%(x[0], entity_id, URL_string)
					query(c, q.encode('ascii','replace'))
			# check/insert URLs of Social Networks
			q = 'SELECT link from ExternalResource where entity_type = "%s" \
				and type = "SOCIAL_NETWORK"' %x[0]
			results = (i[0] for i in query(c, q.encode('ascii','replace')))
			# check if each URL already exists and insert if not
			for n in p.iter('SocialNetworkURL'):
				if n.text not in results:
					URL_string = get_text(n)
					q = 'INSERT INTO ExternalResource VALUES \
						(NULL, "%s", %s, "SOCIAL_NETWORK", %s)' \
						%(x[0], entity_id, URL_string)
					query(c, q.encode('ascii','replace'))
			# check/insert URLs of Citations
			q = 'SELECT link from ExternalResource where entity_type = "%s" \
				and type = "CITATION"' %x[0]
			results = (i[0] for i in query(c, q.encode('ascii','replace')))
			# check if each URL already exists and insert if not
			for n in p.iter('Citation'):
				if n.text not in results:
					URL_string = get_text(n)
					q = 'INSERT INTO ExternalResource VALUES \
						(NULL, "%s", %s, "CITATION", %s)' \
						%(x[0], entity_id, URL_string)
					query(c, q.encode('ascii','replace'))
			# check/insert URLs of External Links
			q = 'SELECT link from ExternalResource where entity_type = "%s" \
				and type = "EXTERNAL_LINK"' %x[0]
			results = (i[0] for i in query(c, q.encode('ascii','replace')))
			# check if each URL already exists and insert if not
			for n in p.iter('ExternalLinkURL'):
				if n.text not in results:
					URL_string = get_text(n)
					q = 'INSERT INTO ExternalResource VALUES \
						(NULL, "%s", %s, "EXTERNAL_LINK", %s)' \
						%(x[0], entity_id, URL_string)
					query(c, q.encode('ascii','replace'))
				
	
	# Insert CrisisOrganization from RelatedCrisis of Organization
	for org in root.iter('Organization'):
		id_organization = '"' + escape_quote(org.attrib.get('organizationIdent')) + '"'
		for cri in org.iter('RelatedCrisis') :
			id_crisis = '"' + escape_quote(cri.attrib.get('crisisIdent')) + '"'
			q = "SELECT * from CrisisOrganization where id_crisis = %s" %id_crisis
			if not query(c, q.encode('ascii', 'replace')):
				q = 'INSERT IGNORE INTO CrisisOrganization VALUES (%s, %s)' \
					%(id_crisis, id_organization)
				query(c, q.encode('ascii', 'replace'))

	# Insert CrisisOrganization from RelatedOrganization of Crisis
	for cri in root.iter('Crisis'):
		id_crisis = '"' + escape_quote(cri.attrib.get('crisisIdent')) + '"'
		for org in cri.iter('RelatedOrganization') :
			id_organization = \
				'"' + escape_quote(org.attrib.get('organizationIdent')) + '"'
			q = "SELECT * from CrisisOrganization where id_organization = %s" \
				%id_organization
			if not query(c, q.encode('ascii', 'replace')):
				q = 'INSERT IGNORE INTO CrisisOrganization VALUES (%s, %s)' \
					%(id_crisis, id_organization)
				query(c, q.encode('ascii', 'replace'))

	# Insert OrganizationPerson from RelatedOrganization of Person
	for per in root.iter('Person'):
		id_person = '"' + escape_quote(per.attrib.get('personIdent')) + '"'
		for org in per.iter('RelatedOrganization') :
			id_organization = \
				'"' + escape_quote(org.attrib.get('organizationIdent')) + '"'
			q = "SELECT * from OrganizationPerson where id_organization = %s" \
				%id_organization
			if not query(c, q.encode('ascii', 'replace')):
				q = 'INSERT IGNORE INTO OrganizationPerson VALUES (%s, %s)' \
					%(id_organization, id_person)
				query(c, q.encode('ascii', 'replace'))

	# Insert OrganizationPerson from RelatedPerson of Organization
	for org in root.iter('Organization'):
		id_organization = '"' + escape_quote(org.attrib.get('organizationIdent')) + '"'
		for per in org.iter('RelatedPerson') :
			id_person = '"' + escape_quote(per.attrib.get('personIdent')) + '"'
			q = "SELECT * from OrganizationPerson where id_person = %s" %id_person
			if not query(c, q.encode('ascii', 'replace')):
				q = 'INSERT IGNORE INTO OrganizationPerson VALUES (%s, %s)' \
					%(id_organization, id_person)
				query(c, q.encode('ascii', 'replace'))

	# Insert PersonCrisis from RelatedPerson of Crisis
	for cri in root.iter('Crisis'):
		id_crisis = '"' + escape_quote(cri.attrib.get('crisisIdent')) + '"'
		for per in cri.iter('RelatedPerson') :
			id_person = '"' + escape_quote(per.attrib.get('personIdent')) + '"'
			q = "SELECT * from PersonCrisis where id_person = %s" %id_person
			if not query(c, q.encode('ascii', 'replace')):
				q = 'INSERT IGNORE INTO PersonCrisis VALUES (%s, %s)' \
					%(id_person, id_crisis)
				query(c, q.encode('ascii', 'replace'))
	# Insert PersonCrisis from RelatedCrisis of Person
	for per in root.iter('Person'):
		id_person = '"' + escape_quote(per.attrib.get('personIdent')) + '"'
		for cri in per.iter('RelatedCrisis') :
			id_crisis = '"' + escape_quote(cri.attrib.get('crisisIdent')) + '"'
			q = "SELECT * from PersonCrisis where id_person = %s" %id_crisis
			if not query(c, q.encode('ascii', 'replace')):
				q = 'INSERT IGNORE INTO PersonCrisis VALUES (%s, %s)' \
					%(id_person, id_crisis)
				query(c, q.encode('ascii', 'replace'))
	
	c.close()
