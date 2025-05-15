{{ config(materialized='table') }}

with family_genome_counts as (
    select
        f.rfam_acc,
        f.rfam_id,
        f.description as family_description,
        f.type as rna_type,
        count(distinct g.genome_acc) as genome_count,
        min(g.created) as first_appearance,
        max(g.created) as last_appearance
    from {{ ref('stg_family') }} f
    left join {{ ref('stg_genome') }} g on f.rfam_acc = g.rfam_acc
    group by 1, 2, 3, 4
)

select
    *,
    case 
        when genome_count = 0 then 'Not Found'
        when genome_count < 10 then 'Rare'
        when genome_count < 100 then 'Common'
        else 'Widespread'
    end as prevalence_category
from family_genome_counts
order by genome_count desc 