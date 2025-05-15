WITH source AS (
    SELECT * FROM family
)

SELECT
    rfam_acc,
    rfam_id,
    auto_wiki,
    COALESCE(description, 'No description') as description,
    COALESCE(author, 'Unknown') as author,
    COALESCE(seed_source, 'Unknown') as seed_source,
    gathering_cutoff,
    trusted_cutoff,
    noise_cutoff,
    cmbuild,
    cmcalibrate,
    cmsearch,
    num_seed,
    num_full,
    num_genome_seq,
    num_refseq,
    type,
    structure_source,
    number_of_species,
    tax_seed,
    ecmli_lambda,
    ecmli_mu,
    ecmli_cal_db,
    ecmli_cal_hits,
    maxl,
    clen,
    match_pair_node,
    hmm_tau,
    hmm_lambda
FROM source 