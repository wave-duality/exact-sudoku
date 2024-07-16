# Introduction
## General Question
For what positive integers $k$ is it possible to generate a sudoku board with precisely $k$ valid solutions? By _sudoku board_, we mean a 9 by 9 array where every entry is either an integer between 1 and 9 or empty. By a _solution_, we mean some assignment of every empty entry in the given sudoku board to an integer that remains consistent with Sudoku rules. We will also say that a sudoku board is a _k-sudoku_ if it has exactly $k$ valid solutions. The classical Sudoku puzzles online typically have a unique solution, so we say that they are _1-sudokus._

## Rules
The rules of Sudoku are well-understood, but we will formalize them here.

1. Every cell must contain exactly one integer, from 1 to 9 (inclusive).
2. Every row must contain each integer from 1 to 9 exactly once.
3. Every column must contain each integer from 1 to 9 exactly once.
4. Every 3 by 3 subgrid must contain each integer from 1 to 9 exactly once. **Subgrids refer to the 9 mutually-exclusive 3 by 3 sections on a Sudoku board, not any contiguous subarray.**

This formalization leads nicely to our methodology.

## Format
All Sudoku boards/solutions are given in 81-character format, where the cells are read by row, from left to right, and then top to bottom. Blank cells are represented with the '.' character.

# Methodology
While Sudoku is NP-Complete (essentially a special case of a Latin Square), some methods are more efficient than others. For this project, we count the number of valid solutions for an arbitrary sudoku board using two steps:

1. Turn the Sudoku puzzle into an exact cover problem.
2. Solve the exact cover problem with Knuth's Algorithm X (Dancing Links).

There are plenty of resources online that explain Step #2, so we will focus here on Step #1. The _exact cover_ problem takes in a binary, two-dimensional matrix, in which the goal is to find an _exact covering set_, or a subset of rows such that each column contains exactly one "1" among these rows. In the context of games, particularly constraint satisfaction problems like Sudoku, one can think broadly of the columns as "constraints" and the rows as "choices." Recall that we listed 4 rules for Sudoku, which are all the necessary rules we need to check whether or not a solution is valid. Hence, consider the following:

1. Our binary matrix will have $9 \cdot 9 \cdot 9 = 729$ rows, since there are $9 \cdot 9$ cells and $9$ choices for each cell. You can think of a particular row as the **choice** of putting a particular number in a particular cell.
2. Our binary matrix will have $9 \cdot 9 \cdot 4 = 324$ columns. There are $9 \cdot 9$ constraints for Rule #1 (each constraint being that a cell must contain a number), $9 \cdot 9$ constraints for Rule #2 (Row 1 must contain a "1", Row 1 must contain a "2", Row 1 must contain a "3", ..., Row 9 must contain a "9"), and so on.
3. Every row will have exactly four "1" entries, since every choice satisfies exactly one constraint in each of the rules. For instance, filling in a "8" in the 6th row and 7th column will satisfy the constraint of having a number in cell $(6, 7),$ having a "8" in Row 6, having a "8" in Row 7, and having a "8" in the 6th subgrid (if you count left to right, then top to bottom).

With this, we have essentially abstractified any Sudoku puzzle into a $729$ by $324$ binary matrix, in which there exists a one-to-one correspondence between exact covering sets and Sudoku solutions. Now, we just apply Knuth's Algorithm X to count the number of covering sets, which gives us the number of valid solutions!

# Results
The goal of this project was to exhibit $k$-sudoku example for $1 \leq k \leq 1000,$ just for fun. To do this, we randomly generated a solved Sudoku board, then removed numbers with a certain probability. The most effective range appeared to be removing between $35$ and $55$ givens.

# Open Questions
What's the smallest $k$ such that no $k$-sudoku exists? What does the distribution of solutions look like if we remove $n$ random clues from a fully solved sudoku to create a puzzle? Is there a nice, mathematical way to prove that no $k$-sudoku exists for some $k$?

