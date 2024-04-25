-- Create trigger to decrease item quantity after order
DROP TRIGGER IF EXISTS decrease_item;
DELIMITER $$

CREATE TRIGGER decrease_item
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END$$

DELIMITER ;