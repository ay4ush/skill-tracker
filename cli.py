import argparse
import sys
import os
from skills import SkillManager, VALID_STAGES

# Enable ANSI colors in Windows terminal (works in most vt100 emulators)
os.system("")

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_success(msg):
    print(f"{Colors.OKGREEN}{msg}{Colors.ENDC}")

def print_error(msg):
    print(f"{Colors.FAIL}{msg}{Colors.ENDC}")

def print_info(msg):
    print(f"{Colors.OKCYAN}{msg}{Colors.ENDC}")

def format_skill(skill):
    output = f"{Colors.HEADER}{Colors.BOLD}{skill['name']}{Colors.ENDC} "
    output += f"[{Colors.OKBLUE}{skill['stage']}{Colors.ENDC}]\n"
    if skill.get('tags'):
        output += f"  Tags: {', '.join(skill['tags'])}\n"
    if skill.get('notes'):
        output += f"  Notes: {skill['notes']}\n"
    if skill.get('comments'):
        output += "  Comments:\n"
        for c in skill['comments']:
            output += f"    - {c['timestamp']}: {c['text']}\n"
    output += f"  Last Updated: {skill['last_updated']}\n"
    return output

def create_parser():
    parser = argparse.ArgumentParser(
        description="Skill Tracker CLI - Track your personal skill development",
        epilog="Use `python main.py <command> --help` for specific command help."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add
    parser_add = subparsers.add_parser("add", help="Add a new skill")
    parser_add.add_argument("name", help="Name of the skill")
    parser_add.add_argument("--tags", nargs="*", help="Optional tags for the skill")

    # Move
    parser_move = subparsers.add_parser("move", help="Move a skill to a different stage")
    parser_move.add_argument("name", help="Name of the skill")
    parser_move.add_argument("stage", choices=VALID_STAGES, help=f"New stage ({', '.join(VALID_STAGES)})")

    # List
    parser_list = subparsers.add_parser("list", help="List skills")
    parser_list.add_argument("stage", nargs="?", choices=VALID_STAGES, help="Optional stage to filter by")

    # Note
    parser_note = subparsers.add_parser("note", help="Add or update a note for a skill")
    parser_note.add_argument("name", help="Name of the skill")
    parser_note.add_argument("text", help="Note text")

    # Comment
    parser_comment = subparsers.add_parser("comment", help="Add a timestamped comment to a skill")
    parser_comment.add_argument("name", help="Name of the skill")
    parser_comment.add_argument("text", help="Comment text")

    # View
    parser_view = subparsers.add_parser("view", help="View full details of a skill")
    parser_view.add_argument("name", help="Name of the skill")

    # Delete
    parser_delete = subparsers.add_parser("delete", help="Delete a skill")
    parser_delete.add_argument("name", help="Name of the skill")

    # Push
    parser_push = subparsers.add_parser("push", help="Push a skill forward by 1 stage")
    parser_push.add_argument("name", help="Name of the skill")

    # Interactive
    parser_interactive = subparsers.add_parser("interactive", help="Start interactive mode")
    
    return parser

def run_cli(args=None):
    parser = create_parser()
    parsed_args = parser.parse_args(args)

    if not parsed_args.command:
        parser.print_help()
        sys.exit(0)

    manager = SkillManager()

    try:
        if parsed_args.command == "add":
            skill = manager.add_skill(parsed_args.name, parsed_args.tags)
            print_success(f"Added skill '{skill['name']}' in stage '{skill['stage']}'")
            
        elif parsed_args.command == "move":
            skill = manager.move_skill(parsed_args.name, parsed_args.stage)
            print_success(f"Moved skill '{skill['name']}' to stage '{skill['stage']}'")
            
        elif parsed_args.command == "list":
            skills = manager.list_skills(parsed_args.stage)
            if not skills:
                print_info("No skills found.")
            else:
                for skill in skills.values():
                    print_info(f"{skill['name']} [{skill['stage']}]")
                    
        elif parsed_args.command == "note":
            manager.add_note(parsed_args.name, parsed_args.text)
            print_success(f"Updated note for '{parsed_args.name}'")
            
        elif parsed_args.command == "comment":
            manager.add_comment(parsed_args.name, parsed_args.text)
            print_success(f"Added comment to '{parsed_args.name}'")
            
        elif parsed_args.command == "view":
            skill = manager.view_skill(parsed_args.name)
            print(format_skill(skill))
            
        elif parsed_args.command == "delete":
            manager.delete_skill(parsed_args.name)
            print_success(f"Deleted skill '{parsed_args.name}'")

        elif parsed_args.command == "push":
            skill = manager.push_skill(parsed_args.name)
            print_success(f"Pushed skill '{skill['name']}' to stage '{skill['stage']}'")
            
        elif parsed_args.command == "interactive":
            import interactive
            interactive.run_interactive(manager)

    except ValueError as e:
        print_error(f"Error: {e}")
        # In interactive mode, we don't want to exit the entire process
        if args is not None:
             raise SystemExit(1)
        sys.exit(1)
