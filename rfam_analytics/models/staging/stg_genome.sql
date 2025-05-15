WITH source AS (
    SELECT * FROM genome
)

SELECT
    upid,
    assembly_acc,
    COALESCE(assembly_version, 'Unknown') as assembly_version,
    total_length,
    created,
    updated,
    COALESCE(kingdom, 'Unknown') as kingdom,
    COALESCE(phylum, 'Unknown') as phylum,
    COALESCE(class, 'Unknown') as class,
    COALESCE("order", 'Unknown') as order_name,
    COALESCE(family, 'Unknown') as family,
    COALESCE(genus, 'Unknown') as genus,
    COALESCE(species, 'Unknown') as species,
    COALESCE(assembly_level, 'Unknown') as assembly_level,
    COALESCE(assembly_name, 'Unknown') as assembly_name
FROM source 