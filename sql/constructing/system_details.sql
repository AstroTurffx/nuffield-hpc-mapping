-- Default 'system_status' to 'Active'
UPDATE hpcs SET system_status="Active";

--- ARCHER 2 --- https://www.archer2.ac.uk/about/hardware.html
UPDATE hpcs SET system_tier=1, system_type="CPU"
WHERE system_id=180036;

INSERT INTO node_details (system_id, number, processor_name, node_cores, accelerator, memory) VALUES
(180036, 5276, 'AMD EPYC 7742', 128, NULL, 256),
(180036, 584, 'AMD EPYC 7742', 128, NULL, 512),
(180036, 4, 'AMD EPYC 7534P', 32, '4x AMD Instinct MI210', 512);

--- Dawn --- https://docs.hpc.cam.ac.uk/hpc/user-guide/pvc.html
UPDATE hpcs SET system_tier=2
WHERE system_id=180202;

INSERT INTO node_details (system_id, number, processor_name, node_cores, accelerator, memory) VALUES
(180202, 256, 'Intel Xeon Platinum 8468', 96, '4x Intel(R) Data Center GPU Max 1550', 1024);

--- DiRAC, Tursa --- https://www.epcc.ed.ac.uk/hpc-services/dirac-tursa-gpu
UPDATE hpcs SET system_tier=2, system_type="GPU"
WHERE system_id=180018;

INSERT INTO node_details (system_id, number, processor_name, node_cores, accelerator, memory) VALUES
(180018, 64, 'AMD EPYC 7413', 48, '4x NVIDIA Ampere A100-80', 1024),
(180018, 114, 'AMD EPYC 7302', 32, '4x NVIDIA Ampere A100-40', 1024),
(180018, 6, 'AMD EPYC ROME 7H12', 128, NULL, 256);

--- Isambard-AI phase 1 --- https://nowlab.cse.ohio-state.edu/static/media/workshops/presentations/exacomm24/IsambardDRIsExaCommISC2024-final.pdf
UPDATE hpcs SET system_tier=2, system_type="AI Accelerator"
WHERE system_id=180257;

UPDATE hpcs SET system_tier=2 WHERE system_id=180257;
INSERT INTO node_details (system_id, number, processor_name, node_cores, accelerator, memory) VALUES
(180257, 168, 'NVIDIA Grace', 72, 'NVIDIA Hopper', 512);

--- Baskerville --- https://docs.baskerville.ac.uk/system/
UPDATE hpcs SET system_tier=2, system_type="GPU"
WHERE system_id=180243;

INSERT INTO node_details (system_id, number, processor_name, node_cores, accelerator, memory) VALUES
(180243, 6, 'Intel Xeon Platinum 8360Y', 72, '4x NVIDIA Ampere A100-80', 512),
(180243, 46, 'Intel Xeon Platinum 8360Y', 72, '4x NVIDIA Ampere A100-40', 512);

--- Wilkes-3 --- https://docs.hpc.cam.ac.uk/hpc/user-guide/a100.html
UPDATE hpcs SET system_tier=2, system_type="GPU"
WHERE system_id=180046;

INSERT INTO node_details (system_id, number, processor_name, node_cores, accelerator, memory) VALUES
(180046, 90, 'AMD EPYC 7763', 128, '4x NVIDIA Ampere A100-SXM-80', 1000);