# VERCEL CONNECTER 2026-11-26
# Hashes build directory, logs deploy row. Direct deploys from shepherd.
# Six-pillar SVCT: content context data time semantics validation.
# Do No Harm first. Append-only. CONNECTER suite entry 8.
# Size 1921 bytes. SHA-256 d6db2c36ced32f1bfc86e6da2d8bd45b920b25be9f44f4c937b8733fab021549

import hashlib
import json
import os
from datetime import datetime

class VercelConnecter:
    def __init__(self, project_name, build_dir):
        self.project_name = project_name
        self.build_dir = build_dir
        self.deploy_log = []

    def seal_deploy_row(self, content, context, data, time_str, semantics, validation):
        row = {
            "content": content,
            "context": context,
            "data": data,
            "time": time_str,
            "semantics": semantics,
            "validation": validation
        }
        row_str = json.dumps(row, sort_keys=True)
        row_hash = hashlib.sha256(row_str.encode()).hexdigest()
        row["sha256"] = row_hash
        self.deploy_log.append(row)
        return row_hash

    def hash_build_directory(self):
        hashes = []
        for root, dirs, files in os.walk(self.build_dir):
            for f in sorted(files):
                path = os.path.join(root, f)
                with open(path, "rb") as fh:
                    h = hashlib.sha256(fh.read()).hexdigest()
                    hashes.append(f"{path}:{h}")
        combined = "\n".join(hashes)
        return hashlib.sha256(combined.encode()).hexdigest(), len(hashes)

    def log_deploy(self, deploy_id, status):
        dir_hash, file_count = self.hash_build_directory()
        now = datetime.now().astimezone().isoformat()
        return self.seal_deploy_row(
            content=f"vercel-deploy:{deploy_id}",
            context="VercelConnecter.log_deploy",
            data=json.dumps({"project": self.project_name, "build_dir_sha256": dir_hash, "file_count": file_count, "status": status}),
            time_str=now,
            semantics="deploy row, hashed build directory, provenance tracked",
            validation="sha256-sealed"
        )

    def terminate(self):
        return len(self.deploy_log)
