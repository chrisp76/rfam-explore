WITH source AS (
    SELECT * FROM genome
)

SELECT
    upid,
    assembly_acc,
    COALESCE(assembly_version, 0) as assembly_version,
    wgs_acc,
    COALESCE(wgs_version, 0) as wgs_version,
    COALESCE(assembly_name, 'Unknown') as assembly_name,
    COALESCE(assembly_level, 'Unknown') as assembly_level,
    COALESCE(study_ref, 'Unknown') as study_ref,
    COALESCE(description, 'Unknown') as description,
    total_length,
    COALESCE(ungapped_length, 0) as ungapped_length,
    COALESCE(circular, 0) as circular,
    COALESCE(ncbi_id, 0) as ncbi_id,
    COALESCE(scientific_name, 'Unknown') as scientific_name,
    COALESCE(common_name, 'Unknown') as common_name,
    COALESCE(kingdom, 'Unknown') as kingdom,
    COALESCE(num_rfam_regions, 0) as num_rfam_regions,
    COALESCE(num_families, 0) as num_families,
    COALESCE(is_reference, 0) as is_reference,
    COALESCE(is_representative, 0) as is_representative,
    created,
    updated
FROM source 