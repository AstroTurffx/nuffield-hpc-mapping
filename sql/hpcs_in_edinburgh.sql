SELECT hpcs.name, installation_year
FROM sites, hpcs
WHERE sites.site_id = hpcs.site_id
AND sites.city = "Edinburgh"