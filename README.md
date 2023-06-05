# digits-game-solver

A solver for the NY Times daily math puzzle game [Digits](https://www.nytimes.com/games/digits), currently in beta at time of writing.

Let's say we want to try to compute 69 using the numbers 1, 3, 4, 5, 10 and 25:

```
% ./digits-game-solver.py 69 1 3 4 5 10 25
(- (* 10 (+ 5 4)) (- 25 (+ 3 1)))
(+ (- (* 10 (+ 5 4)) 25) (+ 3 1))
(- (+ (* 10 (+ 5 4)) (+ 3 1)) 25)
... 2000+ more solutions omitted ...
(- (- (* (- 25 10) 5) 4) (- 3 1))
(- (+ (- (* (- 25 10) 5) 4) 1) 3)
(+ (- (- (* (- 25 10) 5) 4) 3) 1)

Shortest is: (- (* 10 (+ 4 3)) 1)
```

Works pretty fast but for some reason lists the same solution multiple times:

```
% ./digits-game-solver.py 69 1 3 4 5 10 25 | wc -l
    2463

% ./digits-game-solver.py 69 1 3 4 5 10 25 | sort | uniq | wc -l
     972
```

Recursion is hard. 🤷
