WITH genome_rna_stats AS (
    SELECT
        g.upid,
        g.assembly_acc,
        g.kingdom,
        g.scientific_name,
        g.common_name,
        g.num_rfam_regions,
        g.num_families,
        COUNT(DISTINCT f.rfam_acc) as unique_rna_families,
        COUNT(DISTINCT f.type) as unique_rna_types,
        SUM(f.num_genome_seq) as total_rna_sequences
    FROM {{ ref('stg_genome') }} g
    LEFT JOIN {{ ref('stg_family') }} f ON g.upid = f.rfam_id  -- Adjusted join condition
    GROUP BY 1, 2, 3, 4, 5, 6, 7
)

SELECT
    upid,
    assembly_acc,
    kingdom,
    scientific_name,
    common_name,
    num_rfam_regions,
    num_families,
    unique_rna_families,
    unique_rna_types,
    total_rna_sequences,
    CASE 
        WHEN unique_rna_families > 100 THEN 'High'
        WHEN unique_rna_families > 50 THEN 'Medium'
        ELSE 'Low'
    END as rna_diversity_level,
    ROUND(unique_rna_families::FLOAT / NULLIF(unique_rna_types, 0), 2) as families_per_type_ratio
FROM genome_rna_stats 