import sys
import shlex
from cli import print_success, print_error, print_info, create_parser

def run_interactive(manager):
    print_info("Welcome to Skill Tracker Interactive Mode!")
    print_info("Type 'help' for a list of commands or 'exit' to quit.\n")
    
    parser = create_parser()
    
    while True:
        try:
            cmd = input("skill-tracker> ").strip()
            if not cmd:
                continue
            
            if cmd in ['exit', 'quit']:
                print_info("Goodbye!")
                break
            
            if cmd in ['help', '?']:
                parser.print_help()
                continue
            
            try:
                args = shlex.split(cmd)
            except ValueError as e:
                print_error(f"Error parsing command: {e}")
                continue
            
            if args[0] == "interactive":
                print_error("Already in interactive mode!")
                continue

            try:
                from cli import run_cli
                run_cli(args)
            except SystemExit:
                # Catch SystemExit to prevent argparse from killing the interactive shell
                pass
                
        except (KeyboardInterrupt, EOFError):
            print_info("\nGoodbye!")
            break
