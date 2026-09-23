"""
CHUP Phase 7 — JSON Explanation Renderer.

Serializes an ExplanationDocument to deterministic, schema-compliant JSON.
"""

import json
from typing import Dict, Any
from pointer_algorithms.proof_explanation.explanation_model import ExplanationDocument


class JsonExplanationRenderer:
    """
    Renders ExplanationDocument into structured JSON string or dictionary.
    """

    @classmethod
    def to_dict(cls, doc: ExplanationDocument) -> Dict[str, Any]:
        return doc.to_dict()

    @classmethod
    def to_json(cls, doc: ExplanationDocument, indent: int = 2) -> str:
        return json.dumps(doc.to_dict(), indent=indent, sort_keys=True)
