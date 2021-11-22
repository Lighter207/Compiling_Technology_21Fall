
class Grammar:
    '''Parse grammer rules into nonterminals and terminals.'''
    def __init__(self, rules):
        self.rules = tuple(self._parse(rule) for rule in rules)

    def _parse(self, rule):
        return tuple(rule.replace(' ', '').split('::='))
        
    def __getitem__(self, nonterminal):
        yield from [rule for rule in self.rules 
                    if rule[0] == nonterminal]
        
    @staticmethod
    def is_nonterminal(symbol):
        return symbol.isalpha() and symbol.isupper()
        
    @property
    def nonterminals(self):
        return set(nt for nt, _ in self.rules)
        
    @property
    def terminals(self):
        return set(
            symbol
            for _, expression in self.rules
            for symbol in expression
            if not self.is_nonterminal(symbol)
        )


class First:
    '''Get first set of nonterminals from grammer rules.'''
    def __init__(self,grammar_rules) -> None:
        self.first_set = self.first(Grammar(grammar_rules))

    def first(self,grammar):
        # first & follow sets, epsilon-productions
        first = {i: set() for i in grammar.nonterminals}
        first.update((i, {i}) for i in grammar.terminals)
        epsilon=set()
    
        while True:
            updated = False
            
            for nt, expression in grammar.rules:
                # FIRST set w.r.t epsilon-productions
                for symbol in expression:
                    updated |= self.union(first[nt], first[symbol])
                    if symbol not in epsilon:
                        break
                else:
                    updated |= self.union(epsilon, {nt})
                    
            if not updated:
                return first


    def union(self,first,begins):
        n = len(first)
        first |= begins
        return len(first) != n


if __name__ == "__main__":
    gram=[
			'^::=S$',
			'S::=aAd',
			'S::=bAc',
			'S::=aec',
			'S::=bed',
			'A::=e',
		]
    get_first = First(gram)
    print(get_first.first_set)