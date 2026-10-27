import asyncio
import json
from dotenv import load_dotenv
load_dotenv()
from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import ContextualPrecisionMetric , ContextualRecallMetric
from search.hybrid_search import retrieve_hybrid
from db.base import asyncsession
from deepeval.models import LiteLLMModel



golden_data_path = "evals/golden_dataset/golden_data.json"
llm_judge = LiteLLMModel(model="gemini/gemini-3.5-flash-lite")
threshold = 0.6

test_cases = []
async def main():
    global test_cases
    with open(golden_data_path) as f:
        golden_data = json.load(f)
    async with asyncsession() as db:
        for case in golden_data:
            retrieved = []
            for r in await retrieve_hybrid(db , case["question"]):
                retrieved.append(r.chunk_text)
            test_cases.append(LLMTestCase(
                input=case["question"],
                expected_output=case["ideal_answer"],
                retrieval_context=retrieved,
                actual_output="generator not evaluted in this run"
            ))    


asyncio.run(main())

metrics = [ContextualRecallMetric(threshold=threshold , model=llm_judge , include_reason=True) , ContextualPrecisionMetric(threshold=threshold , model=llm_judge , include_reason=True)]
evaluate(test_cases=test_cases , metrics=metrics)
