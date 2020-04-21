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
a practice exercise I wanted to keep this pure python.

I'm not great at making console applications and am even less experienced at dealing with game loops. I don't feel great
about the use of Exceptions to manage game termination but it works for now. I'm definitely unhappy with most of the
rendering so I expect to overhaul that at some point.

Overall I'm pleased with the implementation for a few hours work.

## TODO

- Admin: Unit tests
- Admin: Doc strings
- ~~Feature: Add victory condition~~
- Feature: Add snake flagging
- Feature: Add snake count
- Feature: Add timer
- Feature: Add UI colors
- Refactor: Uncouple rendering from state
- Refactor: Get fancy! Maybe some context managers or decorators