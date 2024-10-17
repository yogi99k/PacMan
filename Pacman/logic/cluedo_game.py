import cnf
import cluedo

def query(kb, player, card):
    if cnf.entails(kb,  cluedo.Cluedo.getIdentifierFromNames(player, card)): return 'Y'
    if cnf.entails(kb, -cluedo.Cluedo.getIdentifierFromNames(player, card)): return 'N'
    return '-'

def printNotepad(clauses):
    for player in cluedo.Cluedo.suspects:
        print('\t', player, end="")
    print('\t', cluedo.Cluedo.casefile)

    for card in cluedo.Cluedo.cards:
        print(card, '\t', end="")
        for player in cluedo.Cluedo.suspects:
            print(query(clauses, player, card), '\t', end="")
        print(query(clauses, cluedo.Cluedo.casefile, card))

def play_cluedo(output=True):
    clauses = cluedo.axiom_card_exists() + cluedo.axiom_card_unique() + cluedo.axiom_casefile_exists() + cluedo.axiom_casefile_unique()
    clauses.extend(cluedo.deal("sc", ["wh", "li", "st"]))
    if output:
        print('After deal: should show that the cards dealt to us are in our hand and only our hand.')
        printNotepad(clauses)
        print
    clauses.extend(cluedo.suggest("sc", "sc", "ro", "lo", "mu", "sc"))
    clauses.extend(cluedo.suggest("mu", "pe", "pi", "di", "pe", None))
    clauses.extend(cluedo.suggest("wh", "mu", "re", "ba", "pe", None))
    clauses.extend(cluedo.suggest("gr", "wh", "kn", "ba", "pl", None))
    clauses.extend(cluedo.suggest("pe", "gr", "cs", "di", "wh", None))
    clauses.extend(cluedo.suggest("pl", "wh", "wr", "st", "sc", "wh"))
    clauses.extend(cluedo.suggest("sc", "pl", "ro", "co", "mu", "pl"))
    clauses.extend(cluedo.suggest("mu", "pe", "ro", "ba", "wh", None))
    clauses.extend(cluedo.suggest("wh", "mu", "cs", "st", "gr", None))
    clauses.extend(cluedo.suggest("gr", "pe", "kn", "di", "pe", None))
    clauses.extend(cluedo.suggest("pe", "mu", "pi", "di", "pl", None))
    clauses.extend(cluedo.suggest("pl", "gr", "kn", "co", "wh", None))
    clauses.extend(cluedo.suggest("sc", "pe", "kn", "lo", "mu", "lo"))
    clauses.extend(cluedo.suggest("mu", "pe", "kn", "di", "wh", None))
    clauses.extend(cluedo.suggest("wh", "pe", "wr", "ha", "gr", None))
    clauses.extend(cluedo.suggest("gr", "wh", "pi", "co", "pl", None))
    clauses.extend(cluedo.suggest("pe", "sc", "pi", "ha", "mu", None))
    clauses.extend(cluedo.suggest("pl", "pe", "pi", "ba", None, None))
    clauses.extend(cluedo.suggest("sc", "wh", "pi", "ha", "pe", "ha"))
    clauses.extend(cluedo.suggest("wh", "pe", "pi", "ha", "pe", None))
    clauses.extend(cluedo.suggest("pe", "pe", "pi", "ha", None, None))
    clauses.extend(cluedo.suggest("sc", "gr", "pi", "st", "wh", "gr"))
    clauses.extend(cluedo.suggest("mu", "pe", "pi", "ba", "pl", None))
    clauses.extend(cluedo.suggest("wh", "pe", "pi", "st", "sc", "st"))
    clauses.extend(cluedo.suggest("gr", "wh", "pi", "st", "sc", "wh"))
    clauses.extend(cluedo.suggest("pe", "wh", "pi", "st", "sc", "wh"))
    clauses.extend(cluedo.suggest("pl", "pe", "pi", "ki", "gr", None))
    if output:
        print('Before accusation: should show a single solution.')
        printNotepad(clauses)
        print("")
    clauses.extend(cluedo.accuse("sc", "pe", "pi", "bi", True))
    if output:
        print('After accusation: if consistent, output should remain unchanged.')
        printNotepad(clauses)
        print("")
        print('Contents of the case file: %s' % [card for card in cluedo.Cluedo.cards if query(clauses, cluedo.Cluedo.casefile, card) == 'Y'])
    return [card for card in cluedo.Cluedo.cards if query(clauses, cluedo.Cluedo.casefile, card) == 'Y']

if __name__ == "__main__":
    play_cluedo()
