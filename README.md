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

## TODO

- Unit tests
- Doc strings
- ~~Add victory condition~~
- Add snake flagging
- Add snake count
- Add timer
- Add UI colors
- Uncouple rendering from state
- Get fancy! Maybe some context managers or decorators