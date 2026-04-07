#!/usr/bin/env python3
"""
Arkhe-Talk: Markdown-based social metadata system for Arkhe agents.
Inspired by KarpathyTalk.
"""

import json
from datetime import datetime
from typing import Dict, Any

class ArkheTalkPost:
    def __init__(self, author: str, content: str, metadata: Dict[str, Any] = None):
        self.post_id = hash(f"{author}{content}{datetime.now()}") % 100000
        self.author = author
        self.content_markdown = content
        self.metadata = metadata or {}
        self.created_at = datetime.now().isoformat()

    def to_json(self) -> str:
        return json.dumps({
            'id': self.post_id,
            'author': self.author,
            'content': self.content_markdown,
            'metadata': self.metadata,
            'created_at': self.created_at
        }, indent=2)

class ArkheTalk:
    def __init__(self):
        self.posts = []

    def publish_coherence_report(self, agent_id: str, lambda_val: float, message: str):
        report_md = f"""## Coherence Report: {agent_id}
**System Status:** λ₂ = {lambda_val:.4f}
**Observation:** {message}
"""
        post = ArkheTalkPost(
            author=agent_id,
            content=report_md,
            metadata={'type': 'coherence_report', 'lambda': lambda_val}
        )
        self.posts.append(post)
        print(f"📢 Arkhe-Talk: {agent_id} published a new coherence report.")
        return post

    def get_feed(self):
        return [p.to_json() for p in self.posts]
