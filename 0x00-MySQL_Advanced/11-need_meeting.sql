-- create views for students who need a meeting
CREATE VIEW need_meeting AS
SELECT name FROM students
WHERE score < 80 AND (last_meeting IS NULL OR last_meeting > 1)