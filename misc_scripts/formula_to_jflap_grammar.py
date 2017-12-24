import click
import re
import os
import functools

__doc__ = """
Convert a libre office forumla into an XML .jff file accepted by JFLAP
uses \"|\" (literal: "|") as separator. and literal: newline as newline
separator. Removes all whitespace (" "). Uses literal -> as production rule
symbol.
"""

RHS_DIVIDER = '"|"'  # == "\"|\""
NEWLINE = "newline"


@click.command()
@click.argument("formula_text", nargs=-1)
def main(formula_text):
    formula = functools.reduce(lambda a, b: a + b, formula_text)
    output_path = os.path.join(os.getcwd(), "grammar.jff")

    xml_out = convert(formula)
    with open(output_path, 'w') as f:
        f.write(xml_out)
    print(xml_out)


def convert(formula_text):
    """Convert a libre office formula to an XML .jff accepted by JFLAP
    
    :param formula_text: the raw text used to build the formula
    :return: a string of XML
    """
    # rm whitespace characters ('\n', ' ', '\t', etc.)
    formula_text = re.sub("\s", "", formula_text)
    xml_output = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
        <!--Created with JFLAP 6.4.--><structure>
        <type>grammar</type>
        <!--The list of productions.-->\n"""

    for rule in formula_text.split(NEWLINE):
        variable = ""
        # determine the variable of the rule
        for index, letter in enumerate(rule, start=0):
            # if production rule arrow encountered,
            # and the '-' char is not last character of rule
            if letter == '-' and len(rule) - 1 != index \
                    and rule[index+1] == ">":
                index += 2
                break
            variable += letter

        # determine the right hand side of the rule
        for right_element in rule[index:].split(RHS_DIVIDER):
            right_output = ""
            for index2, letter in enumerate(right_element, start=0):
                right_output += letter

            xml_output += "\t<production>\n" \
                          "\t\t<left>{}</left>\n" \
                          "\t\t<right>{}</right>\n" \
                          "\t</production>\n".format(variable, right_output)

    # done reading all production rules
    xml_output += "</structure>"
    return xml_output


if __name__ == '__main__':
    test_input = """
    S -> baAB "|" baB "|" ba "|" baA newline
    A -> bAB "|" bA "|" bB "|" b newline
    B -> BAa "|" Aa "|" Ba "|" a "|" bAB "|" bA "|" bB "|" b   
    """
    main()

