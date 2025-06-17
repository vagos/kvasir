#!/usr/bin/env python3

import dspy
import sys
import argparse
from kvasir.utils import get_code_block
from kvasir.program import Program


lm = dspy.LM('openai/gpt-4o-mini')

def main():
    parser = argparse.ArgumentParser(description="Perform task naively using an LLM.")
    parser.add_argument('program', type=str, help='The source code of the program to analyze.')
    parser.add_argument('task', type=str, help='The task to perform on the program.')
    args = parser.parse_args()

    print(f"Performing task: {args.task} on program: {args.program}", file=sys.stderr)
    program = Program(args.program)

    prompt = f"""{args.task}
    Program:
    {program.src}
    
    Please return the program's source code after performing the task.
    """

    output = "\n".join(lm(prompt))
    output = get_code_block(output)

    print(output)

if __name__ == "__main__":
    main()
