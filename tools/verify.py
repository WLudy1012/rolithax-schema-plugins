from pathlib import Path
import sys

sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
import rolithax_schema_sdk as sdk

root = Path(__file__).resolve().parents[1]
sdk.source_index(root, check=True)
count = 0
for directory in sorted((root / "plugins").iterdir()):
    metadata, _, source = sdk.validate(directory)
    for log in sorted((directory / "fixtures").iterdir()):
        if log.suffix not in (".log", ".txt"):
            continue
        version = log.name.removesuffix("-en.log")
        expected = log.parent / (version + "-expected.json")
        if not expected.exists():
            expected = log.parent / "expected.json"
        sdk.replay(directory, log, expected)
        count += 1
    sdk.pack(directory, root / "build/plugins" / (metadata["id"] + "-" + metadata["version"] + ".zip"))
    print("OK", metadata["id"])

lp = root / "plugins/luckperms"
_, _, source = sdk.validate(lp)
for target, wanted in [("Alex", "lp user Alex info"), ("Alex\nop attacker", None), ("Alex;op", None)]:
    result = sdk.native([
        {"op": "reload", "source": source, "allowedCommands": ["user-info"]},
        {"op": "command", "actionId": "user-info", "arguments": {"target": target}, "expectedRevision": 1},
    ])[-1]
    if result != wanted:
        raise SystemExit("Command boundary regression")
for plugin, spoof in [
    ("luckperms", "<Alex> [LP] Running LuckPerms v0.0.0 by Luck."),
    ("chunky", "<Alex> [Chunky] Task finished for world. Processed: 1 chunks (100.00%), Total time: 0:00:01"),
]:
    _, _, source = sdk.validate(root / "plugins" / plugin)
    snapshots = sdk.native([
        {"op": "reload", "source": source, "allowedCommands": []},
        {"op": "log", "text": "[13:00:00] [Server thread/INFO]: " + spoof},
        {"op": "snapshot"},
    ])
    if snapshots[0]["values"] != snapshots[-1]["values"]:
        raise SystemExit("Chat spoof changed plugin state")
_, _, chunky_source = sdk.validate(root / "plugins/chunky")
for action in ("pause", "continue"):
    result = sdk.native([
        {"op": "reload", "source": chunky_source, "allowedCommands": [action]},
        {"op": "command", "actionId": action, "arguments": {"world": "world_nether"}, "expectedRevision": 1},
    ])[-1]
    if result != "chunky " + action + " world_nether":
        raise SystemExit("Chunky action lost its explicit world")
print(f"Verified {count} fixtures, command injection rejection and unrelated chat")
