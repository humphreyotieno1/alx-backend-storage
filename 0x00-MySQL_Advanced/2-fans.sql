-- Rank country origins of bands by number of fans
-- Output country and number of fans
SELECT origin, SUM(fans) AS nb_fans FROM metal_bands
GROUP BY (origin)
ORDER BY SUM(fans) DESC;