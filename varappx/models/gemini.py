# coding: utf-8

from varappx.handle_init import *

class GeneDetailed(db.Model):
    __tablename__ = 'gene_detailed'
    __table_args__ = (
        db.Index('gendet_chrom_gene_idx', 'chrom', 'gene'),
    )

    uid = db.Column(db.Integer, primary_key=True)
    chrom = db.Column(db.String(60))
    gene = db.Column(db.String(60))
    is_hgnc = db.Column(db.Boolean)
    ensembl_gene_id = db.Column(db.Text)
    transcript = db.Column(db.String(60), index=True)
    biotype = db.Column(db.Text)
    transcript_status = db.Column(db.Text)
    ccds_id = db.Column(db.String(60), index=True)
    hgnc_id = db.Column(db.Text)
    entrez_id = db.Column(db.Text)
    cds_length = db.Column(db.Text)
    protein_length = db.Column(db.Text)
    transcript_start = db.Column(db.Text)
    transcript_end = db.Column(db.Text)
    strand = db.Column(db.Text)
    synonym = db.Column(db.Text)
    rvis_pct = db.Column(db.Float, index=True)
    mam_phenotype_id = db.Column(db.Text)


class GeneSummary(db.Model):
    __tablename__ = 'gene_summary'
    __table_args__ = (
        db.Index('gensum_chrom_gene_idx', 'chrom', 'gene'),
    )

    uid = db.Column(db.Integer, primary_key=True)
    chrom = db.Column(db.String(60))
    gene = db.Column(db.String(60))
    is_hgnc = db.Column(db.Boolean)
    ensembl_gene_id = db.Column(db.Text)
    hgnc_id = db.Column(db.Text)
    transcript_min_start = db.Column(db.Integer)
    transcript_max_end = db.Column(db.Integer)
    strand = db.Column(db.Text)
    synonym = db.Column(db.Text)
    rvis_pct = db.Column(db.Float, index=True)
    mam_phenotype_id = db.Column(db.Text)
    in_cosmic_census = db.Column(db.Boolean)

class Resources(db.Model):
    __tablename__ = 'resources'
    rid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    resource = db.Column(db.Text)


class SampleGenotypeCount(db.Model):
    __tablename__ = 'sample_genotype_counts'

    sample_id = db.Column(db.Integer, primary_key=True)
    num_hom_ref = db.Column(db.Integer)
    num_het = db.Column(db.Integer)
    num_hom_alt = db.Column(db.Integer)
    num_unknown = db.Column(db.Integer)


class SampleGenotype(db.Model):
    __tablename__ = 'sample_genotypes'

    sample_id = db.Column(db.Integer, primary_key=True)
    gt_types = db.Column(db.LargeBinary)

class Samples(db.Model):
    __tablename__ = 'samples'
    __table_args__ = (
        db.Index('sample_family_id', 'sample_id', 'family_id'),
    )
    sample_id = db.Column(db.Integer,primary_key=True)
    family_id = db.Column(db.Text,primary_key=True)
    name = db.Column(db.Text, unique=True)
    paternal_id = db.Column(db.Text)
    maternal_id = db.Column(db.Text)
    sex = db.Column(db.Text)
    phenotype = db.Column(db.Text)

# class
#
# t_variant_impacts = Table(
#     'variant_impacts', metadata,
#     db.Column('variant_id', db.Integer),
#     db.Column('anno_id', db.Integer),
#     db.Column('gene', db.String(60), index=True),
#     db.Column('transcript', db.String(60), index=True),
#     db.Column('is_exonic', db.Boolean, index=True),
#     db.Column('is_coding', db.Boolean, index=True),
#     db.Column('is_lof', db.Boolean, index=True),
#     db.Column('exon', db.Text),
#     db.Column('codon_change', db.Text),
#     db.Column('aa_change', db.Text),
#     db.Column('aa_length', db.Text),
#     db.Column('biotype', db.Text),
#     db.Column('impact', db.String(60), index=True),
#     db.Column('impact_so', db.Text),
#     db.Column('impact_severity', db.String(20)),
#     db.Column('polyphen_pred', db.Text),
#     db.Column('polyphen_score', db.Float),
#     db.Column('sift_pred', db.Text),
#     db.Column('sift_score', db.Float),
#     db.Column('vep_allele', db.Text),
#     db.Column('vep_impact', db.Text),
#     db.Column('vep_feature_type', db.Text),
#     db.Column('vep_intron', db.Text),
#     db.Column('vep_hgvsc', db.Text),
#     db.Column('vep_hgvsp', db.Text),
#     db.Column('vep_cdna_position', db.Text),
#     db.Column('vep_cds_position', db.Text),
#     db.Column('vep_existing_variation', db.Text),
#     db.Column('vep_distance', db.Text),
#     db.Column('vep_strand', db.Text),
#     db.Column('vep_flags', db.Text),
#     db.Column('vep_variant_class', db.Text),
#     db.Column('vep_symbol_source', db.Text),
#     db.Column('vep_hgnc_id', db.Text),
#     db.Column('vep_canonical', db.Text),
#     db.Column('vep_tsl', db.Text),
#     db.Column('vep_ccds', db.Text),
#     db.Column('vep_ensp', db.Text),
#     db.Column('vep_swissprot', db.Text),
#     db.Column('vep_trembl', db.Text),
#     db.Column('vep_uniparc', db.Text),
#     db.Column('vep_refseq_match', db.Text),
#     db.Column('vep_gene_pheno', db.Text),
#     db.Column('vep_domains', db.Text),
#     db.Column('vep_hgvs_offset', db.Text),
#     db.Column('vep_motif_name', db.Text),
#     db.Column('vep_motif_pos', db.Text),
#     db.Column('vep_high_inf_pos', db.Text),
#     db.Column('vep_motif_score_change', db.Text)
# )


class Variants(db.Model):
    __tablename__ = 'variants'
    __table_args__ = (
        db.Index('var_gt_counts_idx', 'num_hom_ref', 'num_het', 'num_hom_alt', 'num_unknown'),
        db.Index('var_chr_start_idx', 'chrom', 'start'),
        db.Index('chrom_varid_idx', 'chrom', 'variant_id')
    )

    chrom = db.Column(db.String(20))
    start = db.Column(db.Integer)
    end = db.Column(db.Integer)
    vcf_id = db.Column(db.Text)
    variant_id = db.Column(db.Integer, primary_key=True)
    anno_id = db.Column(db.Integer)
    ref = db.Column(db.Text)
    alt = db.Column(db.Text)
    qual = db.Column(db.Float, index=True)
    filter = db.Column(db.Text)
    type = db.Column(db.String(20), index=True)
    # sub_type = db.Column(db.Text)
    gts = db.Column(db.LargeBinary)
    gt_types = db.Column(db.LargeBinary)
    # gt_phases = db.Column(db.LargeBinary)
    gt_depths = db.Column(db.LargeBinary)
    # gt_ref_depths = db.Column(db.LargeBinary)
    # gt_alt_depths = db.Column(db.LargeBinary)
    # gt_quals = db.Column(db.LargeBinary)
    # gt_copy_numbers = db.Column(db.LargeBinary)
    # gt_phred_ll_homref = db.Column(db.LargeBinary)
    # gt_phred_ll_het = db.Column(db.LargeBinary)
    # gt_phred_ll_homalt = db.Column(db.LargeBinary)
    call_rate = db.Column(db.Float, index=True)

    in_dbsnp = db.Column(db.Boolean, index=True)
    rs_ids = db.Column(db.Text)
    # sv_cipos_start_left = db.Column(db.Integer)
    # sv_cipos_end_left = db.Column(db.Integer)
    # sv_cipos_start_right = db.Column(db.Integer)
    # sv_cipos_end_right = db.Column(db.Integer)
    # sv_length = db.Column(db.Integer)
    # sv_is_precise = db.Column(db.Boolean)
    # sv_tool = db.Column(db.Text)
    # sv_evidence_type = db.Column(db.Text)
    # sv_event_id = db.Column(db.Text)
    # sv_mate_id = db.Column(db.Text)
    # sv_strand = db.Column(db.Text)
    in_omim = db.Column(db.Boolean, index=True)
    clinvar_sig = db.Column(db.Text)
    clinvar_disease_name = db.Column(db.Text)
    clinvar_dbsource = db.Column(db.Text)
    clinvar_dbsource_id = db.Column(db.Text)
    clinvar_origin = db.Column(db.Text)
    clinvar_dsdb = db.Column(db.Text)
    clinvar_dsdbid = db.Column(db.Text)
    clinvar_disease_acc = db.Column(db.Text)
    clinvar_in_locus_spec_db = db.Column(db.Boolean)
    clinvar_on_diag_assay = db.Column(db.Boolean)
    clinvar_causal_allele = db.Column(db.Text)
    clinvar_gene_phenotype = db.Column(db.Text)
    geno2mp_hpo_ct = db.Column(db.Integer)
    pfam_domain = db.Column(db.Text)
    cyto_band = db.Column(db.Text)
    rmsk = db.Column(db.Text)
    in_cpg_island = db.Column(db.Boolean)
    in_segdup = db.Column(db.Boolean)
    is_conserved = db.Column(db.Boolean)
    gerp_bp_score = db.Column(db.Float)
    gerp_element_pval = db.Column(db.Float)
    num_hom_ref = db.Column(db.Integer, index=True)
    num_het = db.Column(db.Integer, index=True)
    num_hom_alt = db.Column(db.Integer, index=True)
    num_unknown = db.Column(db.Integer, index=True)
    aaf = db.Column(db.Float, index=True)
    hwe = db.Column(db.Float)
    inbreeding_coeff = db.Column(db.Float)
    pi = db.Column(db.Float)
    recomb_rate = db.Column(db.Float)
    gene = db.Column(db.String(60), index=True)
    transcript = db.Column(db.String(60), index=True)
    is_exonic = db.Column(db.Boolean, index=True)
    is_coding = db.Column(db.Boolean, index=True)
    is_splicing = db.Column(db.Boolean)
    is_lof = db.Column(db.Boolean, index=True)
    exon = db.Column(db.Text)
    codon_change = db.Column(db.Text)
    aa_change = db.Column(db.Text)
    aa_length = db.Column(db.Text)
    biotype = db.Column(db.Text)
    impact = db.Column(db.String(60), index=True)
    impact_so = db.Column(db.Text)
    impact_severity = db.Column(db.String(20), index=True)
    polyphen_pred = db.Column(db.Text)
    polyphen_score = db.Column(db.Float)
    sift_pred = db.Column(db.Text)
    sift_score = db.Column(db.Float)
    anc_allele = db.Column(db.Text)
    rms_bq = db.Column(db.Float)
    cigar = db.Column(db.Text)
    depth = db.Column(db.Integer, index=True)
    strand_bias = db.Column(db.Float)
    rms_map_qual = db.Column(db.Float)
    in_hom_run = db.Column(db.Integer)
    num_mapq_zero = db.Column(db.Integer)
    num_alleles = db.Column(db.Integer)
    num_reads_w_dels = db.Column(db.Float)
    haplotype_score = db.Column(db.Float)
    qual_depth = db.Column(db.Float)
    allele_count = db.Column(db.Integer)
    allele_bal = db.Column(db.Float)
    in_hm2 = db.Column(db.Boolean)
    in_hm3 = db.Column(db.Boolean)
    is_somatic = db.Column(db.Boolean, index=True)
    somatic_score = db.Column(db.Float)
    in_esp = db.Column(db.Boolean)
    # aaf_esp_ea = db.Column(db.Float)
    # aaf_esp_aa = db.Column(db.Float)
    #
    exome_chip = db.Column(db.Boolean)
    in_1kg = db.Column(db.Boolean)
    # aaf_1kg_amr = db.Column(db.Float)
    # aaf_1kg_eas = db.Column(db.Float)
    # aaf_1kg_sas = db.Column(db.Float)
    # aaf_1kg_afr = db.Column(db.Float)
    # aaf_1kg_eur = db.Column(db.Float)

    aaf_exac_all = db.Column(db.Float)
    aaf_esp_all = db.Column(db.Float, index=True)
    aaf_1kg_all = db.Column(db.Float, index=True)
    max_aaf_all = db.Column(db.Float, index=True)

    grc = db.Column(db.Text)
    gms_illumina = db.Column(db.Float)
    # gms_solid = db.Column(db.Float)
    # gms_iontorrent = db.Column(db.Float)
    # in_cse = db.Column(db.Boolean)
    # encode_tfbs = db.Column(db.Text)
    # encode_dnaseI_cell_count = db.Column(db.Integer)
    # encode_dnaseI_cell_list = db.Column(db.Text)
    # encode_consensus_gm12878 = db.Column(db.Text)
    # encode_consensus_h1hesc = db.Column(db.Text)
    # encode_consensus_helas3 = db.Column(db.Text)
    # encode_consensus_hepg2 = db.Column(db.Text)
    # encode_consensus_huvec = db.Column(db.Text)
    # encode_consensus_k562 = db.Column(db.Text)
    vista_enhancers = db.Column(db.Text)
    cosmic_ids = db.Column(db.Text)
    info = db.Column(db.LargeBinary)
    cadd_raw = db.Column(db.Float, index=True)
    cadd_scaled = db.Column(db.Float, index=True)
    fitcons = db.Column(db.Float, index=True)
    in_exac = db.Column(db.Boolean)

    # aaf_adj_exac_all = db.Column(db.Float)
    # aaf_adj_exac_afr = db.Column(db.Float)
    # aaf_adj_exac_amr = db.Column(db.Float)
    # aaf_adj_exac_eas = db.Column(db.Float)
    # aaf_adj_exac_fin = db.Column(db.Float)
    # aaf_adj_exac_nfe = db.Column(db.Float)
    # aaf_adj_exac_oth = db.Column(db.Float)
    # aaf_adj_exac_sas = db.Column(db.Float)
    # exac_num_het = db.Column(db.Integer)
    # exac_num_hom_alt = db.Column(db.Integer)
    # exac_num_chroms = db.Column(db.Integer)
    # aaf_gnomad_all = db.Column(db.Float)
    # aaf_gnomad_afr = db.Column(db.Float)
    # aaf_gnomad_amr = db.Column(db.Float)
    # aaf_gnomad_asj = db.Column(db.Float)
    # aaf_gnomad_eas = db.Column(db.Float)
    # aaf_gnomad_fin = db.Column(db.Float)
    # aaf_gnomad_nfe = db.Column(db.Float)
    # aaf_gnomad_oth = db.Column(db.Float)
    # aaf_gnomad_sas = db.Column(db.Float)
    gnomad_num_het = db.Column(db.Integer)
    gnomad_num_hom_alt = db.Column(db.Integer)
    gnomad_num_chroms = db.Column(db.Integer)
    # vep_allele = db.Column(db.Text)
    # vep_impact = db.Column(db.Text)
    # vep_feature_type = db.Column(db.Text)
    # vep_intron = db.Column(db.Text)
    vep_hgvsc = db.Column(db.Text)
    vep_hgvsp = db.Column(db.Text)
    # vep_cdna_position = db.Column(db.Text)
    # vep_cds_position = db.Column(db.Text)
    # vep_existing_variation = db.Column(db.Text)
    # vep_distance = db.Column(db.Text)
    # vep_strand = db.Column(db.Text)
    # vep_flags = db.Column(db.Text)
    # vep_variant_class = db.Column(db.Text)
    # vep_symbol_source = db.Column(db.Text)
    # vep_hgnc_id = db.Column(db.Text)
    # vep_canonical = db.Column(db.Text)
    # vep_tsl = db.Column(db.Text)
    # vep_ccds = db.Column(db.Text)
    # vep_ensp = db.Column(db.Text)
    # vep_swissprot = db.Column(db.Text)
    # vep_trembl = db.Column(db.Text)
    # vep_uniparc = db.Column(db.Text)
    # vep_refseq_match = db.Column(db.Text)
    # vep_gene_pheno = db.Column(db.Text)
    # vep_domains = db.Column(db.Text)
    # vep_hgvs_offset = db.Column(db.Text)
    # vep_motif_name = db.Column(db.Text)
    # vep_motif_pos = db.Column(db.Text)
    # vep_high_inf_pos = db.Column(db.Text)
    # vep_motif_score_change = db.Column(db.Text)

    #PoS = db.Column(db.Integer, index=True, server_default=db.text("NULL"))
    allele_depths_raws = db.Column('SAD',db.Text, index=True, server_default=db.text("NULL"))
    allele_freq_raws = db.Column('SAF',db.Text, index=True,server_default=db.text("NULL"))
    allele_freq = db.Column('AF',db.Text, index=True, server_default=db.text("NULL"))
    base_qual_rank_sum = db.Column('BaseQRankSum',db.Float, index=True, server_default=db.text("NULL"))
    fisher_strand_bias = db.Column('FS',db.Float, index=True, server_default=db.text("NULL"))
    map_qual_rank_sum = db.Column('MQRankSum',db.Float, index=True, server_default=db.text("NULL"))
    read_pos_rank_sum = db.Column('ReadPosRankSum',db.Float, index=True, server_default=db.text("NULL"))
    strand_bias_odds_ratio = db.Column('SOR',db.Float, index=True, server_default=db.text("NULL"))
    allele_depths = db.Column('AD',db.Text, index=True, server_default=db.text("NULL"))

class VcfHeader(db.Model):
    __tablename__ = 'vcf_header'
    vcfhid = db.Column(db.Integer, primary_key=True)
    vcf_header = db.Column(db.Text)

class Version(db.Model):
    __tablename__ = 'version'
    vid = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.Text)
