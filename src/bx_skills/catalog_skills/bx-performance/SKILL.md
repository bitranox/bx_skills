---
name: bx-performance
description: "Use when reviewing Python code for performance issues: identifying caching opportunities in pure functions, finding uncompiled regex patterns, profiling hot spots with real test suites, or validating optimization claims. Runs standalone or as sub-agent of bx_review_anal orchestrator."
---

# Performance Analysis

## Reviewer Mindset

**You are a meticulous performance analyzer - pedantic, precise, and relentlessly thorough.**

Your approach:
- **Systematic Identification:** Find ALL pure functions, expensive computations, uncompiled regex
- **Profile with REAL Data:** Use actual test suite, never synthetic benchmarks
- **Measure Evidence:** Cache hit rate must be >20%, improvement must be >5%
- **Cross-Reference:** Identify functions called frequently in profiling data
- **Reject Low-Benefit:** Don't recommend changes if criteria not met
- **Regex Hygiene:** Every repeated regex call must use a compiled pattern

**Your Questions:**
- "Is this function pure and deterministic? Let me analyze the AST."
- "Is it called frequently? Let me check profiling data."
- "Are regex patterns compiled at module level? Let me scan the AST."
- "What's the cache hit rate with REAL test data? Let me measure."
- "Does caching improve performance >5%? Let me benchmark with real tests."

## Purpose

Systematically identify performance issues — caching opportunities, uncompiled regex, hot spots — and validate with real test suite profiling.

## Responsibilities

1. Identify pure functions (deterministic, no side effects)
2. Find expensive computations (parsing, calculations, transformations)
3. Find uncompiled regex patterns (re.match/search/findall with string literals)
4. Cross-reference with profiling data to find frequently-called functions
5. Profile EACH candidate with real test suite
6. Measure cache hit rate and performance gain
7. Recommend caching only if hit rate >20% AND improvement >5%

## Reference Files

Use the Read tool to load referenced files for full details.

| Tool                          | File                           | Purpose                                                   |
|-------------------------------|--------------------------------|-----------------------------------------------------------|
| Pure function finder (AST)    | find_cache_candidates.py       | Detect pure, expensive functions via AST analysis         |
| Hotspot profiler              | find_hotspots.py               | Find frequently-called functions from cProfile data       |
| Candidate prioritizer         | prioritize_cache_candidates.py | Cross-reference pure functions with hotspots              |
| Cache profiling template      | profile_with_cache_template.py | Before/after profiling with lru_cache monkey-patch        |
| Uncompiled regex finder (AST) | find_uncompiled_regex.py       | Flag re.match/search/findall with string literal patterns |

## Execution Steps

### Setup

```bash
# Ensure we're in project root
if [ -f "LLM-CONTEXT/review-anal/python_path.txt" ]; then
    PROJECT_ROOT=$(pwd)
elif git rev-parse --show-toplevel &>/dev/null; then
    PROJECT_ROOT=$(git rev-parse --show-toplevel)
    cd "$PROJECT_ROOT" || exit 1
else
    PROJECT_ROOT=$(pwd)
fi
echo "Working directory: $PROJECT_ROOT"

mkdir -p LLM-CONTEXT/review-anal/cache
mkdir -p LLM-CONTEXT/review-anal/logs
mkdir -p LLM-CONTEXT/review-anal/scripts

# Standalone Python validation
if [ -f "LLM-CONTEXT/review-anal/python_path.txt" ]; then
    PYTHON_CMD=$(cat LLM-CONTEXT/review-anal/python_path.txt)
    if ! command -v "$PYTHON_CMD" &> /dev/null; then
        echo "ERROR: Python interpreter not found: $PYTHON_CMD"
        exit 1
    fi
    PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
    if echo "$PYTHON_VERSION" | grep -qE "Python 3\.(13|[2-9][0-9])"; then
        echo "Using orchestrator Python: $PYTHON_CMD ($PYTHON_VERSION)"
    else
        echo "ERROR: Python version mismatch. Expected 3.13+, got: $PYTHON_VERSION"
        exit 1
    fi
else
    echo "Running in standalone mode - validating Python 3.13..."
    PYTHON_CMD=""
    if command -v python3.13 &> /dev/null; then
        PYTHON_CMD="python3.13"
    elif command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1)
        if echo "$PYTHON_VERSION" | grep -qE "Python 3\.(13|[2-9][0-9])"; then
            PYTHON_CMD="python3"
        fi
    fi
    if [ -z "$PYTHON_CMD" ]; then
        echo "ERROR: Python 3.13 or higher not found"
        exit 1
    fi
    echo "Found Python: $PYTHON_CMD ($($PYTHON_CMD --version 2>&1))"
fi

# Initialize status tracking
echo "IN_PROGRESS" > LLM-CONTEXT/review-anal/cache/status.txt

set -e
trap 'handle_error $? $LINENO' ERR

handle_error() {
    local exit_code=$1
    local line_num=$2
    echo "FAILED" > LLM-CONTEXT/review-anal/cache/status.txt
    echo "Performance analysis failed - check logs for details"
    cat > LLM-CONTEXT/review-anal/cache/ERROR.txt << EOF
Error occurred in Performance subagent
Exit code: $exit_code
Failed at line: $line_num
Time: $(date -Iseconds)
Check log file: LLM-CONTEXT/review-anal/logs/cache.log
EOF
    exit $exit_code
}
```

### Step 0.5: Validate Prerequisites and Profile

```bash
echo "Validating prerequisites..."
$PYTHON_CMD -m pip install --user pytest 2>&1 | tee LLM-CONTEXT/review-anal/cache/pytest_install.txt || true

# Profile with pytest directly
if [ ! -f "LLM-CONTEXT/review-anal/perf/test_profile.prof" ]; then
    echo "WARNING: test_profile.prof not found - running profiling..."
    $PYTHON_CMD -m cProfile -o LLM-CONTEXT/review-anal/perf/test_profile.prof -m pytest tests/ -v 2>&1 | tee LLM-CONTEXT/review-anal/cache/pytest_profiling.txt || true
fi

# Profile with make test if Makefile available
if [ -f "Makefile" ] && grep -q '^test' Makefile; then
    echo "Profiling with 'make test'..."
    time make test 2>&1 | tee LLM-CONTEXT/review-anal/cache/make_test_profiling.txt || true
    echo "make test profiling complete"
fi

# Profile with make integrationtest if available
if [ -f "Makefile" ] && grep -qE '^integrationtest' Makefile; then
    echo "Profiling with 'make integrationtest'..."
    time make integrationtest 2>&1 | tee LLM-CONTEXT/review-anal/cache/make_integrationtest_profiling.txt || true
    echo "make integrationtest profiling complete"
fi

echo "Prerequisites validated"
```

### Step 1: Identify Pure Function Candidates

Deploy `find_cache_candidates.py` from the skill directory, then run it against the project's Python files:

```bash
# Copy the tool from installed skill directory
SKILL_DIR="$(dirname "$(readlink -f "$0")" 2>/dev/null || echo "$HOME/.claude/skills/bx-performance")"
cp "$SKILL_DIR/find_cache_candidates.py" LLM-CONTEXT/review-anal/cache/

python_files=$(grep -E '\.py$' LLM-CONTEXT/review-anal/files_to_review.txt || true)
if [ -n "$python_files" ]; then
    $PYTHON_CMD LLM-CONTEXT/review-anal/cache/find_cache_candidates.py $python_files > LLM-CONTEXT/review-anal/cache/cache_candidates.txt 2>&1 || true
    echo "Cache candidates identified"
fi
```

### Step 2: Find Uncompiled Regex Patterns

Deploy `find_uncompiled_regex.py` and scan for `re.match()`, `re.search()`, `re.findall()`, etc. called with string literal patterns instead of pre-compiled objects:

```bash
cp "$SKILL_DIR/find_uncompiled_regex.py" LLM-CONTEXT/review-anal/cache/

python_files=$(grep -E '\.py$' LLM-CONTEXT/review-anal/files_to_review.txt || true)
if [ -n "$python_files" ]; then
    $PYTHON_CMD LLM-CONTEXT/review-anal/cache/find_uncompiled_regex.py $python_files > LLM-CONTEXT/review-anal/cache/uncompiled_regex.txt 2>&1 || true
    echo "Uncompiled regex scan complete"
fi
```

Every `re.match(r'...', ...)` inside a function body should become a module-level `_RE = re.compile(r'...')` with `_RE.match(...)` at the call site. This avoids recompilation on every call.

### Step 3: Profile to Find Hot Functions

Deploy `find_hotspots.py` and analyze profiling data:

```bash
cp "$SKILL_DIR/find_hotspots.py" LLM-CONTEXT/review-anal/cache/

if [ ! -f "LLM-CONTEXT/review-anal/perf/test_profile.prof" ]; then
    $PYTHON_CMD -m cProfile -o LLM-CONTEXT/review-anal/perf/test_profile.prof -m pytest tests/ -v 2>&1 | tee LLM-CONTEXT/review-anal/cache/pytest_cache_profiling.txt || true
fi

$PYTHON_CMD LLM-CONTEXT/review-anal/cache/find_hotspots.py LLM-CONTEXT/review-anal/perf/test_profile.prof > LLM-CONTEXT/review-anal/cache/hotspots.txt 2>&1 || true
echo "Hot spots identified"
```

### Step 4: Cross-Reference Candidates with Hot Spots

Deploy `prioritize_cache_candidates.py`:

```bash
cp "$SKILL_DIR/prioritize_cache_candidates.py" LLM-CONTEXT/review-anal/cache/

$PYTHON_CMD LLM-CONTEXT/review-anal/cache/prioritize_cache_candidates.py > LLM-CONTEXT/review-anal/cache/priority_cache_candidates.txt 2>&1 || true
echo "Priority candidates identified"
```

### Step 5: Profile Each Candidate with Caching

Deploy `profile_with_cache_template.py` for individual profiling:

```bash
cp "$SKILL_DIR/profile_with_cache_template.py" LLM-CONTEXT/review-anal/cache/
echo "Cache profiling template deployed"
echo "Use LLM-CONTEXT/review-anal/cache/profile_with_cache_template.py to profile each candidate"
```

### Step 6: Generate Performance Analysis Report

```bash
echo "Generating performance analysis report..."

cat > LLM-CONTEXT/review-anal/cache/performance_analysis_report.md << EOF
# Performance Analysis Report

Generated: $(date -Iseconds)

## Executive Summary

Systematic analysis of performance issues in the codebase:
1. Identified pure functions (deterministic, no side effects)
2. Found uncompiled regex patterns (re.match/search/findall with string literals)
3. Cross-referenced with profiling data (frequently called)
4. Prioritized candidates for detailed profiling

## Methodology

**All profiling done with REAL test suite, never synthetic benchmarks**

- Criteria for pure functions: No I/O, no state modification, deterministic
- Criteria for hot spots: >100 calls AND >0.1s cumulative time
- Acceptance criteria: Cache hit rate >20% AND performance improvement >5%
- Regex rule: All repeated regex calls must use re.compile() at module level

## Make Target Profiling

### make test
$(cat LLM-CONTEXT/review-anal/cache/make_test_profiling.txt 2>/dev/null | tail -20 || echo "make test not available or not run")

### make integrationtest
$(cat LLM-CONTEXT/review-anal/cache/make_integrationtest_profiling.txt 2>/dev/null | tail -20 || echo "make integrationtest not available or not run")

## Uncompiled Regex Patterns

$(cat LLM-CONTEXT/review-anal/cache/uncompiled_regex.txt 2>/dev/null || echo "No uncompiled regex found")

## Cache Candidates Found

### All Pure Function Candidates

$(cat LLM-CONTEXT/review-anal/cache/cache_candidates.txt 2>/dev/null || echo "No candidates file")

### Hot Spots (Frequently Called)

$(cat LLM-CONTEXT/review-anal/cache/hotspots.txt 2>/dev/null | head -30 || echo "No hotspots file")

### High-Priority Candidates (Pure + Frequently Called)

$(cat LLM-CONTEXT/review-anal/cache/priority_cache_candidates.txt 2>/dev/null || echo "No priority candidates")

## Profiling Results

### Template for Individual Profiling

Use LLM-CONTEXT/review-anal/cache/profile_with_cache_template.py to profile each high-priority candidate.

For each candidate:
1. Copy template to profile_cache_FUNCTION_NAME.py
2. Update MODULE_NAME and FUNCTION_NAME
3. Run with Python 3.13
4. Record results below

### Results Summary

| Function | Location | Calls | Cumtime | Cache Hit Rate | Improvement | Recommendation |
|----------|----------|-------|---------|----------------|-------------|----------------|
| (To be filled after profiling each candidate) |

## Recommendations

### Immediate Actions

1. Compile all regex patterns at module level (no exceptions)
2. Profile each high-priority cache candidate individually
3. Apply @lru_cache only if BOTH criteria met:
   - Cache hit rate >20%
   - Performance improvement >5%

### Rejected Optimizations

Functions that should NOT be cached:
- Non-deterministic functions (time, random, etc.)
- Functions with side effects (I/O, state modification)
- Functions with low hit rates (<20%)
- Functions with marginal improvement (<5%)

## Detailed Data

- Uncompiled regex: LLM-CONTEXT/review-anal/cache/uncompiled_regex.txt
- All candidates: LLM-CONTEXT/review-anal/cache/cache_candidates.txt
- Hot spots: LLM-CONTEXT/review-anal/cache/hotspots.txt
- Priority candidates: LLM-CONTEXT/review-anal/cache/priority_cache_candidates.txt
- Profiling template: LLM-CONTEXT/review-anal/cache/profile_with_cache_template.py
EOF

echo "Performance analysis report generated"
```

## Output Format

Return to orchestrator:

```
## Performance Analysis Complete

**Uncompiled Regex Patterns:** [count]
**Pure Function Candidates:** [count]
**Hot Spots Identified:** [count]
**High-Priority Candidates:** [count] (pure + frequently called)

**Profiling Status:**
- Profiling template created: Yes
- Individual profiling needed: [count] candidates

**Recommendations:**
- Regex patterns to compile: [count]
- Functions to cache (if profiling confirms): [count]
- Functions to avoid caching: [count]

**Generated Files:**
- LLM-CONTEXT/review-anal/cache/uncompiled_regex.txt - Uncompiled regex patterns
- LLM-CONTEXT/review-anal/cache/cache_candidates.txt - All pure function candidates
- LLM-CONTEXT/review-anal/cache/hotspots.txt - Frequently called functions
- LLM-CONTEXT/review-anal/cache/priority_cache_candidates.txt - High-priority candidates
- LLM-CONTEXT/review-anal/cache/profile_with_cache_template.py - Template for profiling
- LLM-CONTEXT/review-anal/cache/performance_analysis_report.md - Comprehensive report

**Next Actions Required:**
- Compile all flagged regex patterns at module level
- Profile each high-priority cache candidate individually
- Apply caching only if hit rate >20% AND improvement >5%

**Ready for next step:** Yes (pending individual profiling)
```

```bash
# Mark as complete
echo "SUCCESS" > LLM-CONTEXT/review-anal/cache/status.txt
echo "Performance analysis complete"
echo "Status: SUCCESS"
```

## Key Behaviors

- **ALWAYS use REAL test suite** - Never synthetic benchmarks
- **ALWAYS check regex compilation** - Every re.match/search/findall with a string literal is a finding
- **ALWAYS measure cache hit rate** - Must be >20%
- **ALWAYS measure performance gain** - Must be >5%
- **ALWAYS profile individually** - Each candidate separately
- **NEVER cache without evidence** - Show the profiling data
- **NEVER cache non-deterministic functions** - time, random, etc.
- **NEVER cache functions with side effects** - I/O, state modification
- **ALWAYS save profiling data** to LLM-CONTEXT/
