{{ config(materialized='view') }}

select
    rfam_acc,
    rfam_id,
    description,
    author,
    seed_source,
    gathering_cutoff,
    trusted_cutoff,
    noise_cutoff,
    comment,
    type,
    updated
from family 