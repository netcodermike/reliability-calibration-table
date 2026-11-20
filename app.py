from math import fsum


def analyze(data):
    size, entries = data["bins"], data["predictions"]
    if type(size) is not int or not 1 <= size <= 100 or not isinstance(entries, list) or not entries:
        raise ValueError("Provide 1 to 100 bins and at least one prediction")
    groups = [[] for _ in range(size)]
    for probability, outcome in entries:
        if type(probability) not in (int, float) or not 0 <= probability <= 1 or type(outcome) is not int or outcome not in (0, 1):
            raise ValueError("Use probabilities in [0, 1] and integer labels 0 or 1")
        groups[min(size - 1, int(probability * size))].append((probability, outcome))
    bins = []
    for i, values in enumerate(groups):
        if values:
            mean = fsum(p for p, _ in values) / len(values)
            actual = sum(y for _, y in values) / len(values)
            bins.append(dict(lower=i/size, upper=(i+1)/size, count=len(values), mean=mean, actual=actual))
    ece = fsum(item["count"] * abs(item["mean"] - item["actual"]) for item in bins) / len(entries)
    brier = fsum((p-y)**2 for p, y in entries) / len(entries)
    return {"brier": round(brier, 8), "ece": round(ece, 8), "bins": bins}

if __name__ == "__main__":
    import json
    from pathlib import Path
    import sys
    try:
        path, = sys.argv[1:]
        result = analyze(json.loads(Path(path).read_text(encoding="utf-8")))
        print(json.dumps(result, ensure_ascii=True, allow_nan=False))
    except (OSError, ValueError, TypeError, KeyError, AttributeError, OverflowError) as error:
        print(f"Invalid input: {error}", file=sys.stderr)
        sys.exit(2)
