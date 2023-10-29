def expand(file_name, formula):
    loop_stack = []
    formula_stack = []
    output_formula = ""
    while(formula):
        if "and(" in formula or "or(" in formula: # parse input formula to a stack of loops
            and_index = formula.index("and(") + 4 if "and(" in formula else len(formula)
            or_index = formula.index("or(") + 3 if "or(" in formula else len(formula)
            
            if or_index == len(formula) and and_index == len(formula):
                continue

            f_start = and_index if and_index < or_index else or_index
            f_end = formula.index(")")
            #loop_stack can have forulas, we need to handle that scenario
            # print(formula[f_start:f_end])
            loop_stack.append(formula[f_start:f_end] + (",and" if and_index < or_index else ",or"))
            formula = formula[f_end+1:]
            # print(formula)
        else: # finished parsing loops, generate literals
            # ------------------------------------------------------------------
            # f = " (not(S(x,y,z)) or not(S(i,y,z)))"
            # f = " (not(S(x,y,z)) or not(S(i,y,z)) or S(z,x,y))"
            f  = formula
            f = f.strip()
            if f[0] == '(' and f[-1] == ')':
                f=f[1:-1]
            formula_stack = f.strip().split("or")
            parsed_formula_stack = []
            for i in formula_stack:
                # print(i)
                b_pars = i.index("S(")+2
                e_pars = i.index(")")
                interm_param_ofmember = []
                for j in i[b_pars:e_pars].split(","):
                    interm_param_ofmember.append(",".join(["{"+j+"}"]))
                # print(interm_param_ofmember)
                f_out = i[:b_pars] + ",".join(interm_param_ofmember) + i[e_pars:]
                # print(f_out)
                parsed_formula_stack.append(f_out)
            #when ready
            # f = "(" + "or".join(parsed_formula_stack) + ")"
            formula_to_inject = "or".join(parsed_formula_stack)
            # print(formula_to_inject)
            # breakpoint()
            # ------------------------------------------------------------------
            tmp_formula = ""
            dinamic_for_loop="out = ''\nop = ''\n"
            number_of_tabs = 1
            tmp_formula = "out += f\"{op} " + formula_to_inject
            for loop in loop_stack:
                # index 0 = variable(x/y/z)
                # index 1,2 = range of the variable(1,9/1,8)
                # index 3 = boolean operator(and/or)
                loop_element = loop.split(",")
                dinamic_for_loop += f"for {loop_element[0]} in range({loop_element[1]}, {str(int(loop_element[2])+1)}):"
                dinamic_for_loop += "\n" + "\t" * number_of_tabs
                if loop != loop_stack[-1]:
                    dinamic_for_loop += f"op = '{loop_element[3]}'"
                    dinamic_for_loop += "\n" + "\t" * number_of_tabs
                number_of_tabs += 1
                # if len(loop_element[0]) > 1:
                #     print("loop_element[0]", loop_element[0])
                #     breakpoint()
                #     # do the cmoputation
                # else:
                #     tmp_formula += "{" + loop_element[0]+ "},"
                # tmp_formula += "{" + loop_element[0]+ "},"
                if loop == loop_stack[-1]:
                    # breakpoint()
                    # dinamic_for_loop += tmp_formula[:-1] + ") " + "\""
                    dinamic_for_loop += tmp_formula + ") " + "\""
                    dinamic_for_loop += "\n" + "\t" * (number_of_tabs - 1)
                    dinamic_for_loop += f"op = '{loop_element[3]}'\n"
            dinamic_for_loop += 'out = out[out.index(" ")+1:]'

            # for debugging
            # dinamic_for_loop += '\nprint("----------out------------")\n'
            # dinamic_for_loop += 'print(out)\n'
            # dinamic_for_loop += 'print("----------out------------")\n'
            # dinamic_for_loop += 'print("and" in out)\n'
            dinamic_for_loop += f'\nwith open("{file_name}","w") as file:'
            dinamic_for_loop += "\n" + "\t" * number_of_tabs
            dinamic_for_loop += f'file.write(out)'

            print(dinamic_for_loop)
            exec(dinamic_for_loop) # exposes the extended formula in out var
            return
            # breakpoint()
def get_number(dict, number, literal):
    if literal not in dict.keys():
        return number + 1
    return number
def convert_to_dimacs(formulas):
    # read formulas from text files
    formulas_str = []
    dimacs_map = {}
    dimacs_formula = ""
    number_of_clauses = 0
    for file_name in formulas:
        with open(file_name,"r") as file:
            formula = file.read()
            formulas_str.append(formula)
    
    # actual converting of the formulas
    # conjunctions = formula.split(" and")
    number = 1
    for conjunctions in formulas_str:
        for i in conjunctions.split(" and "):

            disjunctions = i.split("or")
            # print(disjunctions)
            

            for literal in disjunctions:                
                # literal = literal.strip()
                number = get_number(dimacs_map, number, literal)
                if "not" in literal:
                    # content_of_not = literal[4:-1] if #I know it is not a good practice to hardcode the indexes, but for now it should work
                    literal = literal.strip()
                    content_of_not = literal[literal.index("not(")+4:literal.rindex(")")-1] if literal.count(")") == (literal.count("(") + 1) else literal[literal.index("not(")+4:literal.rindex(")")]#I know it is not a good practice to hardcode the indexes, but for now it should work
                    # sanity test
                    if content_of_not.count("(") != content_of_not.count(")"):
                        print("Problem")
                    print(content_of_not)
                    # breakpoint()
                    dimacs_map[content_of_not] = number
                    dimacs_formula += str(- number) + " "
                else:
                    dimacs_map[literal] = number
                    dimacs_formula += str(number) + " "
            dimacs_formula += "0\n"
            number_of_clauses += 1
    numbe_of_literals = max(dimacs_map.values())
    # breakpoint()
    print("numbe_of_literals", numbe_of_literals,"number_of_clauses", number_of_clauses)
    dimacs_formula = f"p cnf {numbe_of_literals} {number_of_clauses}\n" + dimacs_formula
    #write dimacs formula to file
    with open("dimacs.out","w") as file:
        file.write(dimacs_formula)
    # breakpoint()

    
#test 1: the parser should be able to parse the following formulas
# There is at least one number in each entry
expand("f1", "and(x,1,9) and(y,1,9) or(z,1,9) S(x,y,z)")
# Each number appears at most once in each row
expand("f2", "and(y,1,9) and(z,1,9) and(x,1,8) and(i,x-1,9) (not(S(x,y,z)) or not(S(i,y,z)))")
# Each number appears at most once in each column
expand("f3", "and(x,1,9) and(z,1,9) and(y,1,8) and(i,y-1,9) (not(S(x,y,z)) or not(S(i,y,z)))")
#Each number appears at most once in each 3x3 sub-grid
expand("f4", "and(z,1,9) and(i,0,2) and(j,0,2) and(x,1,3) and(y,1,3) and(k,y+1,3) (not(S(3*i+x,3*j+y,z)) or not(S(3*i+x,3*j+k,z)))")
expand("f5", "and(z,1,9) and(i,0,2) and(j,0,2) and(x,1,3) and(y,1,3) and(k,x+1,3) and(l,1,3) (not(S(3*i+x,3*j+y,z)) or not(S(3*i+k,3*j+l,z)))")

convert_to_dimacs(["f1", "f2", "f3", "f4", "f5"])

