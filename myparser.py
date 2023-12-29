import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP

NP -> Det N | AP NP | N PP | NP PP | Adj NP | Det Adj N | Det Adj NP | NP Conj S | N | NP VP PP | S

VP -> V NP PP | VP PP | VP NP | V NP | V Det NP | V | VP Conj S | Adv VP | VP Adv | VP Conj S | VP Conj VP

PP -> P NP

"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """

    sentence_l = nltk.tokenize.word_tokenize(sentence)
    new_sentence = []
    for item in sentence_l:
        a = False
        for i in item:
            if i.isalpha():
                a = True
        if a:
            new_sentence.append(item.lower())
    #print(new_sentence)
    return new_sentence
        


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    """recurse = False
    NPs = []
    for subtree in tree.subtrees():
        if not contains_np_subtrees(subtree):
            NPs.append(subtree)
        else:
            recurse = True
            NPs.extend(np_chunk(subtree))
    if recurse == False:
        set(NPs)
        list(NPs)
        return NPs
    return []"""
    NPs = traverse(tree)
    return NPs


#def recursive_np_chunk(tree):
    
def traverse(tree):
    NPs = []
    for subtree in tree.subtrees(lambda t: t.label() == "NP"):
        lowest_NP = True
        i = 0
        for subsubtree in subtree.subtrees(lambda t: t.label() == "NP"):
            #print(subtree)
            #print(subsubtree)
            if subsubtree.label() == "NP" and i != 0:
                lowest_NP = False
            i += 1
        if lowest_NP == True:
            NPs.append(subtree)
    #print(NPs)
    return NPs


if __name__ == "__main__":
    main()
