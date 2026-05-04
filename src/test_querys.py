import json
from src.graph import build_graph

def run_tests():
    # Cargar JSON
    with open("tests/test_querys.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    tests = data["test_queries"]

    graph = build_graph()

    correct = 0

    print("\n=== EJECUTANDO TESTS ===\n")

    for i, test in enumerate(tests, 1):
        query = test["query"]
        expected = test["expected_department"]

        result = graph.invoke({"query": query})
        predicted = result.get("department")

        status = "✅" if predicted == expected else "❌"

        print(f"{i}. {query}")
        print(f"   Esperado: {expected}")
        print(f"   Predicho: {predicted}")
        print(f"   Resultado: {status}\n")

        if predicted == expected:
            correct += 1

    print("=" * 50)
    print(f"Accuracy: {correct}/{len(tests)} = {correct/len(tests)*100:.2f}%")
    print("=" * 50)


if __name__ == "__main__":
    run_tests()