-- Default 'system_status' to 'Active'
UPDATE hpcs SET system_status="Active";

--- ARCHER 2 --- https://www.archer2.ac.uk/about/hardware.html
UPDATE hpcs SET system_tier=1, system_type="CPU"
WHERE system_id=180036;

INSERT INTO node_details (system_id, number, processor_name, node_cores, accelerator, memory) VALUES
(180036, 5276, 'AMD EPYC 7742', 128, NULL, 256),
(180036, 584, 'AMD EPYC 7742', 128, NULL, 512),
(180036, 4, 'AMD EPYC 7534P', 32, '4x AMD Instinct MI210', 512);

--- Dawn ---
UPDATE hpcs SET system_tier=2 WHERE name="Dawn";

--- DiRAC, Tursa --- https://www.epcc.ed.ac.uk/hpc-services/dirac-tursa-gpu
UPDATE hpcs SET system_tier=2, system_type="GPU"
WHERE system_id=180018;

INSERT INTO node_details (system_id, number, processor_name, node_cores, accelerator, memory) VALUES
(180018, 64, 'AMD EPYC 7413', 48, '4x NVIDIA Ampere A100-80', 1024),
(180018, 114, 'AMD EPYC 7302', 32, '4x NVIDIA Ampere A100-40', 1024),
(180018, 6, 'AMD EPYC ROME 7H12', 128, NULL, 256);

--- Isambard-AI phase 1 ---
UPDATE hpcs SET system_tier=2, system_type="AI Accelerator"
WHERE system_id=180257;
UPDATE hpcs SET system_tier=2 WHERE system_id=180257;
INSERT INTO node_details (system_id, number, processor_name, node_cores, accelerator, memory) VALUES
(180257, 476, 'NVIDIA Grace', 72, 'NVIDIA Hopper', 480)