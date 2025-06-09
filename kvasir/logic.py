from typing import Any, Dict
from clingo import Control
from .utils import logger
from .program import Program

class Query:
    def __init__(self, entry: str):
        with open(entry, "r") as file:
            if not file.readable():
                raise ValueError(f"Query file {entry} is not readable.")
            self.query = file.read().strip()

class KnowledgeBase:
    def __init__(self):
        self.ctl = Control([])
        self.program = ""

    def solve(self, query: str):
        results = []

        # self.add_logic(query)

        self.ctl.add("base", [], self.program)
        self.ctl.ground([("base", [])])

        def on_model(model):
            atoms = [str(atom) for atom in model.symbols(shown=True)]
            results.append(atoms)

        with self.ctl.solve(yield_=True) as handle:
            for model in handle:
                on_model(model)
                logger.debug(f"Model: {model}")

        return results

    def add_logic(self, logic: str):
        self.program += logic + "\n"

def run_engine(kb: KnowledgeBase, query: str, program: Program):

    code = (
        """
do(X) :- goal(X).

{ do(X) } :- can(X).

ndo(N) :- N = #count { X : do(X) }.
#maximize { N : ndo(N) }.

:- goal(X), not do(X).

#show do/1.
        """
    )

    kb.add_logic(code)

    return kb.solve(query)

class Plan:
    def __init__(self, extracted_properties):
        self.properties: Dict[str, Any] = extracted_properties  # Dict[str, Any]
        self.history = []  # e.g., list of prior generations / decisions

    def reconfigure(self, new_info) -> "Plan":
        """Update plan based on new synthesis results (e.g., failed verification)."""
        self.history.append(new_info)
        # Optionally mutate `self.properties` or add constraints
        return self

def plan(kb, query, program):
    # Run the logic program given the query and program to produce a plan
    
    to_extract = run_engine(kb, query, program) 
    print(f"Extracted properties: {to_extract}")

    return Plan(extracted_properties={})
