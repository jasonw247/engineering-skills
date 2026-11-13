# Routing from skill name and description

- Main request: Activate. Diagnosing a wrong RAG answer from its trace and proposing a narrow repair is pipeline debugging.
- Neighbor request (answer a question from three attached passages): Do not activate. This asks for an answer from supplied sources, not engineering or diagnosing a retrieval pipeline.

This routing decision uses only the skill name and description.
