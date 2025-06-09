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

    def solve(self, query: Query):
        """Solve the query using the knowledge base."""
        results = []

        logger.debug(f"Solving query: {query.query}")
        logger.debug(f"Using program:\n{self.program}")

        self.add_logic(query.query)

        self.ctl.add("base", [], self.program)
        self.ctl.ground([("base", [])])

        def on_model(model):
            for atom in model.symbols(shown=True):
                if atom.match("do", 1):
                    results.append(atom.arguments[0].name)

        with self.ctl.solve(yield_=True) as handle:
            for model in handle:
                on_model(model)

        logger.debug(f"Solved query: {query.query} with results: {results}")
        return results

    def add_logic(self, logic: str, comment: str=""):
        self.program += logic + " " + (f"% {comment}" if comment else "") + '\n'

def run_engine(kb: KnowledgeBase, query: Query, program: Program) -> Dict[str, Any]:
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

    return { k: True for k in kb.solve(query)}

class Plan:
    def __init__(self, properties: Dict[str, Any]):
        self.properties: Dict[str, Any] = properties
        self.history = []  # e.g., list of prior generations / decisions

    def reconfigure(self, new_info) -> "Plan":
        """Update plan based on new synthesis results (e.g., failed verification)."""
        self.history.append(new_info)
        # Optionally mutate `self.properties` or add constraints
        return self
    
    def does(self, property_name: str) -> bool:
        """Check if the plan includes actions for the given plugin."""
        # Handle module names
        if "." in property_name:
            property_name = property_name.split(".")[-1]
        return property_name in self.properties

    def __repr__(self):
        return f"Plan(properties={self.properties})"

def plan(kb: KnowledgeBase, query: Query, program: Program):
    # Run the logic program given the query and program to produce a plan
    
    to_extract = run_engine(kb, query, program) 
    print(f"Extracted properties: {to_extract}")

    return Plan(properties=to_extract)
