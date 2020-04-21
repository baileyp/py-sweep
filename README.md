# Minesweeper

This project is a console implementation of the classic game
[Minesweeper](https://en.wikipedia.org/wiki/Minesweeper_\(video_game\))
as recommended by
[Triplebyte's interview guide](https://triplebyte.com/candidates/interview_guide).

## Running

Just clone the repo and execute the `minesweeper` module

```bash
$ python -m minesweeper
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
- Add bomb flagging
- Add bomb count
- Add timer
- Add UI colors
- Get fancy! Maybe some context managers or decorators