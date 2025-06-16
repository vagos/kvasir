from typing import Dict

from clingo import Control

from kvasir import utils

from .program import Action, Program
from .utils import logger


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

    def solve(self, query: Query) -> Dict[str, Action]:
        """Solve the query using the knowledge base."""
        results = []

        self.add_logic(query.query)

        logger.debug(f"Using program:\n{self.program}")

        self.ctl.add("base", [], self.program)
        self.ctl.ground([("base", [])])

        def on_model(model):
            r = {}
            for atom in model.symbols(shown=True):
                if atom.match("do", 1):
                    name = atom.arguments[0].name
                    r[name] = Action.PRESERVE
                if atom.match("-do", 1):
                    name = atom.arguments[0].name
                    r[name] = Action.ELIMINATE
                if atom.match("do_min", 1):
                    name = atom.arguments[0].name
                    r[name] = Action.MINIMIZE
                if atom.match("do_max", 1):
                    name = atom.arguments[0].name
                    r[name] = Action.MAXIMIZE
            results.append(r)

        with self.ctl.solve(yield_=True) as handle:
            for model in handle:
                on_model(model)

        if not results:
            logger.error("Plan is unsatisfiable.")
            exit(1)

        return results[-1]

    def add_logic(self, logic: str, comment: str=""):
        self.program += logic + " " + (f"% {comment}" if comment else "") + '\n'

def run_engine(kb: KnowledgeBase, query: Query, program: Program) -> Dict[str, Action]:
    code = (
        """
% Don't change the language unless given as a goal.
:- do(language(p, X)), language(p, Y), X != Y, not goal(language(p, X)).

{ do(X) } :- can(X), not goal_min(X).
{ do_min(X) } :- can(X).

ndo(N) :- N = #count { X : do(X) }.
#maximize { N : ndo(N) }.

:- goal(X), not do(X).
:- goal_min(X), not do_min(X).

:- do(language(P, L1)), do(language(P, L2)), L1 != L2. % A program has one language.

#show do/1.
#show do_min/1.
        """
    )

    kb.add_logic(code)

    return kb.solve(query)

class Plan:
    def __init__(self, properties: Dict[str, Action]):
        self.properties: Dict[str, Action] = properties
        self.history: list[Program] = []
        self.fullfilment = {}

    def reconfigure(self, new_info):
        """Update plan based on new synthesis results (e.g., failed verification)."""
        self.history.append(new_info)

    def update(self, property: str, ok: bool):
        action = self.properties[property]
        match action:
            case Action.PRESERVE:
                self.fullfilment[property] = ok
            case Action.ELIMINATE:
                self.fullfilment[property] = ok
            case Action.MAXIMIZE:
                self.fullfilment[property] = ok
            case Action.MINIMIZE:
                self.fullfilment[property] = ok

    def is_fullfilled(self) -> bool:
        """Check if the plan is fully satisfied."""
        return all(self.fullfilment.get(prop, False) for prop in self.properties)
    
    def does(self, property_name: str) -> bool:
        """Check if the plan includes actions for the given plugin."""
        # Handle module names
        property_name = utils.plugin_basename(property_name)
        return property_name in self.properties

    def __repr__(self):
        return f"Plan(to_extract={self.properties})"

def plan(kb: KnowledgeBase, query: Query, program: Program):
    """ 
    Run the logic program given the query and program to produce a plan
    """
    
    properties = run_engine(kb, query, program) 
    logger.info(f"List of properties in the plan: {properties}")

    if 'language' in properties:    # TODO: Make sure this is correct
        del properties['language']  # Remove language property, handled by the program

    return Plan(properties=properties)
