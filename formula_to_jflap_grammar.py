import click
import re
import os


__doc__ = """
Convert a libre office forumla into an XML .jff file accepted by JFLAP
uses \"|\" (literal: "|") as separator. and literal: newline as newline
separator. Removes all whitespace (" "). Uses literal -> as production rule
symbol.
"""

RHS_DIVIDER = '"|"'  # == "\"|\""
NEWLINE = "newline"

@click.command()
@click.argument("formula_text")
@click.option("output_path", help="Include full file path to file with .jff "
                                  "file is created within script",
              default=os.path.join(os.getcwd(), "grammar.jff"))
def main(formula_text, output_path):
    with open(output_path, 'w') as f:
        f.write(convert(formula_text))


def convert(formula_text):
    re.sub(" ", "", formula_text)
    xml_output = """
        <?xml version="1.0" encoding="UTF-8" standalone="no"?>
        <!--Created with JFLAP 6.4.--><structure>
        <type>grammar</type>
        <!--The list of productions.-->"""

    for rule in formula_text.split("newline"):
        xml_output += "<production>"
        variable = ""
        # determine the variable of the rule
        for index, letter in enumerate(rule, start=0):
            # if production rule arrow encountered,
            # and the '-' char is not last character of rule
            if letter == '-' and len(letter) - 1 != index \
                    and letter[index+1] == ">":
                index += 2
                break
            variable += letter

        rule_done = False
        # determine the right hand side of the rule
        # for index2, letter in enumerate(rule[index:], start=index):
        for right_element in rule[index:].split(RHS_DIVIDER):
            right_output = ""
            for index2, letter in enumerate(right_element, start=0):
                if right_element[index2:] == NEWLINE:
                    rule_done = True
                    break
                right_output += letter

            if rule_done:
                break

            xml_output += "<left>{}</left>".format(variable)
            xml_output += "<right>{}</right>".format(right_output)

        xml_output += "</production"

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

