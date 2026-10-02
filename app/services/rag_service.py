from sqlalchemy.ext.asyncio import AsyncSession
import json
import logging
from app.providers.ollama_chat import OllamaChatProvider
from app.services.retrieval_service import RetrievalService, SearchResult

logger = logging.getLogger(__name__)
INSUFFICIENT_INFORMATION_ANSWER = (
    "Bu soruyu yanıtlamak için mevcut dokümanlarda yeterli bilgi bulunmuyor."
)


class RAGService:
    def __init__(self, db: AsyncSession) -> None:
        self.retrieval = RetrievalService(db)
        self.chat_provider = OllamaChatProvider()

    def _build_context(self, results: list[SearchResult]) -> str:
        context_parts = []

        for index, result in enumerate(results, start=1):
            context_parts.append(
                f"""
                    [SOURCE_{index}]
                    Document: {result.title}
                    File: {result.filename}
                    Version: {result.version}
                    Section: {result.section}

                    {result.content}
                    """.strip()
                )

        return "\n\n---\n\n".join(context_parts)

    async def answer(self, question: str) -> dict:
        results = await self.retrieval.search(
            query=question,
            limit=5,
        )

        if not self.retrieval.is_relevant(results):
            return {
                "status": "insufficient_information",
                "answer": INSUFFICIENT_INFORMATION_ANSWER,
                "sources": [],
            }

        context = self._build_context(results)

        system_prompt = """
            You are a Turkish customer-support knowledge assistant. Use only
            the supplied context; do not invent facts or use outside knowledge.

            Return "answered" when the context directly answers or clearly
            implies the answer. Do not require the answer to repeat the exact
            wording from the context. Keep an answered response natural and
            concise (normally one to three Turkish sentences), and cite only
            the source IDs that support it.

            Return "insufficient_information" only when no supplied source
            directly answers the question.

            Return valid JSON only. An answered response MUST contain all of
            `status`, `answer`, and `source_ids`; use the key `source_ids`,
            never `sources`:
            {"status":"answered","answer":"Turkish answer","source_ids":["SOURCE_1"]}
            or
            {"status":"insufficient_information","answer":null,"source_ids":[]}
            """.strip()

        user_prompt = f"""
Context:

{context}

Question:
{question}
""".strip()

        raw_response = await self.chat_provider.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        try:
            parsed_response = json.loads(raw_response)
        except json.JSONDecodeError:
            logger.warning("Invalid JSON from model: %r", raw_response)
            return {
                "status": "generation_error",
                "answer": None,
                "sources": [],
            }

        if not isinstance(parsed_response, dict):
            logger.warning("Unexpected model response shape: %r", raw_response)
            return {
                "status": "generation_error",
                "answer": None,
                "sources": [],
            }

        if parsed_response.get("status") == "insufficient_information":
            return {
                "status": "insufficient_information",
                "answer": INSUFFICIENT_INFORMATION_ANSWER,
                "sources": [],
            }

        if (
            parsed_response.get("status") != "answered"
            or not isinstance(parsed_response.get("answer"), str)
        ):
            logger.warning("Unexpected model response shape: %r", raw_response)
            return {
                "status": "generation_error",
                "answer": None,
                "sources": [],
            }

        source_ids = parsed_response.get("source_ids")

        if not isinstance(source_ids, list) or not source_ids:
            logger.warning("Answered response without source IDs: %r", raw_response)
            return {
                "status": "generation_error",
                "answer": None,
                "sources": [],
            }

        sources = []

        for source_id in source_ids:
            if not isinstance(source_id, str):
                continue

            try:
                index = int(source_id.replace("SOURCE_", "")) - 1
            except ValueError:
                continue

            if 0 <= index < len(results):
                result = results[index]

                sources.append(
                    {
                        "filename": result.filename,
                        "title": result.title,
                        "section": result.section,
                        "version": result.version,
                    }
                )

        if not sources:
            logger.warning("Answered response without valid sources: %r", raw_response)
            return {
                "status": "generation_error",
                "answer": None,
                "sources": [],
            }

        return {
            "status": "answered",
            "answer": parsed_response["answer"],
            "sources": sources,
        }
