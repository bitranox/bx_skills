import re

def parse_candidates(candidate_file):
    """Parse cache candidates file."""
    with open(candidate_file) as f:
        content = f.read()

    pattern = r'([^\n:]+):(\d+) - (\w+)\(\)'
    matches = re.findall(pattern, content)

    return [{'file': m[0], 'line': int(m[1]), 'function': m[2]} for m in matches]

def parse_hotspots(hotspot_file):
    """Parse hotspots file."""
    with open(hotspot_file) as f:
        content = f.read()

    pattern = r'([^\n:]+):(\d+) - (\w+)\(\)'
    matches = re.findall(pattern, content)

    return [{'file': m[0], 'line': int(m[1]), 'function': m[2]} for m in matches]

def prioritize(candidates, hotspots):
    """Find candidates that are also hot spots (HIGH PRIORITY)."""
    priority = []

    for candidate in candidates:
        for hotspot in hotspots:
            if (candidate['function'] == hotspot['function'] and
                candidate['file'].endswith(hotspot['file'].split('/')[-1])):
                priority.append(candidate)
                break

    return priority

if __name__ == '__main__':
    candidates = parse_candidates('LLM-CONTEXT/review-anal/cache/cache_candidates.txt')
    hotspots = parse_hotspots('LLM-CONTEXT/review-anal/cache/hotspots.txt')

    priority = prioritize(candidates, hotspots)

    print("# High-Priority Cache Candidates\n")
    print("These functions are BOTH pure AND frequently called:\n")

    for p in priority:
        print(f"**{p['file']}:{p['line']} - {p['function']}()**")
        print("  Action: Profile with caching to measure benefit\n")

    print(f"\nTotal high-priority candidates: {len(priority)}")
