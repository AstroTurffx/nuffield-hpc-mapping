SELECT segment, COUNT(*) as 'count'
FROM hpcs, sites
WHERE hpcs.site_id = sites.site_id
GROUP BY segment