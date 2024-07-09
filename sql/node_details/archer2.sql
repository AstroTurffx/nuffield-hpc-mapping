-- https://www.archer2.ac.uk/about/hardware.html
INSERT INTO node_details (
    system_id, 
    number, 
    processor_name, 
    node_cores, 
    accelerator, 
    memory
) VALUES
(1, 5276, 'AMD EPYC 7742', 128, NULL, 256),
(1, 584, 'AMD EPYC 7742', 128, NULL, 512),
(1, 4, 'AMD EPYC 7534P', 32, '4x AMD Instinct MI210', 512);