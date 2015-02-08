-------------------------------------------------
-- Name         : NEVIN VALSARAJ
-- Roll no.     : 12CS10032
-- Submission   : Assignment 3 - CS43002 DBMS Lab
-- Date         : 5 FEB 2015
-------------------------------------------------

-- Solution 2 a)
select title from (pratip_Movie natural join pratip_M_Cast) where year = 1970 group by MID order by count(*) desc;

-- Solution 2 b)
select Name from ((pratip_Person natural join pratip_M_Cast) join (select * from pratip_Movie where year > 1990) as post_1990_movies using (MID)) group by PID having count(*) > 13;

 -- Solution 2 c)
select AN.name, BN.name from pratip_M_Cast as A join pratip_Person as AN on (A.PID=AN.PID) join pratip_M_Cast as B on(A.ID=B.MID) join pratip_Person as BN on (B.PID=BN.PID) where  A.PID < B.PID group by A.PID, B.PID having count(distinct(A.MID)) > 10;

 -- Solution 2 d)

-- Solution 2 e)
select year from pratip_M_Cast natural join pratip_Movie where PID = (select PID from pratip_Person where Name =  "Amitabh Bachchan") group by year having count(*) = (select max(count) from (select count(*) as count from pratip_M_Cast natural join pratip_Movie where PID=(select PID from pratip_Person where Name= "Amitabh Bachchan") group by year) as A);

-- Solution 2 f)
select A.Name, C.Name from pratip_M_Cast natural join pratip_Person as A join pratip_M_Cast as B using (MID) join pratip_Person as C on (B.PID = C.PID ) where C.Name = "Om Puri" and A.Name != "Om Puri" group by A.PID;

-- Solution 2 g - a)
select P.Name from pratip_Movie as M natural join pratip_M_Director as D join pratip_M_Cast as C on (M.MID = C.MID) join pratip_Person as P on (P.PID = C.PID) group by D.PID, C.PID order by count(*) desc limit 1;

-- Solution 2 g - b)
select P.Name from pratip_Movie as M natural join pratip_M_Producer as D join pratip_M_Cast as C on (M.MID = C.MID) join pratip_Person as P on (P.PID = C.PID) group by D.PID, C.PID order by count(*) desc limit 1;


-- Solution 2 h)
select Name from pratip_Movie as M natural join pratip_M_Cast as C join pratip_Person as P on (C.PID = P.PID) where title like 'Dhoom%' group by C.PID having count(distinct MID) = (select count(*) from pratip_Movie where title like "Dhoom%");
