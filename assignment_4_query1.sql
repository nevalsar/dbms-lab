------------------------------------------
---  PRANJAL PANDEY                    ---
---  12CS30026                         ---
---  DBMS Assignment 4                 ---
------------------------------------------
-- 1
--a

SELECT pratip_Person.Name,
       pratip_Movie.Title,
       YEAR
FROM pratip_Person
JOIN pratip_M_Director USING(PID)
JOIN pratip_Movie USING(MID)
JOIN pratip_M_Genre USING (MID)
JOIN pratip_Genre USING(GID)
WHERE pratip_Genre.Name = 'Comedy'
  AND (YEAR % 4) = 0 ;

 --b

SELECT pratip_Person.Name
FROM pratip_Person
JOIN pratip_M_Cast USING(PID)
JOIN pratip_Movie USING(MID)
WHERE pratip_Movie.Title = 'Anand'
  AND YEAR = 1971 ;

 --c

SELECT Name
FROM pratip_Person
WHERE PID IN
    (SELECT PID
     FROM pratip_Person
     JOIN pratip_M_Cast USING(PID)
     JOIN pratip_Movie USING (MID)
     WHERE YEAR < 1970)
  AND PID IN
    (SELECT PID
     FROM pratip_Person
     JOIN pratip_M_Cast USING(PID)
     JOIN pratip_Movie USING (MID)
     WHERE YEAR >1990)
GROUP BY(PID);

 --d

SELECT Name,
       count(MID) AS movies_directed
FROM pratip_Person
JOIN pratip_M_Director USING (PID)
GROUP BY PID HAVING movies_directed >= 10
ORDER BY movies_directed DESC;

 --e i

SELECT YEAR,
       count(distinct(B.MID)) AS female_only
FROM pratip_Movie AS B
WHERE MID NOT IN
    (SELECT MID
     FROM pratip_M_Cast
     JOIN pratip_Person USING(PID)
     WHERE Gender = 'male')
  AND MID IN
    (SELECT MID
     FROM pratip_M_Cast)
GROUP BY YEAR;

 --e ii

SELECT YEAR,
       female_only,
       count(distinct(A.MID)) AS total,
       round(female_only / count(distinct(A.MID)) * 100,2)
FROM pratip_Movie AS A
JOIN
  (SELECT YEAR,
          count(distinct(B.MID)) AS female_only
   FROM pratip_Movie AS B
   WHERE MID NOT IN
       (SELECT MID
        FROM pratip_M_Cast
        JOIN pratip_Person USING(PID)
        WHERE Gender = 'male')
     AND MID IN
       (SELECT MID
        FROM pratip_M_Cast)
   GROUP BY YEAR) AS D USING(YEAR)
GROUP BY YEAR;

 --f

SELECT Title,
       actors_count
FROM pratip_Movie
JOIN
  (SELECT MID,
          count(distinct(PID)) AS actors_count
   FROM pratip_M_Cast
   GROUP BY MID) AS A USING (MID)
WHERE actors_count =
    (SELECT max(actors_count)
     FROM
       (SELECT count(distinct(PID)) AS actors_count
        FROM pratip_M_Cast
        GROUP BY MID) AS B);

 --g

SELECT Decade,
       movie_count
FROM
  (SELECT distinct(YEAR -
                     (SELECT min(distinct(YEAR))
                      FROM pratip_Movie)) DIV 10 AS DecadeID,
                                              count(MID) AS movie_count,
                                              GROUP_CONCAT(distinct(YEAR)
                                                           ORDER BY YEAR ASC) AS Decade
   FROM pratip_Movie
   GROUP BY DecadeID) AS A
WHERE movie_count =
    (SELECT max(movie_count)
     FROM
       (SELECT distinct(YEAR -
                          (SELECT min(distinct(YEAR))
                           FROM pratip_Movie)) DIV 10 AS DecadeID,
                                                   count(MID) AS movie_count
        FROM pratip_Movie
        GROUP BY DecadeID) AS B);

 --h

SELECT Name
FROM pratip_Person
JOIN pratip_M_Cast AS P USING(PID)
GROUP BY P.PID HAVING NOT EXISTS (
                                    (SELECT M2.YEAR - M1.YEAR AS unemployed_years
                                     FROM pratip_Movie AS M1
                                     JOIN pratip_M_Cast AS P1 ON (P1.MID = M1.MID)
                                     JOIN pratip_M_Cast AS P2 USING(PID)
                                     JOIN pratip_Movie AS M2 ON(P2.MID = M2.MID)
                                     WHERE PID = P.PID
                                       AND M2.YEAR =
                                         (SELECT MIN(YEAR)
                                          FROM pratip_Movie
                                          JOIN pratip_M_Cast USING(MID)
                                          WHERE PID = P.PID
                                            AND YEAR > M1.YEAR)
                                     GROUP BY M1.MID HAVING unemployed_years > 3))
AND NOT EXISTS(
                 (SELECT 2015 - M1.YEAR AS unemployed_years
                  FROM pratip_Movie AS M1
                  JOIN pratip_M_Cast AS P1 ON (P1.MID = M1.MID)
                  JOIN pratip_M_Cast AS P2 USING(PID)
                  JOIN pratip_Movie AS M2 ON(P2.MID = M2.MID)
                  WHERE PID = P.PID
                    AND M1.YEAR =
                      (SELECT MAX(YEAR)
                       FROM pratip_Movie
                       JOIN pratip_M_Cast USING(MID)
                       WHERE PID = P.PID
                         AND YEAR < 2015)
                  GROUP BY M1.MID HAVING unemployed_years > 3));

 --i

SELECT DISTINCT (Name)
FROM pratip_Person
NATURAL JOIN pratip_M_Cast AS P
WHERE
    (SELECT count(distinct(MID))
     FROM pratip_M_Cast
     JOIN pratip_M_Director USING (MID)
     JOIN pratip_Person ON(pratip_M_Director.PID = pratip_Person.PID)
     WHERE pratip_M_Cast.PID = P.PID
       AND Name = 'Yash Chopra') > ALL
    (SELECT count(DISTINCT (MID))
     FROM pratip_M_Cast
     JOIN pratip_M_Director USING (MID)
     JOIN pratip_Person ON(pratip_M_Director.PID = pratip_Person.PID)
     WHERE pratip_M_Cast.PID = P.PID
       AND Name != 'Yash Chopra')
ORDER BY Name;

 --j
-- Shah Rukh Khan's PID is used instead
SELECT Name
FROM pratip_Person
JOIN pratip_M_Cast USING(PID)
WHERE PID IN
    (SELECT A.PID
     FROM pratip_M_Cast AS A
     JOIN pratip_M_Cast AS B USING (MID)
     JOIN pratip_M_Cast AS C USING (MID)
     WHERE A.PID != C.PID
       AND B.PID != C.PID
       AND C.PID = 'nm0451321'
     )GROUP BY PID;

