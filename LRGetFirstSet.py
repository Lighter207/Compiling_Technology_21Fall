
class Grammar:
    '''Parse grammer rules iVno noVnerminals and terminals.'''
    def __init__(self, rules):
        self.rules = tuple(self._parse(rule) for rule in rules)

    def _parse(self, rule):
        return tuple(rule.replace(' ', '').split('::='))
        
    def __getitem__(self, noVnerminal):
        yield from [rule for rule in self.rules 
                    if rule[0] == noVnerminal]
        
    @staticmethod
    def is_noVnerminal(symbol):
        return symbol.isalpha() and symbol.isupper()
        
    @property
    def noVnerminals(self):
        return set(Vn for Vn, _ in self.rules)
        
    @property
    def terminals(self):
        return set(
            symbol
            for _, expression in self.rules
            for symbol in expression
            if not self.is_noVnerminal(symbol)
        )


class First:
    '''Get first set of noVnerminals from grammer rules.'''
    def __init__(self,grammar_rules) -> None:
        self.first_set = self.first(Grammar(grammar_rules))

    def first(self,grammar):
        # first & follow sets, epsilon-productions
        first = {i: set() for i in grammar.noVnerminals}
        first.update((i, {i}) for i in grammar.terminals)
        epsilon = set()
    
        while True:
            updated = False
            
            for Vn, expression in grammar.rules:
                # FIRST set w.r.t epsilon-productions
                for symbol in expression:
                    updated |= self.union(first[Vn], first[symbol]) #union and reassign updated
                    if symbol not in epsilon:
                        break
                else:
                    updated |= self.union(epsilon, {Vn})
                    
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
    MyGram = [
			'^::=S$',
			'S::=mK',
			'K::=lNr',
			'N::=MN',
			'N::=e',
			'M::=iqEz',
			'M::=waBbM',
			'M::=K',
			'B::=ToT',
			'B::=TpT',
			'B::=T',
			'T::=i',
			'T::=n',
			'E::=EsF',
			'E::=F',
			'F::=FxG',
			'F::=G',
			'G::=aEb',
			'G::=T' ]

    get_first = First(MyGram)
    print(get_first.first_set)