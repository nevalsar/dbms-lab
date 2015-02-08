-------------------------------------------------
-- Name         : NEVIN VALSARAJ
-- Roll no.     : 12CS10032
-- Submission   : Assignment 3 - CS43002 DBMS Lab
-- Date         : 5 FEB 2015
-------------------------------------------------

-- Solution 1 a)
select pratip_Person.Name, pratip_Movie.Title, YEAR from pratip_Person join pratip_M_Director using(PID) join pratip_Movie using(MID) join pratip_M_Genre using (MID) join pratip_Genre using(GID) where pratip_Genre.Name = 'Comedy' and (YEAR % 4) = 0;

 -- Solution 1 b)
select pratip_Person.Name from pratip_Person join pratip_M_Cast using(PID) join pratip_Movie using(MID) where pratip_Movie.Title = 'Anand' and YEAR = 1971 ;

 -- Solution 1 c)
select Name from pratip_Person where PID IN (select PID from pratip_Person join pratip_M_Cast using(PID) join pratip_Movie using (MID) where YEAR < 1970) and PID in (select PID from pratip_Person join pratip_M_Cast using(PID) join pratip_Movie using (MID) where YEAR >1990) group by (PID);

 -- Solution 1 d)
select Name, count(MID) as movies_directed from pratip_Person join pratip_M_Director using (PID) group by  PID HAVING movies_directed >= 10 order by movies_directed DESC;

 -- Solution 1 e 1)
select YEAR, count(distinct(B.MID)) as female_only from pratip_Movie as B where MID not in (select MID from pratip_M_Cast join pratip_Person using(PID) where Gender = 'male') and MID in (select MID from pratip_M_Cast) group by YEAR;

 -- Solution 1 e 2)
select YEAR, female_only, count(distinct(A.MID)) as total, round(female_only / count(distinct(A.MID)) * 100,2) from pratip_Movie as A join (select YEAR, count(distinct(B.MID)) AS female_only from pratip_Movie as B where MID not in (select MID from pratip_M_Cast join pratip_Person using(PID) where Gender = 'male') and MID in (select MID from pratip_M_Cast) group by  YEAR) as D using(YEAR) group by YEAR;

 -- Solution 1 f)
select Title, actors_count from pratip_Movie join (select MID, count(distinct(PID)) as actors_count from pratip_M_Cast group by  MID) as A using (MID) where actors_count = (select max(actors_count) from (select count(distinct(PID)) as actors_count from pratip_M_Cast group by  MID) as B);

 -- Solution 1 g)
select Decade, movie_count from (select distinct(YEAR - (select min(distinct(YEAR)) from pratip_Movie)) DIV 10 as DecadeID, count(MID) as movie_count, GROUP_CONCAT(distinct(YEAR) order by YEAR asc) as Decade from pratip_Movie group by  DecadeID) as A where movie_count = (select max(movie_count) from
       (select distinct(YEAR -
                          (select min(distinct(YEAR))
                           from pratip_Movie)) DIV 10 AS DecadeID,
                                                   count(MID) AS movie_count
        from pratip_Movie
        group by  DecadeID) AS B);

 -- Solution 1 h)

select Name
from pratip_Person
join pratip_M_Cast AS P using(PID)
group by  P.PID HAVING NOT EXISTS (
                                    (select M2.YEAR - M1.YEAR AS unemployed_years
                                     from pratip_Movie AS M1
                                     join pratip_M_Cast AS P1 ON (P1.MID = M1.MID)
                                     join pratip_M_Cast AS P2 using(PID)
                                     join pratip_Movie AS M2 ON(P2.MID = M2.MID)
                                     where PID = P.PID
                                       and M2.YEAR =
                                         (select MIN(YEAR)
                                          from pratip_Movie
                                          join pratip_M_Cast using(MID)
                                          where PID = P.PID
                                            and YEAR > M1.YEAR)
                                     group by  M1.MID HAVING unemployed_years > 3))
and NOT EXISTS(
                 (select 2015 - M1.YEAR AS unemployed_years
                  from pratip_Movie AS M1
                  join pratip_M_Cast AS P1 ON (P1.MID = M1.MID)
                  join pratip_M_Cast AS P2 using(PID)
                  join pratip_Movie AS M2 ON(P2.MID = M2.MID)
                  where PID = P.PID
                    and M1.YEAR =
                      (select MAX(YEAR)
                       from pratip_Movie
                       join pratip_M_Cast using(MID)
                       where PID = P.PID
                         and YEAR < 2015)
                  group by  M1.MID HAVING unemployed_years > 3));

 -- Solution 1 i)

select DISTINCT (Name)
from pratip_Person
NATURAL join pratip_M_Cast AS P
where
    (select count(distinct(MID))
     from pratip_M_Cast
     join pratip_M_Director using (MID)
     join pratip_Person ON(pratip_M_Director.PID = pratip_Person.PID)
     where pratip_M_Cast.PID = P.PID
       and Name = 'Yash Chopra') > ALL
    (select count(DISTINCT (MID))
     from pratip_M_Cast
     join pratip_M_Director using (MID)
     join pratip_Person ON(pratip_M_Director.PID = pratip_Person.PID)
     where pratip_M_Cast.PID = P.PID
       and Name != 'Yash Chopra')
order by Name;

 -- Solution 1 j)
-- using Shah Rukh Khan's PID

select Name
from pratip_Person
join pratip_M_Cast using(PID)
where PID IN
    (select A.PID
     from pratip_M_Cast AS A
     join pratip_M_Cast AS B ON (A.MID = B.MID)
     where A.PID != B.PID and A.PID != 'nm0451321'
       and B.PID IN
         (select C.PID
          from pratip_M_Cast AS C
          join pratip_M_Cast AS D ON (C.MID = D.MID)
          where C.PID != D.PID
          and D.PID = 'nm0451321'))
group by  PID;
