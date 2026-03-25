import json

from src.pipeline import run_pipeline


if __name__ == "__main__":
    summary = run_pipeline(use_llm=False)
    print("LLM Agentes Consistencia Documental")
    print("-" * 44)
    print(json.dumps(summary, indent=2))
