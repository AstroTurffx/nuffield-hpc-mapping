--- https://www.epcc.ed.ac.uk/hpc-services/dirac-tursa-gpu
-- not running this, the website is unclear or bi-polar
INSERT INTO node_details (
    system_id, 
    number, 
    processor_name, 
    node_cores, 
    accelerator, 
    memory
) VALUES
(180018, 64, 'AMD EPYC 7413', 24, '4x NVIDIA Ampere A100-80', 1024),
(180018, 114, 'AMD EPYC 7302', 32, '4x NVIDIA Ampere A100-40', 1024),
(180018, 6, 'AMD EPYC ROME 7H12', 128, NULL, 256);