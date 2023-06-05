#!/usr/bin/env python3

# 2023-05-26 - solver for the NYTimes game "Digits"

import itertools, operator
import sys

class Node:
    def __init__(self, value):
        self.value = value
        self.op = 'N/A'
        self.a = None
        self.b = None

    def __repr__(self):
        if self.op != 'N/A':
            return f"({self.op} {self.a} {self.b})"
        return str(self.value)

    def __eq__(self, other):
        if type(self) == type(other):
            return self.value == other.value
        return self.value == other

    def __le__(self, other):
        if type(self) == type(other):
            return self.value <= other.value
        return self.value <= other

def mk_node(op, a, b):
    f = op2func(op)
    c = f(a.value,b.value)
    n = Node(c)
    n.op = op
    n.a = a
    n.b = b
    return n

op_lookup = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}
operations = list(op_lookup.keys())


def main():
    target, choices = init()
    solve(target, choices)

def solve(target, choices):
    #print(f"Target: {target}")
    #print(choices)
    #solutions = chain_solver(target, choices)
    solutions = recursive_solver_outer(target, choices)
    shortest = "THIS IS LONGER THAN (- (* (* (- (+ 23 20) 13) 5) 3) 9)"
    for soln in solutions:
        s = str(soln)
        if len(s) < len(shortest):
            shortest = s
        print(s)
    print(f"\nShortest is: {shortest}")


def chain_solver(target, choices):
    # just randomly try all possible permutations
    solutions = []
    for perm in itertools.permutations(choices):
        for ops_tuple in itertools.combinations_with_replacement(operations, 5):
            ops = list(ops_tuple)
            log = []
            numbers = list(perm)
            while len(numbers) > 1:
                a = numbers.pop()
                b = numbers.pop()
                op = ops.pop()
                f = op2func(op)
                c = f(a,b)
                work = f"({a} {op} {b} = {c})"
                log.append(work)
                if c == target:
                    solutions.append(log)
                    break
                numbers.append(c)

    return solutions

def recursive_solver_outer(target, choices):
    pool = []
    for val in choices:
        n = Node(val)
        pool.append(n)
    return recursive_solver(target, pool)

def list_without(pool, i, j):
    """returns the elements from pool except for element i and element j"""
    result = []
    for idx, n in enumerate(pool):
        if idx == i or idx == j:
            continue
        result.append(n)
    #print(f"before: {pool}, after: {result}")
    return result

def recursive_solver(target, pool):
    if len(pool) == 0:
        return []
    if len(pool) == 1 and pool[0].value == target:
        return pool
    if len(pool) == 1 and pool[0].value != target:
        return []
    solutions = []
    for i, a in enumerate(pool):
        if a.value == 0:
            continue
        for j, b in enumerate(pool):
            if b.value == 0:
                continue
            if j == i:
                continue
            if a.value < b.value:
                continue
            for op in operations:
                if op == '/' and a.value % b.value != 0:
                    # only whole numbers
                    continue
                n = mk_node(op, a, b)
                if n.value == target:
                    return [n]
                else:
                    new_pool = list_without(pool, i, j)
                    if len(new_pool) == 0:
                        continue
                    new_pool.append(n)
                    solutions.extend(recursive_solver(target,new_pool))
    return solutions


def op2func(op):
    if op not in op_lookup:
        die("Unknown operator: '{op}'")
    return op_lookup[op]

def die(s):
    print(s)
    sys.exit(1)

def tests():
    #solve(67, [1,2,3,4,5,25])
    #solve(72, [1,2,3,4,5,10])
    #solve(73, [2,3,4,5,10])
    #solve(158, [2,3,5,7,9,11])
    solve(457, [3,7,9,13,20,25])

def usage():
    print(f"Usage: {sys.argv[0]} [target number] n1 n2 n3 n4 n5 n6")

def init():
    if len(sys.argv) < 8:
        usage()
        sys.exit(0)
    target = int(sys.argv[1])
    choices_str = sys.argv[2:]
    choices = [int(n) for n in choices_str]

    return (target, choices)


if __name__ == '__main__':
    main()
