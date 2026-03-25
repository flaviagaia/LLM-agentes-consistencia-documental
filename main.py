import json
import sys


def main() -> int:
    try:
        from src.pipeline import run_pipeline
    except ModuleNotFoundError as exc:
        print(
            "Dependencia ausente ao iniciar o projeto. "
            "Ative o ambiente virtual e instale requirements.txt antes de executar."
        )
        print(f"Modulo ausente: {exc.name}")
        return 1

    summary = run_pipeline(use_llm=False)
    print("LLM Agentes Consistencia Documental")
    print("-" * 44)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
