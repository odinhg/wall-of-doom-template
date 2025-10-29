# Wall of Doom

Welcome to the never ending **Wall of Doom**!

> Trying is the first step to failing!

## The Basics

The active tasks are found in `WALL.md`

The format is as follows:

```
## Project Name 1 

Any content goes here (except `##` which indicates a new project).

- [ ] Item 1
- [x] (1) Item 2
- [x] (4) Item 3

## Project Name 2

> This is a description or notes about the project.

- [c] Item 1
- [ ] Item 2

```

There are five levels of priorities 1 to 5 where 1 is the highest. These are specified in parentheses before the task description. If no priotity is specified, it will be treated as priority 3.

## The Bot of Dooms

The following bots help you manage your Wall of Doom. They have their own GitHub workflows so you don't have to think about keeping your tidy. 

### Vacoom

Vacoom does two things and operates only on `WALL.md`:

1. Move done tasks to the bottom of each task list.
2. Sort every task list by priority.

Vacoom is run on every push.

### Archoov

Archoov is responisble for the archiving completed tasks from `WALL.md`. 

1. Create a timestamped copy of `WALL.md` at `./archive/WALL_YYYY_MM_DD_hh_mm_ss.md` with everything except incomplete tasks.
2. Remove all completed tasks from `WALL.md`.

Archoov is run every weekend.
