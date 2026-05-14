#!/usr/bin/env python3
"""Parse CMPE 260 and CMPE 256 Top 100 question files into JSON."""
import re
import json
import sys

def parse_questions(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Split by question headers (### Q\d+)
    # Pattern: ### Q<number>. <title/question>
    parts = re.split(r'(?=^### Q\d+\.)', content, flags=re.MULTILINE)
    
    questions = []
    current_tier = ""
    
    for part in parts:
        # Check for tier headers in the content before this question
        tier_match = re.search(r'## [🔴🟡🟢🔵] (Tier \d+[^*\n]*)', part)
        if tier_match:
            current_tier = tier_match.group(1).strip()
        
        # Match question header
        q_match = re.match(r'^### Q(\d+)\.\s*(.*?)$', part, re.MULTILINE)
        if not q_match:
            continue
        
        q_num = int(q_match.group(1))
        q_title = q_match.group(2).strip()
        
        # Get the rest after the header line
        rest = part[q_match.end():]
        
        # Extract options (- A) ... - B) ... - C) ... - D) ...)
        options = {}
        for letter in ['A', 'B', 'C', 'D']:
            opt_match = re.search(rf'^- {letter}\)\s*(.*?)$', rest, re.MULTILINE)
            if opt_match:
                options[letter] = opt_match.group(1).strip()
        
        if len(options) != 4:
            print(f"WARNING: Q{q_num} has {len(options)} options: {list(options.keys())}", file=sys.stderr)
            continue
        
        # Extract answer - handle both "Answer: C" and "Answer: B) 0.64" formats
        answer_match = re.search(r'\*\*Answer:\s*([A-D])\)?(?:\s*\)?\s*.*?)?\*\*', rest)
        if not answer_match:
            print(f"WARNING: Q{q_num} has no answer match", file=sys.stderr)
            # Try alternate pattern
            answer_match = re.search(r'\*\*Answer:\s*([A-D])', rest)
            if not answer_match:
                print(f"ERROR: Q{q_num} truly has no answer", file=sys.stderr)
                continue
        
        answer = answer_match.group(1)
        
        # Extract explanation
        expl_match = re.search(r'\*\*Explanation:\*\*\s*(.*?)(?:\n---|\n###|\Z)', rest, re.DOTALL)
        explanation = expl_match.group(1).strip() if expl_match else ""
        
        # The question text: everything between the header and the first option
        # Find where options start
        first_opt = re.search(r'^- A\)', rest, re.MULTILINE)
        if first_opt:
            question_text = rest[:first_opt.start()].strip()
        else:
            question_text = ""
        
        # If question_text is empty, use the title as the question
        if not question_text:
            question_text = q_title
        else:
            # Combine title and any additional text
            if question_text and q_title:
                question_text = q_title + "\n" + question_text
            elif q_title:
                question_text = q_title
        
        # Determine tier from question number
        if q_num <= 30:
            tier = "Tier 1 — Highest Probability"
        elif q_num <= 55:
            tier = "Tier 2 — High Probability"
        elif q_num <= 80:
            tier = "Tier 3 — Moderate-High"
        else:
            tier = "Tier 4 — Moderate"
        
        questions.append({
            "num": q_num,
            "question": question_text,
            "options": options,
            "answer": answer,
            "explanation": explanation,
            "tier": tier
        })
    
    return questions

if __name__ == "__main__":
    cmpe260 = parse_questions("plans/CMPE260_TOP100_Predicted_Exam_Questions.md")
    cmpe256 = parse_questions("plans/CMPE256_TOP100_Predicted_Exam_Questions.md")
    
    print(f"CMPE 260: {len(cmpe260)} questions parsed", file=sys.stderr)
    print(f"CMPE 256: {len(cmpe256)} questions parsed", file=sys.stderr)
    
    # Output as JSON
    result = {
        "cmpe260": cmpe260,
        "cmpe256": cmpe256
    }
    
    print(json.dumps(result, indent=2))
