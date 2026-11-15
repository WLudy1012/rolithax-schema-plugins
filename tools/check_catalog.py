import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import urllib.parse

root = Path(__file__).resolve().parents[1]
limits = {"plugin.json": 16384, "ui.xml": 65536, "rules.yaml": 65536}
readme = (root / "README.md").read_bytes()
assert len(readme) <= 262144, "README exceeds 256 KiB"
fences = re.findall(r"(?ms)^```rolithax-schema-repository[ \t]*\n(.*?)^```[ \t]*$", readme.decode("utf-8"))
assert len(fences) == 1, "Expected exactly one repository fence"


def unique(pairs):
    result = {}
    for key, value in pairs:
        assert key not in result, "Duplicate JSON key"
        result[key] = value
    return result


def relative(value):
    assert isinstance(value, str) and value, "Missing source path"
    assert not any(c in value for c in "\\:%?#"), "Unsafe source path"
    assert not any(ord(c) < 32 for c in value), "Control character in path"
    path = PurePosixPath(value)
    assert not path.is_absolute() and all(part not in ("", ".", "..") for part in value.split("/")), "Path traversal"
    target = root.joinpath(*path.parts)
    assert target.resolve().is_relative_to(root), "Path escapes repository"
    assert not target.is_symlink(), "Symbolic link in source"
    return target


document = json.loads(fences[0], object_pairs_hook=unique)
assert document["schemaVersion"] == 1 and document["id"] and document["name"], "Invalid repository metadata"
assert isinstance(document["plugins"], list) and len(document["plugins"]) <= 256, "Invalid plugin list"
seen = set()
for plugin in document["plugins"]:
    assert re.fullmatch(r"[a-z][a-z0-9-]*(?:\.[a-z][a-z0-9-]*)+", plugin["id"]), "Invalid plugin id"
    assert re.fullmatch(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)", plugin["version"]), "Invalid version"
    assert plugin["id"] not in seen and plugin["name"] and plugin["description"], "Duplicate or incomplete plugin"
    seen.add(plugin["id"])
    source = plugin["source"]
    if source["type"] == "files":
        assert plugin["engine"] == "yaml", "Lua requires prebuilt ZIP"
        assert len(source["files"]) == 3 and {entry["path"] for entry in source["files"]} == set(limits), "Invalid file set"
        directory = relative(source["path"])
        for entry in source["files"]:
            path = relative(source["path"] + "/" + entry["path"])
            data = path.read_bytes()
            assert len(data) <= limits[entry["path"]], "File exceeds limit"
            assert type(entry["size"]) is int and entry["size"] == len(data), f"Incorrect size: {path}"
            assert entry["sha256"] == hashlib.sha256(data).hexdigest(), f"Incorrect SHA-256: {path}"
        manifest = json.loads((directory / "plugin.json").read_text(encoding="utf-8"), object_pairs_hook=unique)
        assert all(manifest[key] == plugin[key] for key in ("id", "version", "engine")), "Manifest differs from catalogue"
        assert manifest["sdkVersion"] == 2, "Official plugins require Schema 2"
    else:
        assert source["type"] == "package" and plugin["engine"] in ("lua", "yaml"), "Invalid source type"
        url = urllib.parse.urlsplit(source["url"])
        assert url.scheme == "https" and url.hostname and not url.username and not url.password and not url.fragment, "Invalid package URL"
        assert re.fullmatch(r"[0-9a-f]{64}", source["sha256"]), "Invalid package digest"
        assert type(source["size"]) is int and 0 < source["size"] <= 524288, "Invalid ZIP size"
    print("OK", plugin["id"])
print(f"Verified metadata and local SHA-256 for {len(seen)} plugins")
