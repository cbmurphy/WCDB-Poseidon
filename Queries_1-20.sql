/*
1. Which people are associated with more than one crisis?
*/
SELECT first_name, last_name, COUNT(*) AS 'number_of_cirses'
FROM Person INNER JOIN PersonCrisis
ON Person.id = PersonCrisis.id_person
GROUP BY Person.id, first_name, last_name
HAVING number_of_cirses >= 2
ORDER BY number_of_cirses;

/*
2. For the past 5 decades, which countries had the most world crises per decade?
*/
CREATE TEMPORARY TABLE R AS
SELECT entity_id, country
FROM Location
WHERE entity_type = 'C';

CREATE TEMPORARY TABLE T1 AS
SELECT country, COUNT(*) AS 'number_of_crises'
FROM Crisis INNER JOIN R
ON Crisis.id = R.entity_id
WHERE YEAR(Crisis.start_date) > 1963
GROUP BY country;

CREATE TEMPORARY TABLE T2 AS
SELECT country, COUNT(*) AS 'number_of_crises'
FROM Crisis INNER JOIN R
ON Crisis.id = R.entity_id
WHERE YEAR(Crisis.start_date) > 1963
GROUP BY country;

SELECT country, number_of_crises / 5 AS 'crises_per_decade'
FROM T1
WHERE T1.number_of_crises >= (
  SELECT MAX(T2.number_of_crises)
  FROM T2
);

DROP TABLE R;
DROP TABLE T1;
DROP TABLE T2;

/*
3. What is the average death toll of accident crises?
*/
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
SELECT COUNT(*)
FROM Crisis
WHERE (YEAR(start_date) >= 1960) AND (YEAR(start_date) <= 1969);

/*
8. Which orgs are located outside the United States and were involved in more than 1 crisis?
*/
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
);

/*
9. Which Orgs, Crises, and Persons have the same location?
This query is rather ambiguous.
*/
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
SELECT name, street_address, locality, region, postal_code, country
FROM Organization
WHERE (UPPER(region) = 'CA') OR (UPPER(region) = 'CALIFORNIA');

/*
13. List all crises that happened in the same state/region.
We will just list all crises that happened by region...
*/
SELECT name, region
FROM Crisis INNER JOIN Location
ON (Crisis.id = Location.entity_id)
WHERE (Location.entity_type = 'C') AND (region IS NOT NULL)
GROUP BY region;

/*
14. Find the total number of human casualties caused by crises in the 1990s.
*/
SELECT SUM(number) AS 'total_casualties'
FROM Crisis INNER JOIN HumanImpact
ON (Crisis.id = HumanImpact.crisis_id)
WHERE (UPPER(HumanImpact.type) = 'DEATH')
AND (YEAR(start_date) >= 1990) AND (YEAR(start_date) <= 1999);

/*
15. How many orgs are government based?
*/
SELECT name AS 'government_based_orgs'
FROM Organization
WHERE kind IN ('AD', 'CB', 'GMB', 'GOV', 'IA', 'NG', 'NS');

/*
16. What is the total number of casualties across the DB?
*/
SELECT SUM(number) AS 'total_casualties'
FROM HumanImpact
WHERE (UPPER(type) = 'DEATH');

/*
17. What is the most common type/kind of crisis occuring in the DB?
*/
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
SELECT name, telephone, fax, email, street_address, locality, region, postal_code, country
FROM Organization;

/*
20. What is the longest-lasting crisis? (if no end date, then ignore)
*/
SELECT name, start_date, end_date
FROM Crisis
WHERE (end_date IS NOT NULL) AND (DATEDIFF(end_date, start_date) = (
  SELECT MAX(DATEDIFF(end_date, start_date))
  FROM Crisis
  WHERE (end_date IS NOT NULL)));
