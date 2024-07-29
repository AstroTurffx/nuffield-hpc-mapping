UPDATE hpcs
SET total_nodes = (
    SELECT SUM(node_details.number)
    FROM node_details
    WHERE node_details.system_id = hpcs.system_id
);