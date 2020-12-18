from utils import read_from_file, d_print


operations = {
    '+': lambda v1, v2: v1 + v2,
    '*': lambda v1, v2: v1 * v2,
}


class Value():
    def __init__(self, value_str):
        self.value = int(value_str)

    def get_value(self):
        return self.value


class Expression():
    def __init__(self, expressions):
        self.expressions = expressions

    def __repr__(self):
        return "EX<{}>".format(self.expressions)

    def get_value(self):
        pass

    @classmethod
    def from_string(cls, expr_str):
        expressions = []
        i = 0
        while i < len(expr_str):
            if '(' == expr_str[i]:
                parens = 1
                current = ''
                while parens > 0:
                    i += 1
                    if expr_str[i] == ')':
                        parens -= 1
                        if parens == 0:
                            break
                    elif expr_str[i] == '(':
                        parens += 1
                    current += expr_str[i]
                expressions.append(Expression.from_string(current))
            elif ' ' == expr_str[i]:
                pass
            elif expr_str[i] in operations:
                expressions.append(operations[expr_str[i]])
            else:
                # There are no double digit numbers so we don't have to worry about assembly 
                expressions.append(int(expr_str[i]))
            i += 1
        return Expression(expressions)

    def solve(self, expressions=None, solve_strat='the-default'):
        expressions = expressions or self.expressions
        rhs, lhs, operator = None, None, None
        for e in expressions:
            if not rhs:
                rhs = e
            elif not operator:
                operator = e
            elif not lhs:
                lhs = e

            if rhs is not None and lhs is not None:
                if isinstance(lhs, Expression):
                    solve_fn = getattr(lhs, solve_strat) or lhs.solve
                    lhs = solve_fn()
                if isinstance(rhs, Expression):
                    solve_fn = getattr(rhs, solve_strat) or rhs.solve
                    rhs = solve_fn()
                rhs = operator(rhs, lhs)
                operator, lhs = None, None
        return rhs

    def solve_2(self):
        mult_expressions = []
        rhs, lhs, operator = None, None, None
        plus_operator = operations['+']
        while plus_operator in self.expressions:
            index = self.expressions.index(plus_operator)
            lhs = self.expressions[index - 1]
            rhs = self.expressions[index + 1]

            if isinstance(lhs, Expression):
                lhs = lhs.solve_2()
            if isinstance(rhs, Expression):
                rhs = rhs.solve_2()
            self.expressions = self.expressions[:index-1] +  [plus_operator(lhs, rhs)] + self.expressions[index+2:]
            d_print(self.expressions)
        return self.solve(solve_strat='solve_2')


def format_input(lines):
    expressions = []
    for line in lines:
        if not line:
            continue
        expressions.append(Expression.from_string(line))
    return expressions


def solve_1(filename):
    expressions = format_input(read_from_file(filename))
    return sum([expression.solve() for expression in expressions])


def solve_2(filename):
    expressions = format_input(read_from_file(filename))
    return sum([expression.solve_2() for expression in expressions])





