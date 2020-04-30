# PySweep

There are ~~pythons~~ snakes in the grass!

This project is a console implementation of the classic game
[Minesweeper](https://en.wikipedia.org/wiki/Minesweeper_\(video_game\))
as recommended by
[Triplebyte's interview guide](https://triplebyte.com/candidates/interview_guide).

## Running

Just clone the repo and execute the `pysweep` module

```bash
$ python -m pysweep
```

The prompts will guide you from there.

### Tests

Tests are written with pytest. Install if not installed already and just run `pytest`

```bash
$ pip install -U pytest
$ pytest
```

## Programming Concepts/Patterns Used

[Anonymous Functions](https://en.wikipedia.org/wiki/Anonymous_function)
: Principally for customizing how user input is captured.

[Depth-First Search](https://en.wikipedia.org/wiki/Depth-first_search)
: For revealing contiguous sections of blank squares.

[Encapsulation](https://en.wikipedia.org/wiki/Encapsulation_\(computer_programming\))
: For state management of the gameboard and squares.

[Null Object Pattern](https://en.wikipedia.org/wiki/Null_object_pattern)
: For gracefully dealing with out of bounds squares.

## Thoughts

I know there are best in class packages available in the community to handle some of the things done here better, but as
a practice exercise I wanted to keep this pure python, save testing.

I'm not great at making console applications and am even less experienced at dealing with game loops. I don't feel great
about the use of Exceptions to manage game termination but it works for now. 

Now that I have some unit tests in place I feel like there are lots of improvements/refinements to be made there. More
to be done with pytest's fixtures, stubs, and spies.

Overall I'm pleased with the implementation for a few hours work.

## TODO

- ~~Admin: Unit tests~~
- Admin: Doc strings
- ~~Feature: Add victory condition~~
- ~~Feature: Add snake flagging~~
- ~~Feature: Add snake count~~
- ~~Feature: Add timer~~
- ~~Feature: Add UI colors~~
- Feature: Richer input options (Multiple row/column selection per command)
- ~~Refactor: Uncouple rendering from state~~
- Refactor: Get fancy! Maybe some context managers or decorators
- Refactor: Unit tests to make better use of built-in mocking

## Changelog

### 0.5.0

- Added UI colors
- Added game timer

### 0.4.0

- Updated rendering so playing larger boards is a bit easier

### 0.3.0

- Added snake flagging
- Added snake counter

### 0.2.0

- Rebranded game as PySweep

### 0.1.0

- Version playable version of game that is winnable
- No flagging
- No bomb counter