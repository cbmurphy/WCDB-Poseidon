use cs327e_cbm772;

DROP TABLE if exists Crisis;

CREATE TABLE Crisis (
	id		CHAR(20)	NOT NULL
		PRIMARY KEY,
	name	text	NOT NULL,
	kind	text	NOT NULL
		REFERENCES CrisisKind(id),
	start_date_time	datetime	NOT NULL,
	end_date_time		datetime,
	economic_impact	float	NOT NULL);


insert into Crisis values('japan_earthquake',
	'2011 Great East Japan',
	'EQ',
	'2011-03-11 00:00:01',
	NULL,
	12200000000);

CREATE TABLE Organization (
	id		CHAR(20)	NOT NULL
		PRIMARY KEY,
	name	text	NOT NULL,
	kind	text	NOT	NULL
		REFERENCES OrganizationKind(id),
	history	text	NOT NULL,
	telephone	text,
	fax		text,
	email	text,
	street_address	text,
	locality	text,
	region	text,
	postal_code	text,
	country	text
);

insert into Organization values(
	'ARC',
	'American Red Cross',
	'HO',
	'As one of the nation&apos;s premier...',
	'1 800 733 2767',
	'RedCross@example.com',
	'2025 E Street',
	'Washington',
	'DC',
	'2006',
	'United States');

select * from Crisis;
select * from Organization;

exit
