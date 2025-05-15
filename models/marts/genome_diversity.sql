{{ config(materialized='table') }}

with genome_rna_counts as (
    select
        g.genome_acc,
        g.description as genome_description,
        count(distinct g.rfam_acc) as unique_rna_families,
        count(distinct f.type) as unique_rna_types
    from {{ ref('stg_genome') }} g
    left join {{ ref('stg_family') }} f on g.rfam_acc = f.rfam_acc
    group by 1, 2
)

select
    *,
    case 
        when unique_rna_families < 5 then 'Low'
        when unique_rna_families < 20 then 'Medium'
        else 'High'
    end as rna_diversity_level
from genome_rna_counts
order by unique_rna_families desc 