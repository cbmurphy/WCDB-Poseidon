#!/usr/bin/env python

# -------
# imports
# -------
import sys
import xml.etree.ElementTree as ET
from Query import *
from Login import *

create_table = ["""
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
DROP TABLE IF EXISTS PersonKind;""",
"""
CREATE TABLE Crisis (
	id		char(100)	NOT NULL
		PRIMARY KEY,
	name	text	NOT NULL,
	kind	char(100)	NOT NULL
		REFERENCES CrisisKind(id),
	start_date	date	NOT NULL,
	start_time	time,
	end_date		date,
	end_time		time,
	economic_impact	char(100)	NOT NULL
);""",
"""
CREATE TABLE Organization (
	id		char(100)	NOT NULL
		PRIMARY KEY,
	name	char(100)	NOT NULL,
	kind	char(100)	NOT	NULL
		REFERENCES OrganizationKind(id),
	history	text	NOT NULL,
	telephone	char(100) NOT NULL,
	fax		char(100) NOT NULL,
	email	char(100) NOT NULL,
	street_address	char(100) NOT NULL,
	locality	char(100) NOT NULL,
	region	char(100) NOT NULL,
	postal_code	char(100) NOT NULL,
	country	char(100) NOT NULL
);""",
"""
CREATE TABLE Person (
	id		char(100)	NOT NULL
		PRIMARY KEY,
	first_name	char(100) NOT NULL,
	middle_name	char(100),
	last_name		char(100) NOT NULL,
	suffix			char(100),
	kind	char(100)	NOT NULL
		REFERENCES PersonKind(id)
);""",
"""
CREATE TABLE Location (
	id	int	NOT NULL AUTO_INCREMENT
		PRIMARY KEY,
	entity_type	ENUM('C', 'O', 'P')	NOT NULL,
	entity_id		char(100)	NOT NULL,
	locality		char(100),
	region			char(100),
	country			char(100)
);""",
"""
CREATE TABlE HumanImpact (
	id	int NOT NULL AUTO_INCREMENT
		PRIMARY KEY,
	crisis_id	char(100) NOT NULL
		REFERENCES Crisis(id),
	type		char(100)	NOT NULL,
	number	int		NOT NULL
);""",
"""
CREATE TABLE ResourceNeeded (
	id	int NOT NULL AUTO_INCREMENT
		PRIMARY KEY,
	crisis_id	char(100) NOT NULL
		REFERENCES Crisis(id),
	description	text
);""",
"""
CREATE TABLE WaysToHelp (
	id	int NOT NULL AUTO_INCREMENT
		PRIMARY KEY,
	crisis_id	char(100) NOT NULL
		REFERENCES Crisis(id),
	description	text
);""",
"""
CREATE TABLE ExternalResource (
	id	int NOT NULL AUTO_INCREMENT
		PRIMARY KEY,
	entity_type	ENUM('C', 'O', 'P')	NOT NULL,
	entity_id		char(100)	NOT NULL,
	type	ENUM('IMAGE', 'VIDEO', 'MAP', 'SOCIAL_NETWORK', 'CITATION', 'EXTERNAL_LINK') NOT NULL,
	link	text	NOT NULL
);""",
"""
CREATE TABlE CrisisOrganization (
	id_crisis	char(100)	NOT NULL
		REFERENCES Crisis(id),
	id_organization	char(100)	NOT NULL
		REFERENCES Organization(id),
	PRIMARY KEY (id_crisis, id_organization)
);""",
"""
CREATE TABLE OrganizationPerson (
	id_organization	char(100)	NOT NULL
		REFERENCES Organization(id),
	id_person	char(100)	NOT NULL
		REFERENCES Person(id),
	PRIMARY KEY (id_organization, id_person)
);""",
"""
CREATE TABLE PersonCrisis (
	id_person	char(100)	NOT NULL
		REFERENCES Person(id),
	id_crisis	char(100)	NOT NULL
		REFERENCES Crisis(id),
	PRIMARY KEY (id_person, id_crisis)
);""",
"""
CREATE TABLE CrisisKind (
	id	char(100)	NOT NULL
		PRIMARY KEY,
	name	char(100)	NOT NULL,
	description	text NOT NULL
);""",
"""
CREATE TABLE OrganizationKind (
	id	char(100)	NOT NULL
		PRIMARY KEY,
	name	char(100)	NOT NULL,
	description	text NOT NULL
);""",
"""
CREATE TABLE PersonKind (
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
def wcdb2_import(root) :
	c = login()
	
	# Create the table
	for q in create_table :
		t = query(c, q)
		assert(t is None)
	
	# Insert CrisisKind
	for n in root.iter('CrisisKind') :
		# name
		name = n.find('Name')
		assert(name is not None)
		name_string = get_text(name)
		# description
		description = n.find('Description')
		assert(description is not None)
		description_string = get_text(description)
		# id
		id = '"' + escape_quote(n.attrib.get('crisisKindIdent')) + '"'
		assert(id is not None)
		q = 'INSERT INTO CrisisKind VALUES (%s, %s, %s)' % (id, name_string, description_string)
		query(c, q.encode('ascii','replace'))
		
	# Insert OrganizationKind
	for n in root.iter('OrganizationKind') :
		# name
		name = n.find('Name')
		assert(name is not None)
		name_string = get_text(name)
		# description
		description = n.find('Description')
		assert(description is not None)
		description_string = get_text(description)
		# id
		id = '"' + escape_quote(n.attrib.get('organizationKindIdent')) + '"'
		assert(id is not None)
		# generate and execute the query
		q = 'INSERT INTO OrganizationKind VALUES (%s, %s, %s)' % (id, name_string, description_string)
		query(c, q.encode('ascii','replace'))
		
	# Insert PersonKind
	for n in root.iter('PersonKind') :
		# name
		name = n.find('Name')
		assert(name is not None)
		name_string = get_text(name)
		# description
		description = n.find('Description')
		assert(description is not None)
		description_string = get_text(description)
		id = '"' + escape_quote(n.attrib.get('personKindIdent')) + '"'
		assert(id is not None)
		# generate and execute the query
		q = 'INSERT INTO PersonKind VALUES (%s, %s, %s)' % (id, name_string, description_string)
		query(c, q.encode('ascii','replace'))
		
	# Insert Crisis
	for n in root.iter('Crisis') :
		# id
		id = '"' + escape_quote(n.attrib.get('crisisIdent')) + '"'
		assert(id is not None)
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
		economic_impact_string = get_text(economic_impact)
		# generate and execute the query
		q = 'INSERT INTO Crisis VALUES (%s, %s, %s, %s, %s, %s, %s, %s)' % \
				(id, name_string, kind_string, start_date_string, start_time_string,
				end_date_string, end_time_string, economic_impact_string)
		query(c, q.encode('ascii','replace'))
	
	# Insert Organization
	for n in root.iter('Organization') :
		# id
		id = '"' + escape_quote(n.attrib.get('organizationIdent')) + '"'
		assert(id is not None)
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
		# generate and execute the query
		q = 'INSERT INTO Organization VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)' % \
				(id, name_string, kind_string, history_string, telephone_string,
				fax_string, email_string, street_address_string, locality_string,
				region_string, postal_code_string, country_string)	
		query(c, q.encode('ascii','replace'))
		
	# Insert Person
	for n in root.iter('Person') :
		# id
		id = '"' + escape_quote(n.attrib.get('personIdent')) + '"'
		assert(id is not None)
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
		# generate and execute the query
		q = 'INSERT INTO Person VALUES (%s, %s, %s, %s, %s, %s)' % \
				(id, first_name_string, middle_name_string, last_name_string,
				suffix_string, kind_string)
		query(c, q.encode('ascii','replace'))
	
	# Insert Location of Crisis
	for p in root.iter('Crisis') :
		entity_id = '"' + escape_quote(p.attrib.get('crisisIdent')) + '"'
		for n in p.iter('Location') :
			locality = n.find('Locality')
			locality_string = 'NULL' if (locality is None) else get_text(locality)
			region = n.find('Region')
			region_string = 'NULL' if (region is None) else get_text(region)
			country = n.find('Country')
			country_string = 'NULL' if (country is None) else get_text(country)
			q = 'INSERT INTO Location VALUES (NULL, "C", %s, %s, %s, %s)' % \
					(entity_id, locality_string, region_string, country_string)
			query(c, q.encode('ascii','replace'))
	# Insert Location of Organization
	for p in root.iter('Organization') :
		entity_id = '"' + escape_quote(p.attrib.get('organizationIdent')) + '"'
		for n in p.iter('Location') :
			locality = n.find('Locality')
			locality_string = 'NULL' if (locality is None) else get_text(locality)
			region = n.find('Region')
			region_string = 'NULL' if (region is None) else get_text(region)
			country = n.find('Country')
			country_string = 'NULL' if (country is None) else get_text(country)
			q = 'INSERT INTO Location VALUES (NULL, "O", %s, %s, %s, %s)' % \
					(entity_id, locality_string, region_string, country_string)
			query(c, q.encode('ascii','replace'))
	# Insert Location of Person
	for p in root.iter('Person') :
		entity_id = '"' + escape_quote(p.attrib.get('personIdent')) + '"'
		for n in p.iter('Location') :
			locality = n.find('Locality')
			locality_string = 'NULL' if (locality is None) else get_text(locality)
			region = n.find('Region')
			region_string = 'NULL' if (region is None) else get_text(region)
			country = n.find('Country')
			country_string = 'NULL' if (country is None) else get_text(country)
			q = 'INSERT INTO Location VALUES (NULL, "P", %s, %s, %s, %s)' % \
					(entity_id, locality_string, region_string, country_string)
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
			number_string = number.text if (number.text is not None) else '0'
			q = 'INSERT INTO HumanImpact VALUES (NULL, %s, %s, %s)' % \
					(crisis_id, tp_string, number_string)
			query(c, q.encode('ascii','replace'))
			
	# Insert ResourceNeeded
	for p in root.iter('Crisis') :
		crisis_id = '"' + escape_quote(p.attrib.get('crisisIdent')) + '"'
		for n in p.iter('ResourceNeeded') :
			description_string = get_text(n)
			q = 'INSERT INTO ResourceNeeded VALUES (NULL, %s, %s)' % \
					(crisis_id, description_string)
			query(c, q.encode('ascii','replace'))
	
	# Insert WaysToHelp
	for p in root.iter('Crisis') :
		crisis_id = '"' + escape_quote(p.attrib.get('crisisIdent')) + '"'
		for n in p.iter('WaysToHelp') :
			description_string = get_text(n)
			q = 'INSERT INTO WaysToHelp VALUES (NULL, %s, %s)' % \
					(crisis_id, description_string)
			query(c, q.encode('ascii','replace'))
			
	# Insert ExernalResource for Crisis
	for p in root.iter('Crisis') :
		entity_id = '"' + escape_quote(p.attrib.get('crisisIdent')) + '"'
		for n in p.iter('ImageURL') :
			URL_string = get_text(n)
			q = 'INSERT INTO ExternalResource VALUES (NULL, "C", %s, "IMAGE", %s)' % \
					(entity_id, URL_string)
			query(c, q.encode('ascii','replace'))
		for n in p.iter('VideoURL') :
			URL_string = get_text(n)
			q = 'INSERT INTO ExternalResource VALUES (NULL, "C", %s, "VIDEO", %s)' % \
					(entity_id, URL_string)
			query(c, q.encode('ascii','replace'))
		for n in p.iter('MapURL') :
			URL_string = get_text(n)
			q = 'INSERT INTO ExternalResource VALUES (NULL, "C", %s, "MAP", %s)' % \
					(entity_id, URL_string)
			query(c, q.encode('ascii','replace'))
		for n in p.iter('SocialNetworkURL') :
			URL_string = get_text(n)
			q = 'INSERT INTO ExternalResource VALUES (NULL, "C", %s, "SOCIAL_NETWORK", %s)' % \
					(entity_id, URL_string)
			query(c, q.encode('ascii','replace'))
		for n in p.iter('Citation') :
			URL_string = get_text(n)
			q = 'INSERT INTO ExternalResource VALUES (NULL, "C", %s, "CITATION", %s)' % \
					(entity_id, URL_string)
			query(c, q.encode('ascii','replace'))
		for n in p.iter('ExternalLinkURL') :
			URL_string = get_text(n)
			q = 'INSERT INTO ExternalResource VALUES (NULL, "C", %s, "EXTERNAL_LINK", %s)' % \
					(entity_id, URL_string)
			query(c, q.encode('ascii','replace'))
	# Insert ExernalResource for Organization
	for p in root.iter('Organization') :
		entity_id = '"' + escape_quote(p.attrib.get('organizationIdent')) + '"'
		for n in p.iter('ImageURL') :
			URL_string = get_text(n)
			q = 'INSERT INTO ExternalResource VALUES (NULL, "O", %s, "IMAGE", %s)' % \
					(entity_id, URL_string)
			query(c, q.encode('ascii','replace'))
		for n in p.iter('VideoURL') :
			URL_string = get_text(n)
			q = 'INSERT INTO ExternalResource VALUES (NULL, "O", %s, "VIDEO", %s)' % \
					(entity_id, URL_string)
			query(c, q.encode('ascii','replace'))
		for n in p.iter('MapURL') :
			URL_string = get_text(n)
			q = 'INSERT INTO ExternalResource VALUES (NULL, "O", %s, "MAP", %s)' % \
					(entity_id, URL_string)
			query(c, q.encode('ascii','replace'))
		for n in p.iter('SocialNetworkURL') :
			URL_string = get_text(n)
			q = 'INSERT INTO ExternalResource VALUES (NULL, "O", %s, "SOCIAL_NETWORK", %s)' % \
					(entity_id, URL_string)
			query(c, q.encode('ascii','replace'))
		for n in p.iter('Citation') :
			URL_string = get_text(n)
			q = 'INSERT INTO ExternalResource VALUES (NULL, "O", %s, "CITATION", %s)' % \
					(entity_id, URL_string)
			query(c, q.encode('ascii','replace'))
		for n in p.iter('ExternalLinkURL') :
			URL_string = get_text(n)
			q = 'INSERT INTO ExternalResource VALUES (NULL, "O", %s, "EXTERNAL_LINK", %s)' % \
					(entity_id, URL_string)
			query(c, q.encode('ascii','replace'))
	# Insert ExernalResource for Person
	for p in root.iter('Person') :
		entity_id = '"' + escape_quote(p.attrib.get('personIdent')) + '"'
		for n in p.iter('ImageURL') :
			URL_string = get_text(n)
			q = 'INSERT INTO ExternalResource VALUES (NULL, "P", %s, "IMAGE", %s)' % \
					(entity_id, URL_string)
			query(c, q.encode('ascii','replace'))
		for n in p.iter('VideoURL') :
			URL_string = get_text(n)
			q = 'INSERT INTO ExternalResource VALUES (NULL, "P", %s, "VIDEO", %s)' % \
					(entity_id, URL_string)
			query(c, q.encode('ascii','replace'))
		for n in p.iter('MapURL') :
			URL_string = get_text(n)
			q = 'INSERT INTO ExternalResource VALUES (NULL, "P", %s, "MAP", %s)' % \
					(entity_id, URL_string)
			query(c, q.encode('ascii','replace'))
		for n in p.iter('SocialNetworkURL') :
			URL_string = get_text(n)
			q = 'INSERT INTO ExternalResource VALUES (NULL, "P", %s, "SOCIAL_NETWORK", %s)' % \
					(entity_id, URL_string)
			query(c, q.encode('ascii','replace'))
		for n in p.iter('Citation') :
			URL_string = get_text(n)
			q = 'INSERT INTO ExternalResource VALUES (NULL, "P", %s, "CITATION", %s)' % \
					(entity_id, URL_string)
			query(c, q.encode('ascii','replace'))
		for n in p.iter('ExternalLinkURL') :
			URL_string = get_text(n)
			q = 'INSERT INTO ExternalResource VALUES (NULL, "P", %s, "EXTERNAL_LINK", %s)' % \
					(entity_id, URL_string)
			query(c, q.encode('ascii','replace'))
	
	# Insert CrisisOrganization from RelatedCrisis of Organization
	for org in root.iter('Organization'):
		id_organization = '"' + escape_quote(org.attrib.get('organizationIdent')) + '"'
		for cri in org.iter('RelatedCrisis') :
			id_crisis = '"' + escape_quote(cri.attrib.get('crisisIdent')) + '"'
			q = 'INSERT IGNORE INTO CrisisOrganization VALUES (%s, %s)' % \
					(id_crisis, id_organization)
			query(c, q.encode('ascii', 'replace'))
	# Insert CrisisOrganization from RelatedOrganization of Crisis
	for cri in root.iter('Crisis'):
		id_crisis = '"' + escape_quote(cri.attrib.get('crisisIdent')) + '"'
		for org in cri.iter('RelatedOrganization') :
			id_organization = '"' + escape_quote(org.attrib.get('organizationIdent')) + '"'
			q = 'INSERT IGNORE INTO CrisisOrganization VALUES (%s, %s)' % \
					(id_crisis, id_organization)
			query(c, q.encode('ascii', 'replace'))		
	# Insert OrganizationPerson from RelatedOrganization of Person
	for per in root.iter('Person'):
		id_person = '"' + escape_quote(per.attrib.get('personIdent')) + '"'
		for org in per.iter('RelatedOrganization') :
			id_organization = '"' + escape_quote(org.attrib.get('organizationIdent')) + '"'
			q = 'INSERT IGNORE INTO OrganizationPerson VALUES (%s, %s)' % \
					(id_organization, id_person)
			query(c, q.encode('ascii', 'replace'))
	# Insert OrganizationPerson from RelatedPerson of Organization
	for org in root.iter('Organization'):
		id_organization = '"' + escape_quote(org.attrib.get('organizationIdent')) + '"'
		for per in org.iter('RelatedPerson') :
			id_person = '"' + escape_quote(per.attrib.get('personIdent')) + '"'
			q = 'INSERT IGNORE INTO OrganizationPerson VALUES (%s, %s)' % \
					(id_organization, id_person)
			query(c, q.encode('ascii', 'replace'))
	# Insert PersonCrisis from RelatedPerson of Crisis
	for cri in root.iter('Crisis'):
		id_crisis = '"' + escape_quote(cri.attrib.get('crisisIdent')) + '"'
		for per in cri.iter('RelatedPerson') :
			id_person = '"' + escape_quote(per.attrib.get('personIdent')) + '"'
			q = 'INSERT IGNORE INTO PersonCrisis VALUES (%s, %s)' % \
					(id_person, id_crisis)
			query(c, q.encode('ascii', 'replace'))
	# Insert PersonCrisis from RelatedCrisis of Person
	for per in root.iter('Person'):
		id_person = '"' + escape_quote(per.attrib.get('personIdent')) + '"'
		for cri in per.iter('RelatedCrisis') :
			id_crisis = '"' + escape_quote(cri.attrib.get('crisisIdent')) + '"'
			q = 'INSERT IGNORE INTO PersonCrisis VALUES (%s, %s)' % \
					(id_person, id_crisis)
			query(c, q.encode('ascii', 'replace'))
	
	c.close()

