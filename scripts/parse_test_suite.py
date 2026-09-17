import re
import json

with open('/tmp/user_prompt.txt') as f:
    text = f.read()

sections = re.split(r'\n(?=#+ [A-Z])', text)

test_cases = []

for s in sections:
    lines = s.strip().split('\n')
    sec_title = lines[0].strip('# ').strip()
    if sec_title.startswith('Final scoring'):
        continue

    # Extract all code blocks with placeholders
    code_blocks = []
    def save_block(m):
        code_blocks.append(m.group(1))
        return f"__CODE_BLOCK_{len(code_blocks)-1}__"
    
    masked_s = re.sub(r'```(?:text)?\n(.*?)\n```', save_block, s, flags=re.DOTALL)
    
    # Now find all numbered items in masked_s
    # Item starts with \n<number>.\n or \n<number>. <text>
    matches = re.finditer(r'(?:^|\n)([0-9]+)\.\s*(.*?)(?=\n[0-9]+\.|\Z)', masked_s, flags=re.DOTALL)
    for m in matches:
        num = int(m.group(1))
        raw_prompt = m.group(2).strip()
        
        # Restore code block if present
        cb_m = re.search(r'__CODE_BLOCK_([0-9]+)__', raw_prompt)
        if cb_m:
            idx = int(cb_m.group(1))
            prompt = code_blocks[idx].strip()
        else:
            # Inline backtick or text
            tick_m = re.search(r'`([^`]+)`', raw_prompt)
            if tick_m:
                prompt = tick_m.group(1).strip()
            else:
                prompt = raw_prompt.split('\n')[0].strip(' *`')
        
        test_cases.append({
            'section': sec_title,
            'number': num,
            'prompt': prompt
        })

print(f'Total accurately extracted test cases: {len(test_cases)}')
with open('dist_test/extracted_test_cases.json', 'w') as out:
    json.dump(test_cases, out, indent=2)
