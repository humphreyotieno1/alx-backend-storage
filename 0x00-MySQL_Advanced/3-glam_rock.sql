-- list bands with Glam as main style
-- Output band name and style
SELECT band_name, (2022 - YEAR(formed)) AS lifespan
FROM metal_bands
WHERE FIND_IN_SET('Glam rock', split)
ORDER BY lifespan DESC;