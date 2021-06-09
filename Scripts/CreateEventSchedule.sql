SET GLOBAL event_scheduler = 1;

DELIMITER $$
CREATE EVENT createSchedule
ON SCHEDULE EVERY '25' MONTH
STARTS '2021-06-08 16:45:00'
DO 
BEGIN
INSERT INTO `GymAdminify`.`Schedule`(`Month`,`Year`)
VALUES(MONTH(current_date())+1,YEAR(current_date()));

UPDATE Room 
SET Schedule = (SELECT ID FROM Schedule ORDER BY ID DESC LIMIT 1)
WHERE ID =(SELECT ID FROM Room ORDER BY ID LIMIT 1);
END$$

DELIMITER ;
SHOW EVENTS FROM GymAdminify;
-- DROP EVENT createSchedule 