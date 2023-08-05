from singlecellmultiomics.utils.sequtils import hamming_distance
import pysamiterators.iterators
import singlecellmultiomics.modularDemultiplexer.baseDemultiplexMethods
from singlecellmultiomics.utils import style_str
complement = str.maketrans('ATCGN', 'TAGCN')
import itertools

class Fragment():
    """
    Fragment

    This class holds 1 or more reads which are derived from the same cluster
    """

    def __init__(self, reads, assignment_radius=3, umi_hamming_distance=1,
                R1_primer_length=0,
                R2_primer_length=6,
                tag_definitions=None,
                mapping_dir = (False,True) # R1 forward, R2 reverse
                 ):
        """
        Initialise Fragment

            Args:
                reads( list ):
                    list containing pysam AlignedSegment reads

                assignment_radius( int ):
                    Assignment radius for molecule resolver

                umi_hamming_distance( int ):
                    umi_hamming_distance distance threshold for associating multiple fragments to a molecule

                R1_primer_length(int):
                    length of R1 primer, these bases are not taken into account when calculating a consensus

                R2_primer_length(int):
                    length of R2 primer, these bases are not taken into account when calculating a consensus

                tag_definitions(list):
                    sam TagDefinitions

                mapping_dir( tuple ):
                    expected mapping direction of mates,
                    True for reverse, False for forward. This parameter is used in dovetail detection

            Returns:
                html(string) : html representation of the fragment
        """
        self.R1_primer_length = R1_primer_length
        self.R2_primer_length = R2_primer_length
        if tag_definitions is None:
            tag_definitions = singlecellmultiomics.modularDemultiplexer.baseDemultiplexMethods.TagDefinitions
        self.tag_definitions = tag_definitions
        self.assignment_radius = assignment_radius
        self.umi_hamming_distance = umi_hamming_distance
        self.mapping_dir = mapping_dir
        self.reads = reads
        self.strand = None
        self.meta = {} # dictionary of meta data
        self.is_mapped = None
        ### Check for multimapping
        self.is_multimapped = True
        self.mapping_quality = 0
        self.match_hash=None

        # Span:\
        self.span=[None,None,None]

        self.umi=None

        # Force R1=read1 R2=read2:
        for i, read in enumerate(self.reads):

            if read is None:
                continue

            if not read.is_unmapped:
                self.is_mapped = True
            if read.mapping_quality>0:
                self.is_multimapped = False
            self.mapping_quality = max(self.mapping_quality, read.mapping_quality)
            if i==0:
                if read.is_read2:
                    raise ValueError('Supply first R1 then R2')
                read.is_read1 = True
                read.is_read2 = False
            elif i==1:
                read.is_read1 = False
                read.is_read2 = True

        self.set_sample()
        self.set_strand(self.identify_strand())
        self.update_span()
        self.update_umi()



    def write_tensor(self, chromosome=None, span_start=None, span_end=None, height=30, index_start=0,
                base_content_table=None,
                base_mismatches_table=None,
                base_indel_table =None,
                base_qual_table=None,

                    ):

        """
        Get tensor representation of the fragment

        Args:
            chromosome( str ):
                chromosome to view

            span_start( int ):
                first base to show

            span_end( int ):
                last base to show

            show_read1(bool):
                show read1

            show_read2(bool):
                show read2

        Returns:
            html(string) : html representation of the fragment

        """
        self.base_mapper = {}
        for i,(strand,base) in enumerate(itertools.product((True,False),'NACTG-')):
            self.base_mapper[(strand,base)] = i+2

        if chromosome is None and span_start is None and span_end is None:
            chromosome, span_start, span_end = self.get_span()

        span_len = span_end - span_start

        reads = self


        for ri,read in enumerate(reads):
            row_index = (ri+index_start) % height
            if read is None:
                continue
            for cycle, query_pos, ref_pos, ref_base in pysamiterators.iterators.ReadCycleIterator(read,with_seq=True):
                if ref_pos is None:
                    continue
                if (ref_pos-span_start)<0 or (ref_pos-span_start)>(span_len-1):
                    continue

                ref_base = ref_base.upper()
                if query_pos is None:
                    query_base='-'
                    qual = 0
                    base_indel_table[row_index,ref_pos-span_start] = 1
                else:
                    query_base = read.seq[query_pos]
                    qual = ord(read.qual[query_pos])

                if ref_pos is not None:
                    base_qual_table[row_index, ref_pos-span_start] = qual
                    if query_base!=ref_base:
                        base_content_table[row_index, ref_pos-span_start] = self.base_mapper[(read.is_reverse,query_base)]
                    else:
                        base_mismatches_table[row_index, ref_pos-span_start] = 0.2
                    base_content_table[row_index, ref_pos-span_start] = self.base_mapper[(read.is_reverse,query_base)]
        return ri+index_start+1


    def get_read_group(self):
        """
        Obtain read group for this fragment
        Returns:
            read_group(str) : Read group containing flow cell lane and unique sample id
        """
        rg = None
        for read in self.reads:
            if read is not None:
                rg = f"{read.get_tag('Fc') if read.has_tag('Fc') else 'NONE'}.{read.get_tag('La') if read.has_tag('La') else 'NONE'}.{read.get_tag('SM') if read.has_tag('SM') else 'NONE'}"
                break
        return rg

    def set_duplicate(self, is_duplicate):
        """Define this fragment as duplicate, sets the corresponding bam bit flag
        Args:
            value(bool) : is_duplicate
        """
        for read in self.reads:
            if read is not None:
                read.is_duplicate = is_duplicate

    def write_tags(self):
        self.set_meta('MQ',self.mapping_quality)
        self.set_meta('MM',self.is_multimapped)
        self.set_meta('RG', self.get_read_group())
        if self.has_valid_span():
            # Write fragment size:
            self.set_meta('fS',abs(self.span[2]-self.span[1]))
            self.set_meta('fe',self.span[1])
            self.set_meta('fs',self.span[2])

    def write_pysam(self, pysam_handle):
        """Write all associated reads to the target file

        Args:
            target_file (pysam.AlignmentFile) : Target file
        """
        self.write_tags()
        for read in self:
            if read is not None:
                pysam_handle.write(read)


    def identify_strand(self):
        # If R2 is rev complement:
        if self.get_R1() is not None:
            # verify if the read has been mapped:
            if self.get_R1().is_unmapped:
                return None
            return self.get_R1().is_reverse
        elif self.get_R2() is not None:
            # verify if the read has been mapped:
            if self.get_R2().is_unmapped:
                return None
            return not self.get_R2().is_reverse
        return None


    def get_random_primer_hash(self):
        """Obtain hash describing the random primer
        Returns None,None when the random primer cannot be described
        Returns
        -------
        reference_start : int or None
        sequence : str or None
        """
        R2 = self.get_R2()
        if R2 is None or R2.query_sequence is None:
            return None,None
        # The read was not mapped
        if R2.is_unmapped:
            # Guess the orientation does not matter
            return None, R2.query_sequence[:self.R2_primer_length]

        if R2.is_reverse:
            global complement
            return(R2.reference_end, R2.query_sequence[-self.R2_primer_length:][::-1].translate(complement))
        else:
            return(R2.reference_start, R2.query_sequence[:self.R2_primer_length])
        raise ValueError()


    def set_meta(self, key, value):
        self.meta[key] = value
        for read in self:
            if read is not None:
                read.set_tag(key,value)

    def get_R1(self):
        if len(self.reads)==0:
            raise IndexError('The fragment has no associated reads')
        return self.reads[0]
    def get_R2(self):
        if len(self.reads)<2:
            raise IndexError('The fragment has no associated R2')
        return self.reads[1]

    def has_R1(self):
        if len(self.reads)==0:
            return False
        return self.reads[0] is not None

    def has_R2(self):
        if len(self.reads)<2:
            return False
        return self.reads[1] is not None


    def update_span(self):


        if self.mapping_dir!=(False,True):
            raise NotImplementedError("Sorry only FW RV is implemented")

        contig = None
        for read in self.reads:
            if read is not None and not read.is_unmapped:
                contig = read.reference_name

        try:
            surfaceStart, surfaceEnd = pysamiterators.iterators.getPairGenomicLocations(
                self.get_R1(),
                self.get_R2(),
                R1PrimerLength = self.R1_primer_length,
                R2PrimerLength = self.R2_primer_length,
                allow_unsafe=True
                )
            self.span = (contig,surfaceStart, surfaceEnd)
        except Exception as e:

            if self.has_R1() and not self.get_R1().is_unmapped:
                self.span = (contig, self.get_R1().reference_start,self.get_R1().reference_end)




    def get_span(self):
        return self.span

    def has_valid_span(self):
        return not any([x is None for x in self.get_span()])

    def set_sample(self, sample=None):
        """Force sample name or obtain sample name from associated reads"""
        if sample is not None:
            self.sample = sample
        else:
            for read in self.reads:
                if read is not None and read.has_tag('SM'):
                    self.sample = read.get_tag('SM')
                    break


    def get_sample(self):
        return self.sample


    def __len__(self):
        """Obtain the amount of associated reads to the fragment

        Returns:
            assocoiated reads (int)
        """
        return(sum(read is not None for read in self.reads))


    def set_strand(self, strand):
        self.strand = strand

    def get_strand(self):
        return self.strand

    def update_umi(self):
        for read in self.reads:
            if read is not None and read.has_tag('RX'):
                self.umi=read.get_tag('RX')

    def get_umi(self):
        return self.umi

    def __iter__(self):
        return iter(self.reads)

    def umi_eq(self, other):
        if self.umi==other.umi:
            return True
        if self.umi_hamming_distance==0:
            return False
        else:
            return hamming_distance(self.umi,other.umi)<=self.umi_hamming_distance

    def __eq__(self, other): # other can also be a Molecule!
        # Make sure fragments map to the same strand, cheap comparisons
        if self.sample!=other.sample:
            return False

        if self.strand!=other.strand:
            return False

        if min(  abs( self.span[1] - other.span[1] ),  abs( self.span[2] - other.span[2] ) ) >self.assignment_radius:
            return False

        # Make sure UMI's are similar enough, more expensive hamming distance calculation
        return self.umi_eq(other)

    def __getitem__(self, index):
        """
        Get a read from the fragment

        Args:
            index( int ):
                0 : Read 1
                1: Read 2
                ..
        """
        return self.reads[index]

    def is_valid(self):
        return self.has_valid_span()

    def get_strand_repr(self):
        s = self.get_strand()
        if s is None:
            return '?'
        if s:
            return '-'
        else:
            return '+'

    def __repr__(self):
        return f"""Fragment:
        sample:{self.get_sample()}
        umi:{self.get_umi()}
        span:{('%s %s-%s' % self.get_span())}
        strand:{self.get_strand_repr()}
        has R1: {"yes" if self.has_R1() else "no"}
        has R2: {"yes" if self.has_R2() else "no"}
        """ + '\n\t'.join([f'{key}:{str(value)}'for key,value in self.meta.items()])

    def get_html(self, chromosome=None, span_start=None, span_end=None, show_read1=None, show_read2=None):
        """
        Get HTML representation of the fragment

        Args:
            chromosome( str ):
                chromosome to view

            span_start( int ):
                first base to show

            span_end( int ):
                last base to show

            show_read1(bool):
                show read1

            show_read2(bool):
                show read2

        Returns:
            html(string) : html representation of the fragment

        """

        if chromosome is None and span_start is None and span_end is None:
            chromosome, span_start, span_end = self.get_span()

        span_len = abs( span_end - span_start )
        visualized_frag = ['.']  * span_len

        if show_read1 is None and show_read2 is None:
            reads = self
        else:
            reads = []
            if show_read1:
                reads.append(self.get_R1())
            if show_read2:
                reads.append(self.get_R2())

        for read in reads:
            if read is None:
                continue
            for cycle, query_pos, ref_pos, ref_base in pysamiterators.iterators.ReadCycleIterator(read,with_seq=True):
                if ref_pos is None:
                    continue
                ref_base = ref_base.upper()
                if query_pos is None:
                    query_base='-'
                else:
                    query_base = read.seq[query_pos]
                if ref_pos is not None:
                    if query_base!=ref_base:
                         v = style_str(query_base,color='red',weight=500)
                    else:
                        v= query_base
                    try:
                        visualized_frag[ref_pos-span_start] = v
                    except IndexError:
                        pass # the alignment is outside the requested view
        return ''.join(visualized_frag)

    def set_rejection_reason(self, reason):
        self.set_meta('RR',reason)

    def set_recognized_sequence(self, seq):
        self.set_meta('RZ',seq)


class SingleEndTranscript(Fragment):
    def __init__(self,reads, **kwargs):
        Fragment.__init__(self, reads, **kwargs)
