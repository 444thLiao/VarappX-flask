# coding: utf-8
from sqlalchemy import Boolean, Column, Float, Index, Integer, LargeBinary, String, Table, Text, text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class GeneDetailed(Base):
    __tablename__ = 'gene_detailed'
    __table_args__ = (
        Index('gendet_chrom_gene_idx', 'chrom', 'gene'),
    )

    uid = Column(Integer, primary_key=True)
    chrom = Column(String(60))
    gene = Column(String(60))
    is_hgnc = Column(Boolean)
    ensembl_gene_id = Column(Text)
    transcript = Column(String(60), index=True)
    biotype = Column(Text)
    transcript_status = Column(Text)
    ccds_id = Column(String(60), index=True)
    hgnc_id = Column(Text)
    entrez_id = Column(Text)
    cds_length = Column(Text)
    protein_length = Column(Text)
    transcript_start = Column(Text)
    transcript_end = Column(Text)
    strand = Column(Text)
    synonym = Column(Text)
    rvis_pct = Column(Float, index=True)
    mam_phenotype_id = Column(Text)


class GeneSummary(Base):
    __tablename__ = 'gene_summary'
    __table_args__ = (
        Index('gensum_chrom_gene_idx', 'chrom', 'gene'),
    )

    uid = Column(Integer, primary_key=True)
    chrom = Column(String(60))
    gene = Column(String(60))
    is_hgnc = Column(Boolean)
    ensembl_gene_id = Column(Text)
    hgnc_id = Column(Text)
    transcript_min_start = Column(Integer)
    transcript_max_end = Column(Integer)
    strand = Column(Text)
    synonym = Column(Text)
    rvis_pct = Column(Float, index=True)
    mam_phenotype_id = Column(Text)
    in_cosmic_census = Column(Boolean)


t_resources = Table(
    'resources', metadata,
    Column('name', Text),
    Column('resource', Text)
)


class SampleGenotypeCount(Base):
    __tablename__ = 'sample_genotype_counts'

    sample_id = Column(Integer, primary_key=True)
    num_hom_ref = Column(Integer)
    num_het = Column(Integer)
    num_hom_alt = Column(Integer)
    num_unknown = Column(Integer)


class SampleGenotype(Base):
    __tablename__ = 'sample_genotypes'

    sample_id = Column(Integer, primary_key=True)
    gt_types = Column(LargeBinary)


t_samples = Table(
    'samples', metadata,
    Column('sample_id', Integer),
    Column('family_id', Text),
    Column('name', Text, unique=True),
    Column('paternal_id', Text),
    Column('maternal_id', Text),
    Column('sex', Text),
    Column('phenotype', Text)
)


t_variant_impacts = Table(
    'variant_impacts', metadata,
    Column('variant_id', Integer),
    Column('anno_id', Integer),
    Column('gene', String(60), index=True),
    Column('transcript', String(60), index=True),
    Column('is_exonic', Boolean, index=True),
    Column('is_coding', Boolean, index=True),
    Column('is_lof', Boolean, index=True),
    Column('exon', Text),
    Column('codon_change', Text),
    Column('aa_change', Text),
    Column('aa_length', Text),
    Column('biotype', Text),
    Column('impact', String(60), index=True),
    Column('impact_so', Text),
    Column('impact_severity', String(20)),
    Column('polyphen_pred', Text),
    Column('polyphen_score', Float),
    Column('sift_pred', Text),
    Column('sift_score', Float),
    Column('vep_allele', Text),
    Column('vep_impact', Text),
    Column('vep_feature_type', Text),
    Column('vep_intron', Text),
    Column('vep_hgvsc', Text),
    Column('vep_hgvsp', Text),
    Column('vep_cdna_position', Text),
    Column('vep_cds_position', Text),
    Column('vep_existing_variation', Text),
    Column('vep_distance', Text),
    Column('vep_strand', Text),
    Column('vep_flags', Text),
    Column('vep_variant_class', Text),
    Column('vep_symbol_source', Text),
    Column('vep_hgnc_id', Text),
    Column('vep_canonical', Text),
    Column('vep_tsl', Text),
    Column('vep_ccds', Text),
    Column('vep_ensp', Text),
    Column('vep_swissprot', Text),
    Column('vep_trembl', Text),
    Column('vep_uniparc', Text),
    Column('vep_refseq_match', Text),
    Column('vep_gene_pheno', Text),
    Column('vep_domains', Text),
    Column('vep_hgvs_offset', Text),
    Column('vep_motif_name', Text),
    Column('vep_motif_pos', Text),
    Column('vep_high_inf_pos', Text),
    Column('vep_motif_score_change', Text)
)


class Variant(Base):
    __tablename__ = 'variants'
    __table_args__ = (
        Index('var_gt_counts_idx', 'num_hom_ref', 'num_het', 'num_hom_alt', 'num_unknown'),
        Index('var_chr_start_idx', 'chrom', 'start'),
        Index('chrom_varid_idx', 'chrom', 'variant_id')
    )

    chrom = Column(String(20))
    start = Column(Integer)
    end = Column(Integer)
    vcf_id = Column(Text)
    variant_id = Column(Integer, primary_key=True)
    anno_id = Column(Integer)
    ref = Column(Text)
    alt = Column(Text)
    qual = Column(Float, index=True)
    filter = Column(Text)
    type = Column(String(20), index=True)
    sub_type = Column(Text)
    gts = Column(LargeBinary)
    gt_types = Column(LargeBinary)
    gt_phases = Column(LargeBinary)
    gt_depths = Column(LargeBinary)
    gt_ref_depths = Column(LargeBinary)
    gt_alt_depths = Column(LargeBinary)
    gt_quals = Column(LargeBinary)
    gt_copy_numbers = Column(LargeBinary)
    gt_phred_ll_homref = Column(LargeBinary)
    gt_phred_ll_het = Column(LargeBinary)
    gt_phred_ll_homalt = Column(LargeBinary)
    call_rate = Column(Float, index=True)
    max_aaf_all = Column(Float, index=True)
    in_dbsnp = Column(Boolean, index=True)
    rs_ids = Column(Text)
    sv_cipos_start_left = Column(Integer)
    sv_cipos_end_left = Column(Integer)
    sv_cipos_start_right = Column(Integer)
    sv_cipos_end_right = Column(Integer)
    sv_length = Column(Integer)
    sv_is_precise = Column(Boolean)
    sv_tool = Column(Text)
    sv_evidence_type = Column(Text)
    sv_event_id = Column(Text)
    sv_mate_id = Column(Text)
    sv_strand = Column(Text)
    in_omim = Column(Boolean, index=True)
    clinvar_sig = Column(Text)
    clinvar_disease_name = Column(Text)
    clinvar_dbsource = Column(Text)
    clinvar_dbsource_id = Column(Text)
    clinvar_origin = Column(Text)
    clinvar_dsdb = Column(Text)
    clinvar_dsdbid = Column(Text)
    clinvar_disease_acc = Column(Text)
    clinvar_in_locus_spec_db = Column(Boolean)
    clinvar_on_diag_assay = Column(Boolean)
    clinvar_causal_allele = Column(Text)
    clinvar_gene_phenotype = Column(Text)
    geno2mp_hpo_ct = Column(Integer)
    pfam_domain = Column(Text)
    cyto_band = Column(Text)
    rmsk = Column(Text)
    in_cpg_island = Column(Boolean)
    in_segdup = Column(Boolean)
    is_conserved = Column(Boolean)
    gerp_bp_score = Column(Float)
    gerp_element_pval = Column(Float)
    num_hom_ref = Column(Integer, index=True)
    num_het = Column(Integer, index=True)
    num_hom_alt = Column(Integer, index=True)
    num_unknown = Column(Integer, index=True)
    aaf = Column(Float, index=True)
    hwe = Column(Float)
    inbreeding_coeff = Column(Float)
    pi = Column(Float)
    recomb_rate = Column(Float)
    gene = Column(String(60), index=True)
    transcript = Column(String(60), index=True)
    is_exonic = Column(Boolean, index=True)
    is_coding = Column(Boolean, index=True)
    is_splicing = Column(Boolean)
    is_lof = Column(Boolean, index=True)
    exon = Column(Text)
    codon_change = Column(Text)
    aa_change = Column(Text)
    aa_length = Column(Text)
    biotype = Column(Text)
    impact = Column(String(60), index=True)
    impact_so = Column(Text)
    impact_severity = Column(String(20), index=True)
    polyphen_pred = Column(Text)
    polyphen_score = Column(Float)
    sift_pred = Column(Text)
    sift_score = Column(Float)
    anc_allele = Column(Text)
    rms_bq = Column(Float)
    cigar = Column(Text)
    depth = Column(Integer, index=True)
    strand_bias = Column(Float)
    rms_map_qual = Column(Float)
    in_hom_run = Column(Integer)
    num_mapq_zero = Column(Integer)
    num_alleles = Column(Integer)
    num_reads_w_dels = Column(Float)
    haplotype_score = Column(Float)
    qual_depth = Column(Float)
    allele_count = Column(Integer)
    allele_bal = Column(Float)
    in_hm2 = Column(Boolean)
    in_hm3 = Column(Boolean)
    is_somatic = Column(Boolean, index=True)
    somatic_score = Column(Float)
    in_esp = Column(Boolean)
    aaf_esp_ea = Column(Float)
    aaf_esp_aa = Column(Float)
    aaf_esp_all = Column(Float, index=True)
    exome_chip = Column(Boolean)
    in_1kg = Column(Boolean)
    aaf_1kg_amr = Column(Float)
    aaf_1kg_eas = Column(Float)
    aaf_1kg_sas = Column(Float)
    aaf_1kg_afr = Column(Float)
    aaf_1kg_eur = Column(Float)
    aaf_1kg_all = Column(Float, index=True)
    grc = Column(Text)
    gms_illumina = Column(Float)
    gms_solid = Column(Float)
    gms_iontorrent = Column(Float)
    in_cse = Column(Boolean)
    encode_tfbs = Column(Text)
    encode_dnaseI_cell_count = Column(Integer)
    encode_dnaseI_cell_list = Column(Text)
    encode_consensus_gm12878 = Column(Text)
    encode_consensus_h1hesc = Column(Text)
    encode_consensus_helas3 = Column(Text)
    encode_consensus_hepg2 = Column(Text)
    encode_consensus_huvec = Column(Text)
    encode_consensus_k562 = Column(Text)
    vista_enhancers = Column(Text)
    cosmic_ids = Column(Text)
    info = Column(LargeBinary)
    cadd_raw = Column(Float, index=True)
    cadd_scaled = Column(Float, index=True)
    fitcons = Column(Float, index=True)
    in_exac = Column(Boolean)
    aaf_exac_all = Column(Float)
    aaf_adj_exac_all = Column(Float)
    aaf_adj_exac_afr = Column(Float)
    aaf_adj_exac_amr = Column(Float)
    aaf_adj_exac_eas = Column(Float)
    aaf_adj_exac_fin = Column(Float)
    aaf_adj_exac_nfe = Column(Float)
    aaf_adj_exac_oth = Column(Float)
    aaf_adj_exac_sas = Column(Float)
    exac_num_het = Column(Integer)
    exac_num_hom_alt = Column(Integer)
    exac_num_chroms = Column(Integer)
    aaf_gnomad_all = Column(Float)
    aaf_gnomad_afr = Column(Float)
    aaf_gnomad_amr = Column(Float)
    aaf_gnomad_asj = Column(Float)
    aaf_gnomad_eas = Column(Float)
    aaf_gnomad_fin = Column(Float)
    aaf_gnomad_nfe = Column(Float)
    aaf_gnomad_oth = Column(Float)
    aaf_gnomad_sas = Column(Float)
    gnomad_num_het = Column(Integer)
    gnomad_num_hom_alt = Column(Integer)
    gnomad_num_chroms = Column(Integer)
    vep_allele = Column(Text)
    vep_impact = Column(Text)
    vep_feature_type = Column(Text)
    vep_intron = Column(Text)
    vep_hgvsc = Column(Text)
    vep_hgvsp = Column(Text)
    vep_cdna_position = Column(Text)
    vep_cds_position = Column(Text)
    vep_existing_variation = Column(Text)
    vep_distance = Column(Text)
    vep_strand = Column(Text)
    vep_flags = Column(Text)
    vep_variant_class = Column(Text)
    vep_symbol_source = Column(Text)
    vep_hgnc_id = Column(Text)
    vep_canonical = Column(Text)
    vep_tsl = Column(Text)
    vep_ccds = Column(Text)
    vep_ensp = Column(Text)
    vep_swissprot = Column(Text)
    vep_trembl = Column(Text)
    vep_uniparc = Column(Text)
    vep_refseq_match = Column(Text)
    vep_gene_pheno = Column(Text)
    vep_domains = Column(Text)
    vep_hgvs_offset = Column(Text)
    vep_motif_name = Column(Text)
    vep_motif_pos = Column(Text)
    vep_high_inf_pos = Column(Text)
    vep_motif_score_change = Column(Text)
    PoS = Column(Integer, index=True, server_default=text("NULL"))
    SAD = Column(Text, index=True, server_default=text("NULL"))
    SAF = Column(Text, index=True, server_default=text("NULL"))
    AF = Column(Text, index=True, server_default=text("NULL"))
    BaseQRankSum = Column(Float, index=True, server_default=text("NULL"))
    FS = Column(Float, index=True, server_default=text("NULL"))
    MQRankSum = Column(Float, index=True, server_default=text("NULL"))
    ReadPosRankSum = Column(Float, index=True, server_default=text("NULL"))
    SOR = Column(Float, index=True, server_default=text("NULL"))
    AD = Column(Text, index=True, server_default=text("NULL"))


t_vcf_header = Table(
    'vcf_header', metadata,
    Column('vcf_header', Text)
)


t_version = Table(
    'version', metadata,
    Column('version', Text)
)