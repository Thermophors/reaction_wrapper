from rdkit import Chem
from rdkit.Chem import rdChemReactions
from typing import Set


class ReactionWrapper:
    """A class to represent chemical transformation.

    This is a wrapper for the rdChemRections.RunReactants:
    https://www.rdkit.org/docs/source/rdkit.Chem.rdChemReactions.html

    Attributes
    ----------
    reaction_smarts : str
        reaction SMARTS
    reactants_smi : str
        reactant SMILES

    Methods
    -------
    run_reaction()
        Run reaction using validated reaction SMARTS and reactant SMILES
    """

    def __init__(self, reaction_smarts: str, reactants_smi: str, limit_products: int = 1000) -> None:
        """
        Parameters
        ----------
        reaction_smarts : str
            reaction SMARTS
        reactants_smi : str
            reactant SMILES
        limit_products : int, optional
            maximum number of returned reaction products, by default 1000

        Raises
        ------
        ValueError
            if reactant SMILES is valid
        ValueError
            if reaction SMARTS is valid
        ValueError
            if reaction SMART is valid using builtin method 
        ValueError
            if reaction is compatible with the reactants
        """
        self.reactants_smi = reactants_smi
        self.reaction_smarts = reaction_smarts
        self.limit_products = limit_products

        # Check if reactant SMILES is valid
        self.reactants_mol = Chem.MolFromSmiles(self.reactants_smi)
        if not self.reactants_mol:
            raise ValueError('Invalid reactant SMILES')

        # Check if reaction SMARTS is valid
        self.rxn = rdChemReactions.ReactionFromSmarts(self.reaction_smarts)
        if not self.rxn:
            raise ValueError(
                'Invalid reaction SMARTS, cannot generate reaction object.')

        # Check if reaction SMART is valid using builtin method
        _, num_errors = self.rxn.Validate()
        if num_errors > 0:
            raise ValueError('Invalid reaction SMARTS')

        # Check if reaction is compatible with the reactants
        self.rxn.Initialize()
        if not self.rxn.IsMoleculeReactant(self.reactants_mol):
            raise ValueError('Reactants not compatible with the reaction')

    def run_reaction(self) -> Set:
        """ Run reaction using validated reaction SMARTS and reactant SMILES

        Returns set of product tuples obtained from validated reaction SMARTS and reactants SMILES

        Returns
        -------
        set
           set containing unique product SMILES
        """

        products = self.rxn.RunReactants(
            (self.reactants_mol,), maxProducts=self.limit_products)
        unique_products = set([tuple(map(Chem.MolToSmiles, p))
                              for p in products])
        return unique_products
