-- find the average score for a user 
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    SELECT user_id, project_id, AVG(score) AS average_score
    FROM corrections
    WHERE user_id = user_id
    GROUP BY user_id, project_id;
END$$

DELIMITER ;