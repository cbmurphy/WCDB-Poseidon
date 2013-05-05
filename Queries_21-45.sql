/* 21. Which person(s) is involved or associated with the most organizations? */

SELECT a.id, a.first_name, a.middle_name, a.last_name, count(a.id) AS "Organizations"
  FROM Person a 
    INNER JOIN OrganizationPerson b
    ON (a.id = b.id_person)
  GROUP BY a.id;

SELECT a.id, a.first_name, a.middle_name, a.last_name, max(c) AS "Organizations"
  FROM
    (SELECT count(a.id) AS c
      FROM Person a 
      INNER JOIN OrganizationPerson b
      ON (a.id = b.id_person) as d
    GROUP BY a.id);
	************
/* 22. How many hurricane crises? */

SELECT count(id)
  FROM Crisis
  WHERE kind = 'HU';

/*23. Name all humanitarian organizations in the DB. */
SELECT name
  FROM Organization
  WHERE kind = 'HO';

/*24. List the crises in the order when they occurred (earliest to latest)*/
SELECT name, start_date
  FROM Crisis
  ORDER BY start_date ASC

/*25. Get the name and kind of all person in the United States of America*/
SELECT a.first_name, a.middle_name, a.last_name, a.kind
  FROM Person a 
    INNER JOIN Location b
    ON (a.id = b.entity_id)
  WHERE b.country = 'United States'

/*26. Who has the longest name?*/
SELECT name, max("Character ")
  FROM Person
  WHERE name IN
    (SELECT name, CHARACTER_LENGTH(name) AS "Character Length"
      FROM Person);
************
/**/
/*
go on python
from WCDB2_import import *
from WCDB2 import *
from lsml import etree as ET
root = ET.parse("WCDB2.xml")
wcdb2_import(root)

go on another terminal
mysql -h z -u username -p password
use cs327e-surely */
