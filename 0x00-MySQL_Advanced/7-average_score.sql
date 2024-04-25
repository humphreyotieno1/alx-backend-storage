-- find the average score for a user 
DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE total_projects INT;
    DECLARE avg_score FLOAT;
    
    SELECT SUM(score) INTO total_score FROM corrections WHERE user_id = user_id;
    SELECT COUNT(*) INTO total_projects FROM corrections WHERE user_id = user_id;
    
    IF total_projects > 0 THEN
        SET avg_score = total_score / total_projects;
    ELSE
        SET avg_score = 0;
    END IF;
    
    UPDATE users SET average_score = avg_score WHERE id = user_id;
END //
DELIMITER ;