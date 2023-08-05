from singlecellmultiomics.molecule.molecule import Molecule
from singlecellmultiomics.molecule.featureannotatedmolecule import FeatureAnnotatedMolecule

class CHICMolecule(Molecule):
    """CHIC Molecule class

    Args:
        fragments (singlecellmultiomics.fragment.Fragment): Fragments to associate to the molecule
        **kwargs: extra args

    """
    def __init__(self,fragment,
                **kwargs):
        Molecule.__init__(self,fragment,**kwargs)

    def write_tags(self):
        Molecule.write_tags(self)


    def is_valid(self,set_rejection_reasons=False):

        try:
            chrom,start,strand = self.get_cut_site()
        except Exception as e:
            if set_rejection_reasons:
                self.set_rejection_reason('no_cut_site_found')
            return False

        return True

    def get_fragment_span_sequence(self,reference=None):
            """Obtain the sequence between the start and end of the molecule
            Args:
                reference(pysam.FastaFile) : reference  to use.
                    If not specified self.reference is used
            Returns:
                sequence (str)
            """
            if reference is None:
                if self.reference is None:
                    raise ValueError('Please supply a reference (PySAM.FastaFile)')
            reference = self.reference
            return reference.fetch(self.chromosome, self.spanStart, self.spanEnd).upper()


class AnnotatedCHICMolecule(FeatureAnnotatedMolecule,CHICMolecule):
    """Chic Molecule which is annotated with features (genes/exons/introns, .. )

    Args:
        fragments (singlecellmultiomics.fragment.Fragment): Fragments to associate to the molecule
        features (singlecellmultiomics.features.FeatureContainer) : container to use to obtain features from
        **kwargs: extra args

    """
    def write_tags(self):
        CHICMolecule.write_tags(self)
        FeatureAnnotatedMolecule.write_tags(self)

    def __init__(self,fragment, features, **kwargs):
        FeatureAnnotatedMolecule.__init__(self,fragment,features,**kwargs)
        CHICMolecule.__init__(self,fragment,**kwargs)
