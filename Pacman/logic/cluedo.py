'''cluedo.py - project skeleton for a propositional reasoner
for the game of Clue.  Unimplemented portions have the comment "TO
BE IMPLEMENTED AS AN EXERCISE".  The reasoner does not include
knowledge of how many cards each player holds.
Originally by Todd Neller
Ported to Python by Dave Musicant
Adapted to course needs by Laura Brown

Copyright (C) 2008 Dave Musicant

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Information about the GNU General Public License is available online at:
  http://www.gnu.org/licenses/
To receive a copy of the GNU General Public License, write to the Free
Software Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
02111-1307, USA.'''

import cnf

class Cluedo:
    suspects = ['sc', 'mu', 'wh', 'gr', 'pe', 'pl']
    weapons  = ['kn', 'cs', 're', 'ro', 'pi', 'wr']
    rooms    = ['ha', 'lo', 'di', 'ki', 'ba', 'co', 'bi', 'li', 'st']
    casefile = "cf"
    hands    = suspects + [casefile]
    cards    = suspects + weapons + rooms

    """
    Return ID for player/card pair from player/card indicies
    """
    @staticmethod
    def getIdentifierFromIndicies(hand, card):
        return hand * len(Cluedo.cards) + card + 1

    """
    Return ID for player/card pair from player/card names
    """
    @staticmethod
    def getIdentifierFromNames(hand, card):
        return Cluedo.getIdentifierFromIndicies(Cluedo.hands.index(hand), Cluedo.cards.index(card))


# **************
#  Question 6 
# **************
def deal(hand, cards):
    "Construct the CNF clauses for the given cards being in the specified hand"
    "*** YOUR CODE HERE ***"
    clauses = []
    for card in cards:
        clauses.append([Cluedo.getIdentifierFromNames(hand, card)])
    return clauses
    return []


# **************
#  Question 7 
# **************
def axiom_card_exists():
    """
    Construct the CNF clauses which represents:
        'Each card is in at least one place'
    """
    "*** YOUR CODE HERE ***"
    clauses = []
    for card in Cluedo.cards:
        clause = [Cluedo.getIdentifierFromNames(hand, card) for hand in Cluedo.hands]
        clauses.append(clause)
    return clauses
    return []


# **************
#  Question 7 
# **************
def axiom_card_unique():
    """
    Construct the CNF clauses which represents:
        'If a card is in one place, it can not be in another place'
    """
    "*** YOUR CODE HERE ***"
    clauses = []
    for card in Cluedo.cards:
        for i in range(len(Cluedo.hands)):
            for j in range(i + 1, len(Cluedo.hands)):
                clauses.append([-Cluedo.getIdentifierFromIndicies(i, Cluedo.cards.index(card)),
                                -Cluedo.getIdentifierFromIndicies(j, Cluedo.cards.index(card))])
    return clauses
    return []


# **************
#  Question 7 
# **************
def axiom_casefile_exists():
    """
    Construct the CNF clauses which represents:
        'At least one card of each category is in the case file'
    """
    "*** YOUR CODE HERE ***"
    clauses = []
    for category in [Cluedo.suspects, Cluedo.weapons, Cluedo.rooms]:
        clause = [Cluedo.getIdentifierFromNames(Cluedo.casefile, card) for card in category]
        clauses.append(clause)
    return clauses
    return []


# **************
#  Question 7 
# **************
def axiom_casefile_unique():
    """
    Construct the CNF clauses which represents:
        'No two cards in each category are in the case file'
    """
    "*** YOUR CODE HERE ***"
    clauses = []
    for category in [Cluedo.suspects, Cluedo.weapons, Cluedo.rooms]:
        for i in range(len(category)):
            for j in range(i + 1, len(category)):
                clauses.append([-Cluedo.getIdentifierFromNames(Cluedo.casefile, category[i]),
                                -Cluedo.getIdentifierFromNames(Cluedo.casefile, category[j])])
    return clauses
    return []


# **************
#  Question 8 
# **************
def suggest(suggester, card1, card2, card3, refuter, cardShown):
    "Construct the CNF clauses representing facts and/or clauses learned from a suggestion"
    "*** YOUR CODE HERE ***"
    suggester_id = Cluedo.getIdentifierFromNames(suggester, suggester)
    card1_id = Cluedo.getIdentifierFromNames(suggester, card1)
    card2_id = Cluedo.getIdentifierFromNames(suggester, card2)
    card3_id = Cluedo.getIdentifierFromNames(suggester, card3)
    refuter_id = Cluedo.getIdentifierFromNames(refuter, refuter) if refuter else None
    cardShown_id = Cluedo.getIdentifierFromNames(refuter, cardShown) if cardShown else None
    knowledge =[]
    if cardShown:
        knowledge.append([cardShown_id])
        for player in Cluedo.hands[Cluedo.hands.index(suggester)+1:Cluedo.hands.index(refuter)]:
            knowledge.append([-Cluedo.getIdentifierFromNames(player, card1)])
            knowledge.append([-Cluedo.getIdentifierFromNames(player, card2)])
            knowledge.append([-Cluedo.getIdentifierFromNames(player, card3)])
    elif refuter and not cardShown:
        knowledge.append([Cluedo.getIdentifierFromNames(refuter, card1),
                                  Cluedo.getIdentifierFromNames(refuter, card2),
                                  Cluedo.getIdentifierFromNames(refuter, card3)])
        previous_player = Cluedo.hands.index(refuter)
        for player in Cluedo.hands[Cluedo.hands.index(suggester)+1:previous_player]:
            knowledge.append([-Cluedo.getIdentifierFromNames(player, card1)])
            knowledge.append([-Cluedo.getIdentifierFromNames(player, card2)])
            knowledge.append([-Cluedo.getIdentifierFromNames(player, card3)])
    else:
        for player in Cluedo.suspects:
            if player != suggester and player != cardShown:
                knowledge.append([-Cluedo.getIdentifierFromNames(player, card1)])
                knowledge.append([-Cluedo.getIdentifierFromNames(player, card2)])
                knowledge.append([-Cluedo.getIdentifierFromNames(player, card3)])
    is_satisfiable = cnf.satisfiable(knowledge)

    return knowledge
# **************
#  Question 9 
# **************
def accuse(accuser, card1, card2, card3, correct):
    "Construct the CNF clauses representing facts and/or clauses learned from an accusation"
    "*** YOUR CODE HERE ***"
    '''clauses = []
    if correct:
        # Accuser correctly accuses the cards
        accuser_clauses = [[Cluedo.getIdentifierFromNames(accuser, card)] for card in [card1, card2, card3]]
        clauses.extend(accuser_clauses)
    else:
        # Every other player has at least one of the accused cards
        for hand in Cluedo.hands:
            if hand != accuser:
                hand_clauses = [[-Cluedo.getIdentifierFromNames(hand, card)] for card in [card1, card2, card3]]
                clauses.extend(hand_clauses)
    return clauses'''
    clauses = []
    accuser_id = Cluedo.hands.index(accuser)
    card_ids = [Cluedo.cards.index(card1), Cluedo.cards.index(card2), Cluedo.cards.index(card3)]

    if correct:
        for card in card_ids:
            clauses.append([Cluedo.getIdentifierFromNames(Cluedo.casefile, Cluedo.cards[card])])
    else:
        clauses.append([-Cluedo.getIdentifierFromNames(Cluedo.casefile, Cluedo.cards[card]) for card in card_ids])
        for card in card_ids:
            clauses.append([-Cluedo.getIdentifierFromNames(Cluedo.hands[accuser_id], Cluedo.cards[card])])
    return clauses

    

