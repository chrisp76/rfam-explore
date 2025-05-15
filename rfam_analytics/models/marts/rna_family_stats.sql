WITH family_stats AS (
    SELECT
        f.rfam_acc,
        f.rfam_id,
        f.description,
        f.type,
        f.num_genome_seq,
        f.number_of_species,
        COUNT(DISTINCT g.upid) as genome_count,
        COUNT(DISTINCT g.kingdom) as kingdom_count
    FROM {{ ref('stg_family') }} f
    LEFT JOIN {{ ref('stg_genome') }} g ON f.rfam_id = g.upid  -- Adjusted join condition
    GROUP BY 1, 2, 3, 4, 5, 6
)

SELECT
    rfam_acc,
    rfam_id,
    description,
    type,
    num_genome_seq,
    number_of_species,
    genome_count,
    kingdom_count,
    CASE 
        WHEN genome_count = 0 THEN 0
        ELSE ROUND(number_of_species::FLOAT / genome_count, 2)
    END as species_per_genome_ratio,
    CASE 
        WHEN kingdom_count > 3 THEN 'Widespread'
        WHEN kingdom_count > 1 THEN 'Moderate'
        ELSE 'Limited'
    END as distribution_category
FROM family_stats 