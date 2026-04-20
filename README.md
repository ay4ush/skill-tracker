# Skill Tracker CLI

A lightweight, local command-line tool to track your personal skill development across different stages.

## Features
- Track skills across stages: `TO_LEARN`, `LEARNING`, `PRACTICING`, `DONE`, `REVISE`
- Add notes and timestamped comments to skills
- Tag skills for organization
- Purely local JSON storage (`skills.json`)
- Interactive menu mode
- Colorized CLI output

## Requirements
- Python 3.6+
- No external dependencies

## Usage

### Getting Help
```bash
python main.py --help
python main.py add --help
```

### Basic Commands

**Add a skill:**
```bash
python main.py add "Docker" --tags devops containers
```

**Move a skill to a new stage:**
```bash
python main.py move "Docker" LEARNING
```

**Push a skill to the next stage:**
```bash
python main.py push "Docker"
```

**Add a note:**
```bash
python main.py note "Docker" "Need to read about multi-stage builds."
```

**Add a comment (timestamped log):**
```bash
python main.py comment "Docker" "Finished tutorial part 1."
```

**View skill details:**
```bash
python main.py view "Docker"
```

**List all skills:**
```bash
python main.py list
```

**List skills by stage:**
```bash
python main.py list LEARNING
```

**Delete a skill:**
```bash
python main.py delete "Docker"
```

### Interactive Mode
Launch an interactive shell to run commands continually without typing `python main.py` every time.
```bash
python main.py interactive
```
