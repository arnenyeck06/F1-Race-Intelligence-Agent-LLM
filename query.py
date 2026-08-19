"""
query.py — Ask F1 questions from the command line.

Usage:
  python query.py "who won the Monaco Grand Prix 2024?"
  python query.py "what were the fastest laps at Silverstone 2024?"
  python query.py "how many pit stops did Ferrari make in Bahrain 2024?"
"""

import argparse
import os
import sys
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(__file__))

from agent.rag import run_agent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="F1 question")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    result = run_agent(args.query, verbose=args.verbose)

    print("\n" + "=" * 60)
    print("ANSWER")
    print("=" * 60)
    print(result["answer"])
    print(f"\n[tokens] in={result['input_tokens']} out={result['output_tokens']}")


if __name__ == "__main__":
    main()
