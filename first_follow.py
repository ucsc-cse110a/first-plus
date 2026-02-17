"""
Authors:
    Laurel Willey for CSE110A Homework #2
    Marcelo Siero Instructor for CSE110A

    Original code for First, Follow and First+ provided by Laurel.
    Marcelo added some relation visualization, and did some testing.

    Type: python first_follow.py  -g <file_name> 
    Use -h for help
    Use -t for tabular (i.e. show First and Follow as tabular charts)
    See sample files g0.py, g1.py, ..., g10.py, g_expr.py 
    The parser file is a python program

    Must install:
       pip install pandas
       pip install rich 

Source: https://www.cs.uaf.edu/~cs331/notes/FirstFollow.pdf  
"""
# import pdb; 

import pandas as pd
from rich.console import Console 
from rich.markdown import Markdown 
console = Console()
import argparse  
import os
#
EPSILON     = ''
EPSILON_str = 'e'

class g:
    # symbol implies Terminal or Non-Terminal
    grammar = {}                  # 
    eT                    = []    # expanded terminals (includes $)
                                  # Note $ is only needed for FOLLOW() sets
                                  # epsilon is only needed for FIRST set.
                                  # it is not needed for FIRST+ set.
                                  # Some text describe $, as EOF, or None
    start                 = ""
    T                     = []    # set of terminals, T, from grammar as ordered list
    NT                    = []    # set of non-terminals, NT, as ordered list
    rules                 = []    # [rule_no, lhs, [rhs]]  lhs is an NT, NT ::= ...
                                  # where RHS is the list of NT and T for that rule.
    first_temp            = {} # {NT: set()}; dict, key is an NT, value is a set from NT, eT 
    first_of_NT           = {} # {NT: set()}; dict where key is an NT, value is a set from NT,eT 
    first_of_rule         = {} # {rule_no: set()} set of T only.
    first_w_closure_of_NT = {} # {NT: set()};     set of T only.
    first_plus_for_NT     = {} # {NT: set()};     set of T only.
    first_plus_for_rule   = {} # {rule_no: set()}  set of first+ symbols for each rule
    follow_of_NT          = {} # {NR, set()}; key is NT, value is a set from NT,eT 

#:===== COMPUTE SET FUNCTIONS ==========================================
def compute_first(rules, nonterminals, terminals):
    """
    Computes the first set for each rule.
    This algorithm includes a mapping from terminal -> terminal
    which turns out to be useful for the given algorithm.

    Returns:
      FIRST: Dict of first sets for each rule, i.e. FIRST[R] = set()

    Algorithm source: https://www.cs.uaf.edu/~cs331/notes/FirstFollow.pdf
    Algorithm description (adapted):
        Note: 'e' means epsilon

        1a. If R is a terminal, FIRST[R] = {R}.
            # bootstrap algorithm, with FIRST(terminal)=terminal
        2a. If `R ::= e` is a production, add e to FIRST[R].
        3a. If `R ::= Y1 Y2 ... Yk`, then for each production:
            * Add FIRST(Y1) - {e} to FIRST[R]
            * if e in FIRST(Y1), also add FIRST(Y2) - {e}, etc.
            * if e in FIRST(Y1),...,FIRST(Yk), add e to FIRST[R].
    """
    # Initialize FIRST[R] = set() for all nonterminals
    FIRST = { R: set() for R in nonterminals }

    # Bootstrap the algorithm by making the first of all terminals by the terminal.
    # 1a. If R is a terminal, FIRST[R] = {R}.
    for t in terminals:
        FIRST[t] = {t}
    # The next line should happen automatically if EPSILON is in terminals.
    # FIRST[EPSILON] = {EPSILON}   # Also make sure FIRST[e] = {e}

    # 2a. If R -> e is a production, add e to FIRST[R].
    for _, R, rhs in rules:
        if not rhs:
            FIRST[R].add(EPSILON)

    # 3a. If R -> Y1 Y2 ... Yk, then for each production:
    # loop until sets are no longer changing
    expanded = True
    while expanded: # run until there are no more changes.
        expanded = False

        for _, R, rhs in rules: # we don't care about idx numbers, FIRST is indexed by R, not idx
            # compute FIRST(rhs) = FIRST(Y1...Yk)
            #   stop the sequence if Y_i does not have a first of EPSILON
            first_rhs = set()

            # for each symbol Yi in the RHS add to the FIRST set
            for symbol in rhs:
                # * Add FIRST(Y1) - {e} to FIRST[R]
                first_rhs |= (FIRST[symbol] - {EPSILON})

                # if Yi does not resolve to e, break here, we are done with this rule.
                # it EPSILON is in FIRST[symbol] it can nullify this symboel 
                if EPSILON not in FIRST[symbol]:
                    break

            # * if e in FIRST(Y1), also add FIRST(Y2) - {e}, etc.
            # * if e in FIRST(Y1),...,FIRST(Yk), add e to FIRST[R].

            else: # if we did not break out of the loop, and we are here
                  # implication is that that EPSILON is in FIRST[symbol]
                # If every Yi resolves to e, add e to FIRST(rhs)
                first_rhs.add(EPSILON)

            # If the set has expanded, union with FIRST[R]
            if not first_rhs <= FIRST[R]:  # i.e. first_rhs is > FIRST[R]
                FIRST[R] |= first_rhs      # Change it and expand it.
                # Reset flag to propagate expansion
                expanded = True

    # The return relation keeps the terminal to terminal relation
    # But does not keep NT to NT relation like transitive closure
    # it preserves EPSILON terminal
    return FIRST

def compute_first_wo_terminals(rules, nonterminals, terminals):
    tmp_first = compute_first(g.rules, g.NT, g.T)
    # filter out the reg to reg relations - not needed.
    first = filter_rows(tmp_first, g.NT)
    return(first)

def compute_follow(rules, nonterminals, FIRST, start_symbol):
    """
    Computes the follow set for each rule.

    Returns:
      FOLLOW: Dict of follow sets for each rule, i.e. FOLLOW[R] = set()

    Algorithm source: https://www.cs.uaf.edu/~cs331/notes/FirstFollow.pdf
    Algorithm description (adapted):
        Note: 'e' means epsilon

        1. Place EOF symb '$' in FOLLOW[S] for starting symbol S
        2. For any production `A => a B b`, add FIRST(B) - {e} to FOLLOW[B].
        3. For any production `A => a B` or `A => a B b` with e in FIRST(b), add FOLLOW[A] to FOLLOW[B].

    """
    # Initialize FOLLOW[R] = set() for all nonterminals
    FOLLOW = { R: set() for R in nonterminals }

    # 1. Place EOF symb '$' in FOLLOW[S] for starting symbol S
    FOLLOW[start_symbol].add('$')

    # loop until sets are no longer changing
    expanded = True
    while expanded:
        expanded = False

        # For each production A => rhs
        for idx, R, rhs in rules:  # For every rule
            # we don't care about idx numbers since 
            #      FOLLOW is indexed by R, not idx
            # for all rules of form: A=>aBb  
            # this holds FIRST(b) union FOLLOW(A) as we scan right to left
            trailer = FOLLOW[R].copy()

            # scan rhs from right to left (we want follow, not first)
            for symbol in reversed(rhs):
                if symbol in nonterminals:
                    # symb is nonterminal so anything that follows symb also follows R
                    # 2. For any production `A => a B b`, add FIRST(B) - {e} to FOLLOW[B].
                    # 3. For any production `A => a B` or `A => a B b` with e in FIRST(b), add FOLLOW[A] to FOLLOW[B].
                    if not trailer <= FOLLOW[symbol]:
                        # we caught our set expanding, so we reset expanded so the next loop propagates the change
                        FOLLOW[symbol] |= trailer
                        expanded = True

                    # update trailer to be FIRST(B) union (old trailer if epsilon in FIRST(B))
                    if EPSILON in FIRST[symbol]:
                        # B => e, so FOLLOW(B) includes FIRST(B) - {e} and whatever is in trailer
                        trailer |= (FIRST[symbol] - {EPSILON})
                    else:
                        # B does not resolve to e, so reset trailer = FIRST(B)
                        trailer = FIRST[symbol].copy()
                else:
                    # B is a terminal so the only thing following is FIRST(B)
                    trailer = FIRST[symbol].copy()
    return FOLLOW

def compute_first_plus(rules, FIRST, FOLLOW):
    """
    Compute first+ set by iterating over productions (R -> symb) and 
    accumulating all terminals that can begin strings derived from symb. 
    If symb resolves to epsilon, also add FOLLOW[R].

    Returns:
      FIRST_PLUS: Dict of first+ sets for each rule by idx, i.e. FIRST_PLUS[idx] = set()

    Note: FIRST_FOLLOW eliminates all EPSILONS.
    """
    FIRST_PLUS = {}
    # iterate over all rules
    for idx, R, rhs in rules:
        # create a first+ set for each rule to be inserted into FIRST_PLUS by rule idx
        fp = set()
        # iterate over all symbs on RHS of rule R
        for symbol in rhs:
            # FIRST[terminal] must == terminal
            # add terminal in the first set of symb to the first+ set of symb
            fp |= (FIRST[symbol] - {EPSILON})
            if EPSILON not in FIRST[symbol]:
                # since symbol cannot produce epsilon (i.e. it is not
                # nullable, we are done.
                break
        else: # If we exit normally we are all done we did not find an EPSILON.
            # Otherwise an EPSILON was found either directly or an NT
            # Thus we add the follow set for the LHS
            fp |= FOLLOW[R]

        # insert first+ for R into FIRST_PLUS by idk
        FIRST_PLUS[idx] = fp
    return FIRST_PLUS

#:===== END OF COMPUTE SETS ============================================================
def print_title(title):
    print()
    print(title)
    print("-" * len(title))

def print_relation(relation, title):
    """prints relation for FIRST or FOLLOW"""
    print_title(title)
    for key in relation:
        print(f'{key}: {" ".join(relation[key])}')

# Show a way to display <set>_of_nt as a relational table.
def unique_in_order(my_list, in_set={}):
    ''' returns ordere list of unique items, must be in_set if in_set is defined.'''
    unique_list = []
    seen = set()
    for item in my_list:
        if in_set:
            print("DIAG: ", type(item), type(in_set))
            if item not in in_set:
                continue
        if item not in seen:
            unique_list.append(item)
            seen.add(item)
    return(unique_list)

def filter_rows(relation, desired_rows):
    filtered_relation = {k: v for k, v in relation.items() if k in desired_rows} 
    return filtered_relation

def print_smy():
    print("START: ", g.start)
    print("NT: ", g.NT)
    print("T: ", g.T)
    print()
    print("RULES: ")  # show the rules
    for rule in g.rules:
       (rule_no, lhs, rhs) = rule
       print(f'{rule_no}. {lhs} : ', rhs)
    print()

def load_grammar(filename):
    """Executes the file and returns the grammar dictionary.
       Defines: g.rules,  
    """
    try:
        if not os.path.isfile(filename):
           raise FileNotFoundError(f"Grammar file '{filename}' does not exist.")
        context = {}
        with open(filename, "r") as f:
           code = f.read()
           exec(code, context)
        if "grammar" not in context:
           raise ValueError(f"File '{filename}' does not define a 'grammar' variable.")
        g.grammar = context["grammar"]
        # print("\nLoaded grammar:")
        non_terminals = []
        ordered_symbols = []
        ordered_terminal = []     # python >3.7 keys are ordered in dicts
        terminal_set = set()
        rule_no = 1
        for lhs, rules in g.grammar.items():
            # print("LHS: ", lhs) 
            non_terminals.append(lhs)    # append non-terminals in order given
            for rhs in rules:
                # print("RHS: ", rhs) 
                rule = [rule_no, lhs, rhs]
                g.rules.append(rule)
                if not rhs:
                    ordered_symbols.extend([""])  # collect all symbols in order given
                else:
                    ordered_symbols.extend(rhs)  # collect all symbols in order given
                rule_no += 1
        g.start = g.rules[0][1];  # first NT is considerd the start symbol.
        terminal_set = set(ordered_symbols) - set(non_terminals) # remove non-terminals
        g.T = sorted(list(terminal_set), reverse=True)
        # unique_in_order(ordered_symbols, terminal_set)  # return terminals in order given.
        g.eT = g.T + ['$']   # not needed until FOLLOW
        # We could test the grammar for non-defined non-terminals.
        g.NT = unique_in_order(non_terminals) 
        # Load the grammar
    except (FileNotFoundError, ValueError) as e:
        print(f"\nError: {e}")

    return context["grammar"]

def print_first_plus_set(rules, first_plus):
    print_title("FIRST+ SET")
    i = 0;
    for key in first_plus.keys():
        lhs = rules[i][1]
        print(f"{key}. {lhs} : " + " ".join(first_plus[key]))
        i += 1

def print_markdown_table(df, title):
    """convert EPSILON to EPSILON_str"""
    do_md_formatted = 1;  # print as console formatted markdown else just markdown
    chk_mark = 'v' if do_md_formatted else '\u2713'
    headers = [""] + list(df.columns)
    # Make First row: spanning the full width of the table
    n_cols = len(headers)
    title_str = f"**{title}**"  # center the title with Markdown bold
    title_prefix = "     " * (n_cols // 2)
    md = title_prefix + title_str + " " + "\n"
    # md = f"\n----{title}----\n"
    # Build Markdown
    # md = "| " + " | ".join(title_row) + " |" + "\n"
    # md += "|" + "|".join(["---"] * n_cols) + "|" + "\n"

    # Build Header
    md += "| " + " | ".join(headers) + " |" + "\n"
    md += "|" + "|".join(["---"] * len(headers)) + "|" + "\n"
    for idx in df.index:
        row = [idx] + [(chk_mark if df.loc[idx, col] else "") for col in df.columns]
        md += "| " + " | ".join(row) + " |" + "\n"
    if not do_md_formatted:
        print(md)
    else:
        md = Markdown(md)
        console.print(md)

def create_relational_table(relations, columns):
    """relation has the form: [{name: set}, ...]
       This returns a pandas relational table
       columns are typically terminals.
    """
    clean_relations = {}  # replace "" with EPSILON_str 
    for lhs, rhs_set in relations.items():
        # map empty string to EPSILON_str
        lhs_fixed = lhs if lhs != EPSILON else EPSILON_str
        rhs_fixed = {symbol if symbol != EPSILON else EPSILON_str for symbol in rhs_set}
        clean_relations[lhs_fixed] = rhs_fixed
    rows = clean_relations.keys()  # typically non-terminals
    columns = [c if c != EPSILON else EPSILON_str for c in columns]
    # print("CLEAN: ", clean_relations)
    # print("COLUMNS: ", columns)
    relations_table = pd.DataFrame(False, index=rows, columns=columns, dtype=bool)
    #
    for lhs, rhs in clean_relations.items():
        relations_table.loc[lhs, list(rhs)] = True
    return relations_table

def do_args():
    global args, grammar
    parser = argparse.ArgumentParser(description="Grammar LL(1) analysis.")
    parser.add_argument('-t', '--tabular', action='store_true', 
                             help='display relational tables first and follow')
    parser.add_argument('-a', '--all', action='store_true', 
                             help='display first and follow as well as firt+')
    # -g with default and type validation
    parser.add_argument('-g', metavar='FILENAME', type=str, default="grammar.py",
                        help='Input grammar file (default: grammar.py)')
    
    args = parser.parse_args()
    if (False):
        print("Flags:")
        print(f"  --tabular (-t): {args.tabular}")
        print(f"  -g <file>     : {args.g}")

def main():
    do_args()
    load_grammar(args.g)
    print_title("GRAMMAR")
    print_smy() 

    # compute first set (rules, nonterminals, terminals):
    first = compute_first(g.rules, g.NT, g.T)  # includes reg to reg relation
    first_no_terms = compute_first_wo_terminals(g.rules, g.NT, g.T)

    if args.all:
       if args.tabular: # print table
           first_table = create_relational_table(first_no_terms, g.T)
           print_markdown_table(first_table, "FIRST_TABLE TERMINALS FILTERED")
   
       print_relation(first_no_terms, "FIRST SET")
   
       if args.tabular:
           first_table = create_relational_table(first, g.T)
           print_markdown_table(first_table, "FIRST TABLE")
           # These include FIRST[terminal] == {terminal}

    follow = compute_follow(g.rules, g.NT, first, g.start)
    if args.all:
       if args.tabular:
           follow_table = create_relational_table(follow, g.eT)
           print_markdown_table(follow_table, "FOLLOW SET")
   
       print_relation(follow, "FOLLOW SET")

    first_plus = compute_first_plus(g.rules, first, follow)
    print_first_plus_set(g.rules, first_plus)

if __name__ == "__main__":
    main()

