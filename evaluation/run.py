import asyncio
import json
from pathlib import Path

import httpx


API_URL = "http://localhost:8000/api/v1/ask"
CASES_FILE = Path(__file__).parent / "cases.json"
RESULTS_FILE = Path(__file__).parent / "results.md"


def markdown_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


async def main():
    cases = json.loads(CASES_FILE.read_text())

    passed_count = 0
    report_rows = []

    async with httpx.AsyncClient(timeout=120.0) as client:
        for case in cases:
            response = await client.post(
                API_URL,
                json={"question": case["question"]},
            )

            response.raise_for_status()
            result = response.json()

            passed = True
            reasons = []

            # Check expected status
            if result["status"] != case["expected_status"]:
                passed = False
                reasons.append(
                    f"status expected={case['expected_status']} "
                    f"actual={result['status']}"
                )

            # Check expected answer content
            expected_contains = case.get("expected_contains")

            if expected_contains:
                answer = result.get("answer") or ""

                if expected_contains.lower() not in answer.lower():
                    passed = False
                    reasons.append(
                        f"answer does not contain '{expected_contains}'"
                    )

            # Check expected source version
            expected_version = case.get("expected_version")

            if expected_version is not None:
                source_versions = [
                    source["version"]
                    for source in result.get("sources", [])
                ]

                if expected_version not in source_versions:
                    passed = False
                    reasons.append(
                        f"expected source version {expected_version}"
                    )

            # Count passed cases
            if passed:
                passed_count += 1

            status = "PASS" if passed else "FAIL"

            print(
                f"\n[{status}] "
                f"[{case['type'].upper()}] "
                f"{case['question']}"
            )

            print(f"Expected status: {case['expected_status']}")
            print(f"Actual status:   {result['status']}")
            print(f"Answer:          {result.get('answer')}")
            print(f"Sources:         {result.get('sources')}")

            if reasons:
                print(f"Reasons:         {', '.join(reasons)}")

            source_summary = "; ".join(
                f"{source.get('filename')} v{source.get('version')} "
                f"({source.get('section')})"
                for source in result.get("sources", [])
            ) or "—"
            report_rows.append(
                "| "
                + " | ".join(
                    [
                        str(case["id"]),
                        markdown_cell(case["type"]),
                        markdown_cell(case["question"]),
                        markdown_cell(case["expected_status"]),
                        markdown_cell(result["status"]),
                        markdown_cell(case.get("expected_contains", "—")),
                        markdown_cell(case.get("expected_version", "—")),
                        markdown_cell(result.get("answer") or "—"),
                        markdown_cell(source_summary),
                        status,
                    ]
                )
                + " |"
            )

    print("\n------------------------------")
    print(f"Result: {passed_count}/{len(cases)} passed")
    print("------------------------------")

    RESULTS_FILE.write_text(
        "# Evaluation Results\n\n"
        f"API: `{API_URL}`  \n"
        f"Final result: **{passed_count}/{len(cases)} passed**\n\n"
        "| ID | Type | Question | Expected status | Actual status | "
        "Expected keyword | Expected version | Actual answer | Sources | Result |\n"
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n"
        + "\n".join(report_rows)
        + "\n",
        encoding="utf-8",
    )
    print(f"Markdown report: {RESULTS_FILE}")


if __name__ == "__main__":
    asyncio.run(main())
