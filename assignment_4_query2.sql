------------------------------------------
---  PRANJAL PANDEY                    ---
---  12CS30026                         ---
---  DBMS Assignment 4                 ---
------------------------------------------
 --a

SELECT title
FROM (pratip_Movie
      NATURAL JOIN pratip_M_Cast)
WHERE year  = 1970
GROUP BY MID
ORDER BY count(*) DESC;

 --b

SELECT Name
FROM ((pratip_Person
       NATURAL JOIN pratip_M_Cast)
      JOIN
        (SELECT *
         FROM pratip_Movie
         WHERE YEAR > 1990) AS post_1990_movies USING (MID))
GROUP BY PID HAVING count(*) > 13;

 --c

SELECT AN.name,
       BN.name
FROM pratip_M_Cast AS A
JOIN pratip_Person AS AN ON(A.PID=AN.PID)
JOIN pratip_M_Cast AS B ON(A.MID=B.MID)
JOIN pratip_Person AS BN ON (B.PID=BN.PID)
WHERE A.PID<B.PID
GROUP BY A.PID,
         B.PID HAVING count(distinct(A.MID))>10;

 --d
/* NO ACTOR IS BIG OR SMALL IN EYE OF MYSQL */ --e


--e
SELECT YEAR
FROM pratip_M_Cast
NATURAL JOIN pratip_Movie
WHERE PID =
    (SELECT PID
     FROM pratip_Person
     WHERE Name = "Amitabh Bachchan")
GROUP BY YEAR HAVING count(*) =
  (SELECT max(COUNT)
   FROM
     (SELECT COUNT(*) AS COUNT
      FROM pratip_M_Cast
      NATURAL JOIN pratip_Movie
      WHERE PID=
          (SELECT PID
           FROM pratip_Person
           WHERE Name= "Amitabh Bachchan")
      GROUP BY YEAR) AS A);

 --f

SELECT A.Name,
       C.Name
FROM pratip_M_Cast
NATURAL JOIN pratip_Person AS A
JOIN pratip_M_Cast AS B USING (MID)
JOIN pratip_Person AS C ON (B.PID = C.PID)
WHERE C.Name = "Om Puri"
  AND A.Name != 'Om Puri'
GROUP BY A.PID;

 -- g-a

SELECT P.Name
FROM pratip_Movie AS M
NATURAL JOIN pratip_M_Director AS D
JOIN pratip_M_Cast AS C ON (M.MID = C.MID)
JOIN pratip_Person AS P ON (P.PID = C.PID)
GROUP BY D.PID,
         C.PID
ORDER BY COUNT(*) DESC LIMIT 1;

 -- g-b

SELECT P.Name
FROM pratip_Movie AS M
NATURAL JOIN pratip_M_Producer AS D
JOIN pratip_M_Cast AS C ON (M.MID = C.MID)
JOIN pratip_Person AS P ON (P.PID = C.PID)
GROUP BY D.PID,
         C.PID
ORDER BY COUNT(*) DESC LIMIT 1;

 --h

SELECT Name
FROM pratip_Movie AS M
NATURAL JOIN pratip_M_Cast AS C
JOIN pratip_Person AS P ON (C.PID = P.PID)
WHERE title LIKE 'Dhoom%'
GROUP BY C.PID HAVING COUNT(DISTINCT MID) =
  (SELECT COUNT(*)
   FROM pratip_Movie
   WHERE title LIKE "Dhoom%");