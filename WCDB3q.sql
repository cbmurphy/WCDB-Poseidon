USE cs327e_xiaolong;

/*
1. Which people are associated with more than one crisis?
*/
SELECT 'Which people are associated with more than one crisis?' AS 'Query 1';

SELECT first_name, last_name, COUNT(*) AS 'number_of_crises'
FROM Person INNER JOIN PersonCrisis
ON Person.id = PersonCrisis.id_person
GROUP BY Person.id, first_name, last_name
HAVING number_of_crises >= 2
ORDER BY number_of_crises;

/*
2. For the past 5 decades, which countries had the most world crises per decade?
*/
SELECT 'For the past 5 decades, which countries had the most world crises per decade?' AS 'Query 2';
CREATE TABLE Decade (starts int, ends int);
INSERT INTO Decade (starts, ends) VALUES(1960, 1969), (1970, 1979), (1980, 1989), (1990, 1999), (2000, 2009);

CREATE TEMPORARY TABLE R AS
SELECT entity_id, country
FROM Location
WHERE entity_type = 'C';

CREATE TEMPORARY TABLE T1 AS
SELECT starts, ends, country, COUNT(*) AS 'number_of_crises'
FROM Crisis INNER JOIN R
ON Crisis.id = R.entity_id
INNER JOIN Decade
WHERE (YEAR(Crisis.start_date) >= Decade.starts)
  AND (YEAR(Crisis.start_date) <= Decade.ends)
GROUP BY Decade.starts, country;

CREATE TEMPORARY TABLE T2 AS
SELECT starts, MAX(number_of_crises) AS max_crises
FROM T1
GROUP BY starts;

SELECT country, number_of_crises, T1.starts AS 'decade'
FROM T1 INNER JOIN T2 ON T1.starts = T2.starts AND T1.number_of_crises = T2.max_crises
GROUP BY decade;

DROP TABLE R; DROP TABLE T1; DROP TABLE T2; DROP TABLE Decade;

/*
3. What is the average death toll of accident crises?
*/
SELECT 'What is the average death toll of accident crises?' AS 'Query 3';

SELECT AVG(number) AS 'average_death_toll' FROM (
  SELECT number
  FROM Crisis INNER JOIN HumanImpact
  ON Crisis.id = HumanImpact.crisis_id
  WHERE UPPER(HumanImpact.type) = 'DEATH'
  UNION
  SELECT 0 AS number
  FROM Crisis
  WHERE NOT EXISTS (
    SELECT *
    FROM HumanImpact
    WHERE (Crisis.id = HumanImpact.crisis_id) AND (UPPER(HumanImpact.type) = 'DEATH'))
  ) AS T;

/*
4. What is the average death toll of world crises per country?
Same problem as the previous one...
*/
SELECT 'What is the average death toll of world crises per country?' AS 'Query 4';

CREATE TEMPORARY TABLE R AS
SELECT entity_id, country
FROM Location
WHERE entity_type = 'C';

SELECT country, AVG(HumanImpact.number) AS 'average_death_toll'
FROM Crisis INNER JOIN HumanImpact
ON Crisis.id = HumanImpact.crisis_id
INNER JOIN R
ON Crisis.id = R.entity_id
WHERE UPPER(HumanImpact.type) = 'DEATH'
GROUP BY country
ORDER BY average_death_toll;

DROP TABLE R;

/*
5. What is the most common resource needed for different types of disasters?
*/
SELECT 'What is the most common resource needed for different types of disasters?' AS 'Query 5';

CREATE TEMPORARY TABLE R1 AS
SELECT kind, description, COUNT(*) AS 'number'
FROM Crisis INNER JOIN ResourceNeeded
ON Crisis.id = ResourceNeeded.crisis_id
GROUP BY kind, description;

CREATE TEMPORARY TABLE R2 AS
SELECT kind, description, COUNT(*) AS 'number'
FROM Crisis INNER JOIN ResourceNeeded
ON Crisis.id = ResourceNeeded.crisis_id
GROUP BY kind, description;

SELECT kind, description AS 'most_common_resource_needed', number
FROM R1
WHERE number >= ALL(
  SELECT number
  FROM R2
  WHERE R1.kind = R2.kind
);

DROP TABLE R1;
DROP TABLE R2;

/*
6. How many persons are related to crises located in countries other than their own?
*/
SELECT 'How many persons are related to crises located in countries other than their own?' AS 'Query 6';

CREATE TEMPORARY TABLE R AS
SELECT entity_id, country
FROM Location
WHERE entity_type = 'C';

CREATE TEMPORARY TABLE S1 AS
SELECT entity_id, country
FROM Location
WHERE entity_type = 'P';

CREATE TEMPORARY TABLE S2 AS
SELECT entity_id, country
FROM Location
WHERE entity_type = 'P';


SELECT CONCAT(P1.first_name, ' ', P1.last_name) AS 'name'
FROM Person AS P1 INNER JOIN S1
ON P1.id = S1.entity_id
WHERE EXISTS(
  SELECT *
  FROM PersonCrisis INNER JOIN Crisis
  ON PersonCrisis.id_crisis = Crisis.id
  INNER JOIN R
  ON R.entity_id = Crisis.id
  WHERE (id_person = P1.id) AND (R.country NOT IN(
    SELECT country
    FROM Person AS P2 INNER JOIN S2
    ON P2.id = S2.entity_id
    WHERE P2.id = P1.id
  ))
);

DROP TABLE R;
DROP TABLE S1;
DROP TABLE S2;

/*
7. How many crises occurred during the 1960s?
*/
SELECT 'How many crises occurred during the 1960s?' AS 'Query 7';

SELECT COUNT(*)
FROM Crisis
WHERE (YEAR(start_date) >= 1960) AND (YEAR(start_date) <= 1969);

/*
8. Which orgs are located outside the United States and were involved in more than 1 crisis?
*/
SELECT 'Which orgs are located outside the United States and were involved in more than 1 crisis?' AS 'Query 8';

SELECT name
FROM Organization
WHERE EXISTS (
  SELECT *
  FROM CrisisOrganization
  WHERE id_organization = Organization.id
)
AND EXISTS (
  SELECT *
  FROM Location
  WHERE (entity_type = 'O') AND (entity_id = Organization.id)
    AND (UPPER(country) != 'US') AND (UPPER(country) != 'UNITED STATES')
    AND (UPPER(country) != 'UNITED STATES OF AMERICA')
);

/*
9. Which Orgs, Crises, and Persons have the same location?
This query is rather ambiguous.
*/
SELECT 'Which Orgs, Crises, and Persons have the same location?' AS 'Query 9';

SELECT * FROM (
  SELECT id, country, region, locality
  FROM Organization
  UNION
  SELECT Crisis.id AS id, country, region, locality
  FROM Crisis INNER JOIN Location
  ON Crisis.id = Location.entity_id
  WHERE Location.entity_type = 'C'
  UNION
  SELECT Person.id AS id, country, region, locality
  FROM Person INNER JOIN Location
  ON Person.id = Location.entity_id
  WHERE Location.entity_type = 'P'
) AS T
GROUP BY country, region, locality;

/*
10. Which crisis has the minumum Human Impact?
*/
SELECT 'Which crisis has the minumum Human Impact?' AS 'Query 10';

CREATE TEMPORARY TABLE R AS
SELECT Crisis.id, SUM(number) AS total_human_impact
FROM Crisis INNER JOIN HumanImpact
ON Crisis.id = HumanImpact.crisis_id
GROUP BY id;

SELECT MIN(total_human_impact) INTO @x
FROM R;

SELECT name
FROM R INNER JOIN Crisis
ON (Crisis.id = R.id)
WHERE total_human_impact <= @x;

DROP TABLE R;

/*
11. Count the number of crises that each organization helped.
Involeved instead of helped?
*/
SELECT 'Count the number of crises that each organization helped.' AS 'Query 11';

SELECT id_organization AS 'organization', COUNT(*) AS 'number_of_crises'
FROM CrisisOrganization
GROUP BY id_organization
UNION
SELECT id AS 'organization', 0 AS 'number_of_crises'
FROM Organization
WHERE id NOT IN (SELECT id_organization FROM CrisisOrganization);

/*
12. Name and Postal Address of all orgs in California.
*/
SELECT 'Name and Postal Address of all orgs in California.' AS 'Query 12';

SELECT name, street_address, locality, region, postal_code, country
FROM Organization
WHERE (UPPER(region) = 'CA') OR (UPPER(region) = 'CALIFORNIA');

/*
13. List all crises that happened in the same state/region.
We will just list all crises that happened by region...
*/
SELECT 'List all crises that happened in the same state/region.' AS 'Query 13';

SELECT name, region
FROM Crisis INNER JOIN Location
ON (Crisis.id = Location.entity_id)
WHERE (Location.entity_type = 'C') AND (region IS NOT NULL)
GROUP BY region;

/*
14. Find the total number of human casualties caused by crises in the 1990s.
*/
SELECT 'Find the total number of human casualties caused by crises in the 1990s.' AS 'Query 14';

SELECT SUM(number) AS 'total_casualties'
FROM Crisis INNER JOIN HumanImpact
ON (Crisis.id = HumanImpact.crisis_id)
WHERE (UPPER(HumanImpact.type) = 'DEATH')
AND (YEAR(start_date) >= 1990) AND (YEAR(start_date) <= 1999);

/*
15. Find the organization(s) that has provided support on the most Crises.
*/
SELECT 'Find the organization(s) that has provided support on the most Crises.'
AS 'Query 15';

SELECT id_organization
FROM CrisisOrganization
GROUP BY id_organization
HAVING COUNT(*) = (
  SELECT MAX(num)
  FROM (
    SELECT COUNT(*) AS 'num'
    FROM CrisisOrganization
    GROUP BY id_organization) AS T
);

/*
16. How many orgs are government based?
*/
SELECT 'How many orgs are government based?' AS 'Query 16';

SELECT name AS 'government_based_orgs'
FROM Organization
WHERE kind IN ('AD', 'CB', 'GMB', 'GOV', 'IA', 'NG', 'NS');

/*
17. What is the total number of casualties across the DB?
*/
SELECT 'What is the total number of casualties across the DB?' AS 'Query 17';

SELECT SUM(number) AS 'total_casualties'
FROM HumanImpact
WHERE (UPPER(type) = 'DEATH');

/*
18. What is the most common type/kind of crisis occuring in the DB?
*/
SELECT 'What is the most common type/kind of crisis occuring in the DB?' AS 'Query 18';

CREATE TEMPORARY TABLE R AS
SELECT kind, COUNT(*) AS 'number_of_crises'
FROM Crisis
GROUP BY kind;

SELECT MAX(number_of_crises) INTO @x
FROM R;

SELECT *
FROM R
WHERE number_of_crises = @x;

DROP TABLE R;

/*
19. Create a list of telephone numbers, emails, and other contact info for all orgs.
*/
SELECT 'Create a list of telephone numbers, emails, and other contact info for all orgs.' AS 'Query 19';

SELECT name, telephone, fax, email, street_address, locality, region, postal_code, country
FROM Organization;

/*
20. What is the longest-lasting crisis? (if no end date, then ignore)
*/
SELECT 'What is the longest-lasting crisis? (if no end date, then ignore)' AS 'Query 20';

SELECT name, start_date, end_date
FROM Crisis
WHERE (end_date IS NOT NULL) AND (DATEDIFF(end_date, start_date) = (
  SELECT MAX(DATEDIFF(end_date, start_date))
  FROM Crisis
  WHERE (end_date IS NOT NULL)));

/* 21. Which person(s) is involved or associated with the most organizations? */
SELECT 'Which person(s) is involved or associated with the most organizations?' AS 'Query 21';

CREATE temporary TABLE T AS
  (SELECT Person.id, Person.first_name, Person.middle_name, Person.last_name, 
     count(distinct OrganizationPerson.id_organization) AS 'counts'
    FROM Person INNER JOIN OrganizationPerson
    ON Person.id = OrganizationPerson.id_person
    GROUP BY Person.id);

SELECT MAX(counts) INTO @x FROM T;

SELECT first_name, middle_name, last_name
  FROM T
  WHERE counts = @x;

DROP TABLE T;

/* 22. How many hurricane crises? */
SELECT 'How many hurricane crises?' AS 'Query 22';

SELECT count(id)
  FROM Crisis
  WHERE kind = 'HU';

/*23. Name all humanitarian organizations in the DB. */
SELECT 'Name all humanitarian organizations in the DB.' AS 'Query 23';

SELECT name
  FROM Organization
  WHERE kind = 'HO';

/*24. List the crises in the order when they occurred (earliest to latest)*/
SELECT 'List the crises in the order when they occurred (earliest to latest)' AS 'Query 24';

SELECT name, start_date
  FROM Crisis
  ORDER BY start_date ASC;

/*25. Get the name and kind of all person in the United States of America*/
SELECT 'Get the name and kind of all person in the United States of America' AS 'Query 25';

SELECT a.first_name, a.middle_name, a.last_name, a.kind
  FROM Person a 
    INNER JOIN Location b
    ON (a.id = b.entity_id)
  WHERE b.country = 'United States';

/*26. Who has the longest name?*/
SELECT 'Who has the longest name?' AS 'Query 26';

create temporary table T as
 (SELECT first_name, middle_name, last_name, 
  LENGTH(first_name) + IFNULL(LENGTH(middle_name), 0) + LENGTH(last_name) AS len 
    FROM Person);

SELECT MAX(len) INTO @x FROM T;

SELECT first_name, middle_name, last_name
  FROM T
  WHERE len = @x;

DROP TABLE T;

/*27. Which kinds of crisis only have one crisis example?*/
SELECT 'Which kinds of crisis only have one crisis example?' AS 'Query 27';

CREATE temporary TABLE T AS
  (SELECT CrisisKind.id, Crisis.name
    FROM Crisis INNER JOIN CrisisKind
    ON CrisisKind.id = Crisis.kind);

SELECT id, name
  FROM T
  GROUP BY id
  HAVING COUNT(*) = 1;

DROP TABLE T;

/*28. Which people don't have a middle name?*/
SELECT 'Which people dont have a middle name?' AS 'Query 28';

SELECT first_name, middle_name, last_name
  FROM Person
  WHERE middle_name is NULL;

/*29. What are the names that start with 'B'?*/
SELECT 'What are the names that start with B?' AS 'Query 29';

SELECT first_name, middle_name, last_name
  FROM Person
  WHERE LEFT(first_name, 1) = 'B';

/*30. List all the people associated with each country.*/
SELECT 'List all the people associated with each country.' AS 'Query 30';

SELECT Location.country, Person.first_name, Person.middle_name,   
  Person.last_name
  FROM Person INNER JOIN Location
  ON (Person.id = Location.entity_id)
  ORDER BY Location.country;

/*31. What crisis affected the most countries?*/
SELECT 'What crisis affected the most countries?' AS 'Query 31';

CREATE temporary table T AS
  (SELECT Crisis.id, Crisis.name, count(distinct Location.country) as 'num_countries'
    FROM Crisis INNER JOIN Location
    ON Location.entity_id = Crisis.id
    WHERE Location.entity_type = 'C'
    GROUP BY Crisis.id);

SELECT MAX(num_countries) INTO @x FROM T;

SELECT name
  FROM T
  WHERE num_countries = @x;

DROP table T;

/*32. What is the first (earliest) crisis in the first database?*/
SELECT 'What is the first (earliest) crisis in the first database?' AS 'Query 32';

SELECT name
  FROM Crisis
  WHERE start_date <= ALL
  (SELECT start_date 
    FROM Crisis);

/*33. Number of organizations in the US?*/
SELECT 'Number of organizations in the US?' AS 'Query 33';

SELECT count(id) FROM Organization
WHERE UPPER(country) IN ('UNITED STATES OF AMERICA', 'US', 'UNITED STATES');

/*34. How many people are singers?*/
SELECT 'How many people are singers?' AS 'Query 34';

SELECT count(id) AS 'num_singers' FROM Person WHERE kind = 'SNG';

/*35. Number of current or former leaders?*/
SELECT 'Number of current or former leaders?' AS 'Query 35';

SELECT count(id) AS 'num_leaders' FROM Person WHERE kind = 'LD';

/*36. Find the start date of every hurricane that occurred in the U.S.*/
SELECT 'Find the start date of every hurricane that occurred in the U.S.' AS 'Query 36';

SELECT distinct name AS 'US_hurricane', start_date FROM Crisis INNER JOIN Location ON Crisis.id = Location.entity_id WHERE UPPER(country) IN ('UNITED STATES OF AMERICA', 'US', 'UNITED STATES')
AND kind = 'HU';


/*37. Number of natural disasters occurring where June 5th 2000 to Jun 5th 2012.*/
SELECT 'Number of natural disasters occurring where June 5th 2000 to Jun 5th 2012.' AS 'Query 37';

SELECT count(*) as 'num_disasters' FROM Crisis WHERE kind in ('EQ', 'FR', 'FL', 'HU', 'ME', 'ST', 'TO', 'TS', 'VO') AND start_date >= '2000-06-05' AND start_date <= '2012-06-05';


/*38. Number of political figures grouped by country*/
SELECT 'Number of political figures grouped by country' AS 'Query 38';

SELECT count(*) AS 'num_political figures', country FROM Person INNER JOIN Location ON Person.id = Location.entity_id WHERE kind = 'PR' or kind = 'PM' or kind = 'VP' GROUP BY country;

/*39. Location with the most number of natural disasters.*/
SELECT 'Location with the most number of natural disasters.' AS 'Query 39';

CREATE temporary TABLE T AS
SELECT country, count(*) AS 'num_disasters' FROM Location INNER JOIN Crisis ON Location.entity_id = Crisis.id WHERE kind in ('EQ', 'FR', 'FL', 'HU', 'ME', 'ST', 'TO', 'TS', 'VO') GROUP BY country;

SELECT max(num_disasters) INTO @x FROM T;

SELECT country FROM T WHERE num_disasters = @x;

drop table T;


/*40. Average number of deaths caused by hurricanes.*/
SELECT 'Average number of deaths caused by hurricanes.' AS 'Query 40';

SELECT avg(number) AS 'avg_HU_deaths' FROM HumanImpact INNER JOIN Crisis ON HumanImpact.crisis_id = Crisis.id WHERE type = 'Death' AND kind = 'HU';

/*41.	Total number of deaths caused by terrorist attacks*/
SELECT 'Total number of deaths caused by terrorist attacks' AS 'Query 41';

SELECT sum(number) AS 'deaths' FROM HumanImpact INNER JOIN Crisis ON HumanImpact.crisis_id = Crisis.id WHERE type = 'Death' AND kind = 'TA';

/*42.	List of Hurricanes in the US that Wallace Stickney (WStickney) helped out with.*/
SELECT 'List of Hurricanes in the US that Wallace Stickney (WStickney) helped out with.' AS 'Query 42';

SELECT distinct name FROM Crisis INNER JOIN PersonCrisis ON Crisis.id = PersonCrisis.id_crisis WHERE id_person = 'WStickney' AND kind = 'HU';


/*43.	List of hurricanes in the US where FEMA was NOT involved.*/
SELECT 'List of hurricanes in the US where FEMA was NOT involved.' AS 'Query 43';

SELECT distinct name FROM Crisis INNER JOIN Location ON Crisis.id = Location.entity_id WHERE Crisis.id not in (SELECT id_crisis FROM CrisisOrganization WHERE id_organization = 'FEMA') AND UPPER(country) IN ('UNITED STATES OF AMERICA', 'US', 'UNITED STATES') AND kind = 'HU';


/*44.	 Number of crises that intelligence agencies were involved in.*/
SELECT 'Number of crises that intelligence agencies were involved in.' AS 'Query 44';

SELECT count(*) AS 'num_crises' FROM Crisis INNER JOIN CrisisOrganization ON Crisis.id = CrisisOrganization.id_crisis WHERE id_organization in (SELECT id FROM Organization WHERE kind = 'IA');


/*45.	How many more orgs does America have than Britain.*/
SELECT 'How many more orgs does America have than Britain.' AS 'Query 45';

SELECT R.x- S.y AS 'more_orgs' FROM (SELECT count(distinct Organization.id) AS x FROM Organization WHERE country = 'United States') AS R, (SELECT count(distinct Organization.id) AS y FROM Organization WHERE country = 'United Kingdom') AS S;

