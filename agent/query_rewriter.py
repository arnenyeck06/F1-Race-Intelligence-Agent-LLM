"""
query_rewriter.py
Rewrites user queries into better retrieval queries before search.
Runs without API calls — uses simple rule-based expansion for F1 domain.
Falls back to LLM rewriting when API is available.
"""

import re

F1_EXPANSIONS = {
    "won": "winner race result position 1",
    "fastest": "fastest lap time duration",
    "pit": "pit stop duration lap compound tyre",
    "tyre": "tyre compound soft medium hard pit stop",
    "tire": "tyre compound soft medium hard pit stop",
    "drs": "drag reduction system overtaking",
    "safety car": "safety car deployment lap restart",
    "podium": "top 3 positions winner race result",
    "qualifying": "qualifying grid position pole",
    "championship": "standings points drivers constructors",
}


def rewrite_query(query: str, use_llm: bool = False, client=None) -> str:
    """
    Rewrite a user query for better retrieval.
    
    Two strategies:
    1. Rule-based: expand F1 domain terms (always runs)
    2. LLM: rephrase into search-optimized form (runs when client provided)
    """
    # Rule-based expansion
    expanded = query.lower()
    added_terms = []
    for term, expansion in F1_EXPANSIONS.items():
        if term in expanded:
            added_terms.append(expansion)

    if added_terms:
        rewritten = f"{query} {' '.join(added_terms)}"
    else:
        rewritten = query

    # LLM rewriting (when credits available)
    if use_llm and client:
        try:
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=100,
                messages=[{
                    "role": "user",
                    "content": f"""Rewrite this F1 question as a search query with relevant keywords.
Return ONLY the rewritten query, no explanation.

Original: {query}
Rewritten:"""
                }]
            )
            llm_rewrite = response.content[0].text.strip()
            if llm_rewrite:
                return llm_rewrite
        except Exception:
            pass

    return rewritten


if __name__ == "__main__":
    tests = [
        "Who won Monaco?",
        "fastest lap at Silverstone",
        "Ferrari pit stop strategy",
        "what is DRS",
        "championship standings after Bahrain",
    ]
    for q in tests:
        print(f"Original:  {q}")
        print(f"Rewritten: {rewrite_query(q)}")
        print()
