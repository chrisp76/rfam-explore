{{ config(materialized='view') }}

select
    genome_acc,
    rfam_acc,
    description,
    created
from genome 