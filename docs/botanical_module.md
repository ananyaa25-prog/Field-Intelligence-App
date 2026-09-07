\# Botanical Intelligence AI Module



\## 1. Overview



The Botanical Intelligence AI module provides a grounded question-answering pipeline for India's native flora.



The module combines structured botanical knowledge, conservation information, evidence evaluation, question classification, grounded prompt construction, deterministic response generation, and application-ready response formatting.



The main entry point is:



`ai/botanical\_assistant.py`



The architecture is designed so that factual botanical responses are generated from the verified project knowledge base rather than unsupported information.



\---



\## 2. AI Pipeline



The complete pipeline is:



```text

User Question

&#x20;     ↓

Plant Retrieval

&#x20;     ↓

Question Classification

&#x20;     ↓

Evidence Collection

&#x20;     ↓

Confidence Evaluation

&#x20;     ↓

Grounded Prompt Construction

&#x20;     ↓

Grounded Response Generation

&#x20;     ↓

Response Formatting

&#x20;     ↓

Application-Ready Output

