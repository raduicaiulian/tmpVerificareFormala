def expand(formula):
    loop_stack = []
    output_formula = ""
    while(formula):
        if "and(" in formula or "or(" in formula: # parse input formula to a stack of loops
            # if "and(" in formula:
            #     and_index = formula.index("and(") + 4
            # else:
            #     and_index = len(formula)
            and_index = formula.index("and(") + 4 if "and(" in formula else len(formula)
            # if "or(" in formula:
            #     or_index = formula.index("or(") + 3
            # else:
            #     or_index = len(formula)
            or_index = formula.index("or(") + 3 if "or(" in formula else len(formula)
            
            if or_index == len(formula) and and_index == len(formula):
                continue
            #if or_index < and_index:
            #    breakpoint()
            f_start = and_index if and_index < or_index else or_index
            f_end = formula.index(")")
            print(formula[f_start:f_end])
            loop_stack.append(formula[f_start:f_end] + (",and" if and_index < or_index else ",or"))
            formula = formula[f_end+1:]
            print(formula)
        else: # finished parsing loops, generate literals
            formula = ""
            dinamic_for_loop="out = ''\nop = ''\n"
            number_of_tabs = 1
            formula = "out += f\"{op} S("
            for loop in loop_stack:
                loop_element = loop.split(",")
                dinamic_for_loop += f"for {loop_element[0]} in range({loop_element[1]}, {str(int(loop_element[2])+1)}):"
                dinamic_for_loop += "\n" + "\t" * number_of_tabs
                if loop != loop_stack[-1]:
                    dinamic_for_loop += f"op = '{loop_element[3]}'"
                    dinamic_for_loop += "\n" + "\t" * number_of_tabs
                number_of_tabs += 1
                formula += "{" + loop_element[0]+ "},"
                if loop == loop_stack[-1]:
                    # breakpoint()
                    dinamic_for_loop += formula[:-1] + ") " + "\""
                    dinamic_for_loop += "\n" + "\t" * (number_of_tabs - 1)
                    dinamic_for_loop += f"op = '{loop_element[3]}'\n"
            dinamic_for_loop += 'out = out[out.index(" ")+1:]'

            # for debugging
            dinamic_for_loop += '\nprint("----------out------------")\n'
            dinamic_for_loop += 'print(out)\n'
            dinamic_for_loop += 'print("----------out------------")\n'
            dinamic_for_loop += 'print("and" in out)\n'

            print(dinamic_for_loop)
            exec(dinamic_for_loop) # exposes the extended formula in out var
            breakpoint()
            pass
        print(loop_stack)


expand("and(x,1,9) and(y,1,9) or(z,1,9) S(x,y,z)")
