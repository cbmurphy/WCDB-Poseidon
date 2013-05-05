DROP TABLE IF EXISTS Crisis;
DROP TABLE IF EXISTS Organization;
DROP TABLE IF EXISTS Person;
DROP TABLE IF EXISTS Location;
DROP TABLE IF EXISTS HumanImpact;
DROP TABLE IF EXISTS ResourceNeeded;
DROP TABLE IF EXISTS WaysToHelp;
DROP TABLE IF EXISTS ExternalResource;
DROP TABLE IF EXISTS CrisisOrganization;
DROP TABLE IF EXISTS OrganizationPerson;
DROP TABLE IF EXISTS PersonCrisis;
DROP TABLE IF EXISTS CrisisKind;
DROP TABLE IF EXISTS OrganizationKind;
DROP TABLE IF EXISTS PersonKind;

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
);

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
	country	char(100)  NOT NULL
);

CREATE TABLE Person (
	id		char(100)	NOT NULL
		PRIMARY KEY,
	first_name	char(100) NOT NULL,
	middle_name	char(100),
	last_name		char(100) NOT NULL,
	suffix			char(100),
	kind	char(100)	NOT NULL
		REFERENCES PersonKind(id)
);

CREATE TABLE Location (
	id	int	NOT NULL AUTO_INCREMENT
		PRIMARY KEY,
	entity_type	ENUM('C', 'O', 'P')	NOT NULL,
	entity_id		char(100)	NOT NULL,
	locality		char(100),
	region			char(100),
	country			char(100)
);

CREATE TABlE HumanImpact (
	id	int NOT NULL AUTO_INCREMENT
		PRIMARY KEY,
	crisis_id	char(100) NOT NULL
		REFERENCES Crisis(id),
	type		char(100)	NOT NULL,
	number	int		NOT NULL
);

CREATE TABLE ResourceNeeded (
	id	int NOT NULL AUTO_INCREMENT
		PRIMARY KEY,
	crisis_id	char(100) NOT NULL
		REFERENCES Crisis(id),
	description	text
);

CREATE TABLE WaysToHelp (
	id	int NOT NULL AUTO_INCREMENT
		PRIMARY KEY,
	crisis_id	char(100) NOT NULL
		REFERENCES Crisis(id),
	description	text
);

CREATE TABLE WaysToHelp (
	id	int NOT NULL AUTO_INCREMENT
		PRIMARY KEY,
	crisis_id	char(100) NOT NULL
		REFERENCES Crisis(id),
	description	text
);

CREATE TABLE ExternalResource (
	id	int NOT NULL AUTO_INCREMENT
		PRIMARY KEY,
	entity_type	ENUM('C', 'O', 'P')	NOT NULL,
	entity_id		char(100)	NOT NULL,
	type	ENUM('IMAGE', 'VIDEO', 'MAP', 'SOCIAL_NETWORK', 'CITATION', 'EXTERNAL_LINK') NOT NULL,
	link	text	NOT NULL
);

CREATE TABlE CrisisOrganization (
	id_crisis	char(100)	NOT NULL
		REFERENCES Crisis(id),
	id_organization	char(100)	NOT NULL
		REFERENCES Organization(id),
	PRIMARY KEY (id_crisis, id_organization)
);

CREATE TABLE OrganizationPerson (
	id_organization	char(100)	NOT NULL
		REFERENCES Organization(id),
	id_person	char(100)	NOT NULL
		REFERENCES Person(id),
	PRIMARY KEY (id_organization, id_person)
);

CREATE TABLE PersonCrisis (
	id_person	char(100)	NOT NULL
		REFERENCES Person(id),
	id_crisis	char(100)	NOT NULL
		REFERENCES Crisis(id),
	PRIMARY KEY (id_person, id_crisis)
);

CREATE TABLE CrisisKind (
	id	char(100)	NOT NULL
		PRIMARY KEY,
	name	char(100)	NOT NULL,
	description	text NOT NULL
);

CREATE TABLE OrganizationKind (
	id	char(100)	NOT NULL
		PRIMARY KEY,
	name	char(100)	NOT NULL,
	description	text NOT NULL
);

CREATE TABLE PersonKind (
	id	char(100)	NOT NULL
		PRIMARY KEY,
	name	char(100)	NOT NULL,
	description	text NOT NULL
);
