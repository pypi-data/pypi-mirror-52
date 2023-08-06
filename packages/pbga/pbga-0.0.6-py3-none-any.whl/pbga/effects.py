VARIANT_EFFECTS = (
    #
    # HIGH Putative Impact
    #
    #
    # change of feature structure or larger units
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:1000182">SO:1000182</a> A kind of
    # chromosome variation where the chromosome complement is not an exact multiple of the haploid number (is a
    # chromosome_variation).
    # 
    # <b>Not</b> used in Jannovar annotations.
    # 
    'CHROMOSOME_NUMBER_VARIATION',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001893">SO:0001893</a> A feature ablation
    # whereby the deleted region includes a transcript feature (is a: feature_ablation)
    # 
    'TRANSCRIPT_ABLATION',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001572">SO:0001572</a> A sequence variant
    # whereby an exon is lost from the transcript (is a (is a: {@link #SPLICING_VARIANT}), {@link #TRANSCRIPT_VARIANT}
    # ).
    # 
    'EXON_LOSS_VARIANT',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:1000036">SO:1000036</a> A continuous
    # nucleotide sequence is inverted in the same position.
    # 
    'INVERSION',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0000667">SO:0000667</a> The sequence of one
    # or more nucleotides added between two adjacent nucleotides in the sequence.
    # <p>
    # In Jannovar, used to annotate a structural variant insertion.
    # 
    'INSERTION',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0000199">SO:0000199</a> A region of
    # nucleotide sequence that has translocated to a new position. The observed adjacency of two previously separated
    # regions.
    # 
    'TRANSLOCATION',

    # high impact changes in the coding region
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001909">SO:0001909</a> A frameshift
    # variant that causes the translational reading frame to be extended relative to the reference feature (is a {@link
    # #FRAMESHIFT_VARIANT}, internal_feature_elongation).
    # 
    'FRAMESHIFT_ELONGATION',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001910">SO:0001910</a> A frameshift
    # variant that causes the translational reading frame to be shortened relative to the reference feature (is a
    # {@link #FRAMESHIFT_VARIANT}, internal_feature_truncation).
    # 
    'FRAMESHIFT_TRUNCATION',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001589">SO:0001589</a>A sequence variant
    # which causes a disruption of the translational reading frame, because the number of nucleotides inserted or
    # deleted is not a multiple of threee (is a: protein_altering_variant).
    # <p>
    # Used for frameshift variant for the case where there is no stop codon any more and the rare case in which the
    # transcript length is retained.
    # 
    'FRAMESHIFT_VARIANT',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001908">SO:0001908</a> A sequence variant
    # that causes the extension of a genomic feature from within the feature rather than from the terminus of the
    # feature, with regard to the reference sequence.
    # <p>
    # In Jannovar, used to annotate a {@link #COMPLEX_SUBSTITUTION} that does not lead to a frameshift and increases
    # the transcript length.
    # 
    'INTERNAL_FEATURE_ELONGATION',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001906">SO:0001906</a> A sequence variant
    # that causes the reduction of a genomic feature, with regard to the reference sequence (is a: feature_variant).
    # <p>
    # The term <a href="http://www.sequenceontology.org/browser/current_svn/term/INTERNAL_FEATURE_TRUNCATION">
    # INTERNAL_FEATURE_TRUNCATION</a> would be more fitting but is not available in SO.
    # <p>
    # In Jannovar, used to annotate a {@link #COMPLEX_SUBSTITUTION} that does not lead to a frameshift and decreases
    # the transcript length and structural variants.
    # 
    'FEATURE_TRUNCATION',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001880">SO:0001880</a> A feature
    # amplification of a region containing a transcript.
    # <p>
    # In Jannovar, used together with {@link #STRUCTURAL_VARIANT} to denote an SV copy number gain.
    # 
    'TRANSCRIPT_AMPLIFICATION',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001563">SO:0001563</a> A sequence variant
    # where copies of a feature (CNV) are either increased or decreased.
    # <p>
    # In Jannovar, used together with {@link #STRUCTURAL_VARIANT} to denote an SV copy number gain.
    # 
    'COPY_NUMBER_CHANGE',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0002007">SO:0002007</a> An MNV is a
    # multiple nucleotide variant (substitution) in which the inserted sequence is the same length as the replaced
    # sequence (is a: substitution).
    # <p>
    # In Jannovar, only used for marking MNVs in coding regions.
    # 
    'MNV',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:1000005">SO:1000005</a> When no simple or
    # well defined DNA mutation event describes the observed DNA change, the keyword "complex" should be used. Usually
    # there are multiple equally plausible explanations for the change (is a: substitution).
    # <p>
    # Used together with {@link #INTERNAL_FEATURE_ELONGATION} or {@link #FEATURE_TRUNCATION} to describe an variant
    # that does not lead to a frameshift but a changed transcript length. Used together with {@link
    # #FRAMESHIFT_ELONGATION} or {@link #FRAMESHIFT_TRUNCATION} if the substitution leads to a frameshift variant.
    # 
    'COMPLEX_SUBSTITUTION',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001587">SO:0001587</a> A sequence variant
    # whereby at least one base of a codon is changed, resulting in a premature stop codon, leading to a shortened
    # transcript (is a: nonsynonymous_variant, feature_truncation).
    # 
    'STOP_GAINED',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001578">SO:0001578</a> A sequence variant
    # where at least one base of the terminator codon (stop) is changed, resulting in an elongated transcript (is a:
    # nonsynonymous variant, terminator_codon_variant, feature_elongation)
    # 
    'STOP_LOST',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0002012">SO:0002012</a> A codon variant
    # that changes at least one base of the canonical start codon (is a: initiator_codon_variant).
    # 
    'START_LOST',

    # splicing changes, might change splicing
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001574">SO:0001574</a> A splice variant
    # that changes the 2 base region at the 3' end of an intron (is a {@link #SPLICE_REGION_VARIANT}).
    # 
    'SPLICE_ACCEPTOR_VARIANT',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001575">SO:0001575</a> A splice variant
    # that changes the 2 base pair region at the 5' end of an intron (is a {@link #SPLICE_REGION_VARIANT}).
    # 
    'SPLICE_DONOR_VARIANT',

    # change in rare amino acids, exotic variant
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0002008">SO:0002008</a> A sequence variant
    # whereby at least one base of a codon encoding a rare amino acid is changed, resulting in a different encoded
    # amino acid (children: selenocysteine_loss, pyrrolysine_loss).
    # 
    # <b>Not</b> used in Jannovar annotations.
    # 
    'RARE_AMINO_ACID_VARIANT',
    #
    # Marker for smallest {@link VariantEffect} with {@link PutativeImpact#HIGH} impact.
    # 
    # _SMALLEST_HIGH_IMPACT,

    #
    # MODERATE Putative Impact
    #
    #
    # moderate impact changes in coding region that
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001583">SO:0001583</a> A sequence variant,
    # that changes one or more bases, resulting in a different amino acid sequence but where the length is preserved.
    # 
    'MISSENSE_VARIANT',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001821">SO:0001821</a> An inframe non
    # synonymous variant that inserts bases into in the coding sequence (is a: inframe_indel,
    # internal_feature_elongation).
    # 
    'INFRAME_INSERTION',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001824">SO:0001824</a> An inframe increase
    # in cds length that inserts one or more codons into the coding sequence within an existing codon (is a: {@link
    # #INFRAME_INSERTION}).
    # 
    'DISRUPTIVE_INFRAME_INSERTION',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001822">SO:0001822</a> An inframe non
    # synonymous variant that deletes bases from the coding sequence (is a: inframe_indel, feature_truncation).
    # 
    'INFRAME_DELETION',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001826">SO:0001826</a> An inframe decrease
    # in cds length that deletes bases from the coding sequence starting within an existing codon (is a: {@link
    # #INFRAME_DELETION}).
    # 
    'DISRUPTIVE_INFRAME_DELETION',

    # changes in the UTR
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0002013">SO:0002013</a> A sequence variant
    # that causes the reduction of a the 5'UTR with regard to the reference sequence (is a: {@link
    # #FIVE_PRIME_UTR_EXON_VARIANT} or {@link #FIVE_PRIME_UTR_INTRON_VARIANT})
    # <p>
    # Jannovar does <b>not</b> yield use this at the moment.
    # 
    'FIVE_PRIME_UTR_TRUNCATION',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0002015">SO:0002015</a> A sequence variant
    # that causes the reduction of a the 3' UTR with regard to the reference sequence (is a: {@link
    # #FIVE_PRIME_UTR_EXON_VARIANT} or {@link #FIVE_PRIME_UTR_INTRON_VARIANT}).
    # <p>
    # Jannovar does <b>not</b> yield use this at the moment.
    # 
    'THREE_PRIME_UTR_TRUNCATION',

    #
    # Marker for smallest {@link VariantEffect} with {@link PutativeImpact#MODERATE} impact.
    # 
    # _SMALLEST_MODERATE_IMPACT,

    #
    # LOW Putative Impact
    #
    #
    # changes in the splicing region
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001630">SO:0001630</a> A sequence variant
    # in which a change has occurred within the region of the splice site, either within 1-3 bases of the exon or 3-8
    # bases of the intron (is a: {@link #SPLICING_VARIANT}).
    # 
    'SPLICE_REGION_VARIANT',

    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001567">SO:0001567</a> A sequence variant
    # where at least one base in the terminator codon is changed, but the terminator remains (is a: {@link
    # #SYNONYMOUS_VARIANT}, terminator_codon_variant).
    # 
    'STOP_RETAINED_VARIANT',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001582">SO:0001582</a> A codon variant
    # that changes at least one base of the first codon of a transcript (is a: {@link #CODING_SEQUENCE_VARIANT},
    # children: start_retained_variant, start_lost).
    # 
    'INITIATOR_CODON_VARIANT',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001819">SO:0001819</a> A sequence variant
    # where there is no resulting change to the encoded amino acid (is a: {@link #CODING_SEQUENCE_VARIANT}, children:
    # start_retained_variant, stop_retained_variant).
    # 
    'SYNONYMOUS_VARIANT',

    # changes in coding transcripts, exons/introns
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001969">SO:0001969</a> A sequence variant
    # that changes non-coding intro sequence in a non-coding transcript (is a: {@link #CODING_TRANSCRIPT_VARIANT},
    # {@link #INTRON_VARIANT}).
    # 
    'CODING_TRANSCRIPT_INTRON_VARIANT',

    # UTR variant
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001983">SO:0001983</a> A 5' UTR variant
    # where a premature start codon is introduced, moved or lost (is a: {@link #FIVE_PRIME_UTR_EXON_VARIANT} or {@link
    # #FIVE_PRIME_UTR_INTRON_VARIANT}).
    # 
    # <b>Not</b> used in Jannovar annotations.
    # 
    # TODO(holtgrem): use
    'FIVE_PRIME_UTR_PREMATURE_START_CODON_GAIN_VARIANT',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0002092">SO:0002092</a> A UTR variant of
    # the 5' UTR (is a: 5_prime_UTR_variant; is a: UTR_variant).
    # 
    'FIVE_PRIME_UTR_EXON_VARIANT',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0002089">SO:0002089</a> A UTR variant of
    # the 3' UTR (is a: 3_prime_UTR_variant; is a: UTR_variant).
    # 
    'THREE_PRIME_UTR_EXON_VARIANT',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0002091">SO:0002091</a> A UTR variant
    # between 5' UTRs (is a: 5_prime_UTR_variant; is a: UTR_variant).
    # 
    'FIVE_PRIME_UTR_INTRON_VARIANT',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0002090">SO:0002090</a> A UTR variant
    # between 3' UTRs (is a: 3_prime_UTR_variant; is a: UTR_variant).
    # 
    'THREE_PRIME_UTR_INTRON_VARIANT',

    # changes in non-coding transcripts, exons/introns
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001792">SO:0001792</a> A sequence variant
    # that changes non-coding exon sequence in a non-coding transcript (is a: {@link #NON_CODING_TRANSCRIPT_VARIANT},
    # {@link #EXON_VARIANT}).
    # 
    'NON_CODING_TRANSCRIPT_EXON_VARIANT',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001970">SO:0001970</a> A sequence variant
    # that changes non-coding intro sequence in a non-coding transcript (is a: {@link #NON_CODING_TRANSCRIPT_VARIANT},
    # {@link #INTRON_VARIANT}).
    # 
    'NON_CODING_TRANSCRIPT_INTRON_VARIANT',

    #
    # Marker for smallest {@link VariantEffect} with {@link PutativeImpact#LOW} impact.
    # 
    # _SMALLEST_LOW_IMPACT,
    #
    #
    # MODIFIER Putative Impact
    #
    #
    # duplication marker
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:1000039">SO:1000039</a> A tandem
    # duplication where the individual regions are in the same orientation (is a: tandem_duplication).
    # <p>
    # In Jannovar used, as an additional marker to describe that a duplication is a tandem duplication.
    # 
    'DIRECT_TANDEM_DUPLICATION',

    # mobile element markers
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0002066">SO:0002066</a> A deletion of a
    # mobile element when comparing a reference sequence (has mobile element) to a individual sequence (does not have
    # mobile element).
    # <p>
    # In Jannovar used, as an additional marker to describe that a deletion is a mobile element deletion.
    # 
    'MOBILE_ELEMENT_DELETION',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001837">SO:0001837</a> A kind of insertion
    # where the inserted sequence is a mobile element.
    # <p>
    # In Jannovar used, as an additional marker to describe that an insertion is a mobile element insertion.
    # 
    'MOBILE_ELEMENT_INSERTION',

    # variant in custom region
    #
    # Variant in a user-specified custom region.
    # 
    # <b>Not</b> used in Jannovar annotations.
    # 
    # TODO(holtgrem): use?
    'CUSTOM',

    # variants with distances to genes/transcripts
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001631">SO:0001631</a> A sequence variant
    # located 5' of a gene (is a: {@link #INTERGENIC_VARIANT}).
    # 
    'UPSTREAM_GENE_VARIANT',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001632">SO:0001632</a> A sequence variant
    # located 3' of a gene (is a: {@link #INTERGENIC_VARIANT}).
    # 
    'DOWNSTREAM_GENE_VARIANT',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001628">SO:0001628</a> A sequence variant
    # located in the intergenic region, between genes (is a: feature_variant).
    # 
    'INTERGENIC_VARIANT',

    # regulatory TFBS variants
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001895">SO:0001895</a> An ablation
    # whereby the deleted region includes a transcription factor binding site.
    # 
    # <b>Not</b> used in Jannovar annotations.
    # 
    'TFBS_ABLATION',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001892">SO:0001892</a> An amplification
    # of a region containing a transcription factor binding site.
    # 
    # <b>Not</b> used in Jannovar annotations.
    # 
    'TFBS_AMPLIFICATION',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001782">SO:0001782</a> A sequence variant
    # located within a transcription factor binding site (is a: {@link #REGULATORY_REGION_VARIANT}).
    # 
    # <b>Not</b> used in Jannovar annotations.
    # 
    'TF_BINDING_SITE_VARIANT',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001566">SO:0001566</a> A sequence variant
    # located within a regulatory region (is a: feature_variant).
    # 
    # <b>Not</b> used in Jannovar annotations.
    # 
    'REGULATORY_REGION_VARIANT',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001894">SO:0001894</a> A feature ablation
    # whereby the deleted region includes a regulatory region.
    # 
    # <b>Not</b> used in Jannovar annotations.
    # 
    'REGULATORY_REGION_ABLATION',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001891">SO:0001891</a>  Amplification of
    # a region containing a regulatory region.
    # 
    # <b>Not</b> used in Jannovar annotations.
    # 
    'REGULATORY_REGION_AMPLIFICATION',

    # variant in intronic regions
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0002018">SO:0002018</a> A transcript
    # variant occurring within a conserved region of an intron (is a: {@link #INTRON_VARIANT}).
    # 
    # <b>Not</b> used in Jannovar annotations.
    # 
    'CONSERVED_INTRON_VARIANT',

    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0002011">SO:0002011</a> A variant that
    # occurs within a gene but falls outside of all transcript features. This occurs when alternate transcripts of a
    # gene do not share overlapping sequence (is a: {@link #TRANSCRIPT_VARIANT} ).
    # 
    # TODO(holtgrem): use?
    'INTRAGENIC_VARIANT',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0002017">SO:0002017</a> A sequence variant
    # located in a conserved intergenic region, between genes (is a: {@link #INTERGENIC_VARIANT}).
    # 
    'CONSERVED_INTERGENIC_VARIANT',

    # general variant types
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001537">SO:0001537</a> A sequence variant
    # that changes one or more sequence features (is a: sequence variant).
    # 
    'STRUCTURAL_VARIANT',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001580">SO:0001580</a> A sequence variant
    # that changes the coding sequence (is a: {@link #CODING_TRANSCRIPT_VARIANT}, {@link #EXON_VARIANT}).
    # <p>
    # Sequence Ontology does <b>not</b> have a term
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/CODING_TRANSCRIPT_EXON_VARIANT" >
    # CODING_TRANSCRIPT_EXON_VARIANT</a>, so we use this.
    # 
    # <b>Not</b> used in Jannovar annotations.
    # 
    'CODING_SEQUENCE_VARIANT',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001627">SO:0001627</a> A transcript
    # variant occurring within an intron (is a: {@link #TRANSCRIPT_VARIANT}).
    # <p>
    # Jannovar uses {@link #CODING_TRANSCRIPT_INTRON_VARIANT} and {@link #NON_CODING_TRANSCRIPT_INTRON_VARIANT}
    # instead.
    # 
    'INTRON_VARIANT',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001791">SO:0001791</a> A sequence variant
    # that changes exon sequence (is a: {@link #TRANSCRIPT_VARIANT}).
    # 
    'EXON_VARIANT',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001568">SO:0001568</a> A sequence variant
    # that changes the process of splicing (is a: {@link #GENE_VARIANT}).
    # 
    # <b>Not</b> used in Jannovar annotations.
    # 
    'SPLICING_VARIANT',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0000276">SO:0000276</a> Variant affects a
    # miRNA (is a: miRNA_primary_transcript, small_regulatory_ncRNA).
    # 
    # <b>Not</b> used in Jannovar annotations.
    # 
    # TODO(holtgrem): use?
    'MIRNA',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001564">SO:0001564</a> A sequence variant
    # where the structure of the gene is changed (is a: feature_variant).
    # 
    # <b>Not</b> used in Jannovar annotations.
    # 
    'GENE_VARIANT',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001968">SO:0001968</a> A transcript
    # variant of a protein coding transcript (is a: {@link #TRANSCRIPT_VARIANT}).
    # <p>
    # Used, e.g., for marking SVs as affecting coding transcripts.
    # 
    'CODING_TRANSCRIPT_VARIANT',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001619">SO:0001619</a> (is a:
    # {@link #TRANSCRIPT_VARIANT}).
    # <p>
    # Used, e.g., for marking splicing variants as non-coding or SVs as affecting non-coding transcripts.
    # 
    'NON_CODING_TRANSCRIPT_VARIANT',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001576">SO:0001576</a> A sequence variant
    # that changes the structure of the transcript (is a: {@link #GENE_VARIANT}). TRANSCRIPT_VARIANT,
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:">SO:</a> (is a: {@link #GENE_VARIANT})).
    # 
    # <b>Not</b> used in Jannovar annotations.
    # 
    'TRANSCRIPT_VARIANT',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0000605">SO:0000605</a> A region containing
    # or overlapping no genes that is bounded on either side by a gene, or bounded by a gene and the end of the
    # chromosome (is a: biological_region).
    # 
    # <b>Not</b> used in Jannovar annotations.
    # 
    'INTERGENIC_REGION',
    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0000340">SO:0000340</a> Structural unit
    # composed of a nucleic acid molecule which controls its own replication through the interaction of specific
    # proteins at one or more origins of replication (is a: replicon).
    # 
    # <b>Not</b> used in Jannovar annotations.
    # 
    'CHROMOSOME',

    #
    # <a href="http://www.sequenceontology.org/browser/current_svn/term/SO:0001060">SO:0001060</a> Top level term for
    # variants, can be used for marking "uknown effect".
    # 
    # <b>Not</b> used in Jannovar annotations.
    # 
    'SEQUENCE_VARIANT'
)

VARIANT_EFFECT_PRIORITIES = {e: i for i, e in enumerate(VARIANT_EFFECTS)}


def get_priority(effect: str) -> int:
    """
    Return a numeric value for given `effect`. Lower the value, higher the priority.
    :param effect: string like `MISSENSE_VARIANT`
    :return: integer representing the priority, -1 if the `effect` is un-recognized/gibberish/None
    """
    return VARIANT_EFFECT_PRIORITIES[effect] if effect in VARIANT_EFFECTS else -1
