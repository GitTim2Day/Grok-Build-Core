"""fsguard.py -- list / read / write files ONLY inside the kit workspace dir.

Append and archive, never delete: there is no delete operation. Overwriting a file first
copies the old bytes to workspace/.archive/<relpath>.<timestamp> (that folder is read-only
through the API). Path guard (fail closed): relative paths only; no '..', no NUL, no
backslash or drive colon, no leading dot segments except reading .archive; the resolved
real path (symlinks followed) must stay under the real workspace root.
"""
from __future__ import annotations
import base64, os, re, shutil, time

MAX_READ = 2 * 2**20
MAX_WRITE = 2 * 2**20
MAX_LIST = 2000
ARCHIVE = ".archive"
_SEG_OK = re.compile(r"^[A-Za-z0-9 _.\-()+,]{1,128}$")


class GuardError(ValueError):
    def __init__(self, msg, status=400):
        super().__init__(msg)
        self.status = status


class Workspace:
    def __init__(self, root: str):
        os.makedirs(root, exist_ok=True)
        self.root = os.path.realpath(root)

    def resolve(self, rel: str, for_write: bool = False) -> str:
        if not isinstance(rel, str):
            raise GuardError("path must be a string")
        if len(rel) > 512:
            raise GuardError("path too long")
        if "\x00" in rel or "\\" in rel or ":" in rel:
            raise GuardError("path refused (NUL, backslash or colon)", 403)
        if rel.startswith("/") or rel.startswith("~"):
            raise GuardError("absolute path refused", 403)
        segs = [s for s in rel.split("/") if s not in ("", ".")]
        for i, s in enumerate(segs):
            if s == "..":
                raise GuardError("path traversal refused", 403)
            if not _SEG_OK.match(s):
                raise GuardError(f"path segment refused: {s[:40]!r}", 403)
            if s.startswith(".") and not (i == 0 and s == ARCHIVE and not for_write):
                raise GuardError("hidden path refused", 403)
        full = os.path.realpath(os.path.join(self.root, *segs))
        if full != self.root and not full.startswith(self.root + os.sep):
            raise GuardError("path escapes workspace (symlink?) refused", 403)
        return full

    def rel(self, full: str) -> str:
        return os.path.relpath(full, self.root).replace(os.sep, "/")

    def list(self, rel: str = "") -> dict:
        full = self.resolve(rel)
        if not os.path.isdir(full):
            raise GuardError("not a directory", 404)
        items = []
        for name in sorted(os.listdir(full))[:MAX_LIST]:
            p = os.path.join(full, name)
            if os.path.islink(p):
                real = os.path.realpath(p)
                if not real.startswith(self.root + os.sep):
                    items.append({"name": name, "type": "link-outside (hidden from use)", "size": 0})
                    continue
            st = os.stat(p)
            items.append({"name": name, "type": "dir" if os.path.isdir(p) else "file", "size": st.st_size,
                          "mtime": int(st.st_mtime)})
        return {"path": self.rel(full) if full != self.root else "", "items": items}

    def read(self, rel: str) -> dict:
        full = self.resolve(rel)
        if not os.path.isfile(full):
            raise GuardError("not a file", 404)
        size = os.path.getsize(full)
        if size > MAX_READ:
            raise GuardError(f"file over read cap ({MAX_READ} bytes)", 413)
        b = open(full, "rb").read(MAX_READ + 1)
        try:
            return {"path": self.rel(full), "encoding": "utf-8", "content": b.decode("utf-8"), "size": size}
        except UnicodeDecodeError:
            return {"path": self.rel(full), "encoding": "base64", "content": base64.b64encode(b).decode("ascii"),
                    "size": size, "note": "not UTF-8 (shown as base64; QUARANTINE node for the text door)"}

    def write(self, rel: str, content, encoding: str = "utf-8") -> dict:
        if not rel or rel.endswith("/"):
            raise GuardError("file name required")
        full = self.resolve(rel, for_write=True)
        if encoding == "utf-8":
            if not isinstance(content, str):
                raise GuardError("content must be a string")
            data = content.encode("utf-8")
        elif encoding == "base64":
            try:
                data = base64.b64decode(content, validate=True)
            except Exception:
                raise GuardError("bad base64")
        else:
            raise GuardError("encoding must be utf-8 or base64")
        if len(data) > MAX_WRITE:
            raise GuardError(f"content over write cap ({MAX_WRITE} bytes)", 413)
        if os.path.isdir(full):
            raise GuardError("a directory has that name", 409)
        parent = os.path.dirname(full)
        os.makedirs(parent, exist_ok=True)
        if os.path.realpath(parent) != parent or not (parent == self.root or parent.startswith(self.root + os.sep)):
            raise GuardError("parent escapes workspace", 403)
        archived = ""
        if os.path.exists(full):
            if open(full, "rb").read() == data:
                return {"path": self.rel(full), "bytes": len(data), "archived": "", "unchanged": True}
            stamp = time.strftime("%Y%m%d-%H%M%S") + f"-{time.time_ns() % 10**6:06d}"
            dest = os.path.join(self.root, ARCHIVE, self.rel(full) + "." + stamp)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy2(full, dest)
            archived = self.rel(dest)
        tmp = full + ".kit-tmp"
        with open(tmp, "wb") as f:
            f.write(data)
        os.replace(tmp, full)
        return {"path": self.rel(full), "bytes": len(data), "archived": archived}
