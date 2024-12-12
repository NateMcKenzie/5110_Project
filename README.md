# Running the program

```
usage: Evacuation Simulator [-h] [-f] [-q] [level_file] [output_dir]

Watch how cooperative or not people are in evacuations

positional arguments:
  level_file   Level file to use
  output_dir   Directory where output files will be saved

options:
  -h, --help   show this help message and exit
  -f, --fancy  Enable fancy renderer
  -q, --quiet  Disable rendering (precedence over -f)
```

example command:
`python main.py -f levels/funnel5050.lvl funnel5050_output`

# Fancy Rendering
If using FancyRender to render, you need to have curses. On Linux, you probably have it. On Windows, you will need to
get one somehow. Easiest solution: `pip install windows-curses`

# Level Files
The level files that we've provided show examples and have a brief description of how they work. The top line will be
ignored (simple parser assumes there's a comment there). The next 3 lines have space seperated numbers describing:
```
width height
agent_count round_count
cooperation_rate
```
After that, level data is provided in the same format as the basic renderer would show it, wihtout any agents.

# Generate.sh
It may not work on all systems, but I wanted to be able to quickly generate plots for all available level files.
`generate.sh` does this, simply run it and let it work.
