from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from langsmith import traceable

from app.models.user import User

from app.core.events import SecurityEvent

from app.ai_security.security_pipeline import (
    SecurityPipeline,
)

from app.services.prompt_builder import (
    PromptBuilder,
)

from app.services.retriever_service import (
    RetrieverService,
)

from app.services.audit_service import (
    AuditService,
)

from app.services.conversation_service import (
    ConversationService,
)

from app.shared.ai.azure_openai_client import (
    AzureOpenAIClient,
)

from app.ai_monitoring.token_tracker import (
    TokenTracker,
)

from app.ai_monitoring.latency_tracker import (
    LatencyTracker,
)

from app.ai_monitoring.llm_logger import (
    LLMLogger,
)


class ChatService:

    def __init__(
        self,
        session: AsyncSession,
        retriever_service: RetrieverService,
    ):

        self.session = session

        self.retriever_service = retriever_service

        self.security = SecurityPipeline()

        self.audit_service = AuditService()

        self.conversation_service = ConversationService()

        self.prompt_builder = PromptBuilder()

        self.azure_client = AzureOpenAIClient()

        self.token_tracker = TokenTracker()

        self.latency_tracker = LatencyTracker()

        self.llm_logger = LLMLogger()

    @traceable(
        name="security_copilot_chat"
    )
    async def chat(
        self,
        question: str,
        user: User,
    ) -> dict[str, Any]:

        secured_question = (
            self.security.secure_input(
                question
            )
        )

        history = await self.conversation_service.get_history(
            session=self.session,
            user_id=user.id,
        )

        documents = await self.retriever_service.search(
            query=secured_question,
            top_k=5,
        )

        messages = self.prompt_builder.build(
            question=secured_question,
            context=documents,
            history=history,
        )

        start_time = self.latency_tracker.start()

        response = await self.azure_client.chat_completion(
            messages=messages,
        )

        latency = self.latency_tracker.end(
            start_time
        )

        token_usage = self.token_tracker.calculate(
            response
        )

        self.llm_logger.log_request(
            model="azure-openai",
            latency=latency,
            tokens=token_usage,
        )

        answer = (
            response.choices[0]
            .message
            .content
            or ""
        )

        secured_answer = (
            self.security.secure_output(
                answer
            )
        )

        await self.conversation_service.save(
            session=self.session,
            user_id=user.id,
            question=secured_question,
            answer=secured_answer,
        )

        await self.audit_service.log(
            session=self.session,
            user=user.username,
            event=SecurityEvent.CHAT_COMPLETED,
            resource="KNOWLEDGE_ASSISTANT",
            details={
                "documents_used": len(documents),
                "latency": latency,
                "tokens": {
                    "prompt": token_usage.prompt_tokens,
                    "completion": token_usage.completion_tokens,
                    "total": token_usage.total_tokens,
                },
            },
        )

        return {

            "answer": secured_answer,

            "metadata": {

                "documents_used":
                len(documents),

                "latency":
                latency,

                "tokens": {

                    "prompt":
                    token_usage.prompt_tokens,

                    "completion":
                    token_usage.completion_tokens,

                    "total":
                    token_usage.total_tokens,

                },

            },

            "sources": [

                {

                    "id": str(doc.id),

                    "source": doc.source,

                    "content_preview":
                    doc.content[:200],

                }

                for doc in documents

            ],

        }

    async def stream_chat(
        self,
        question: str,
        user: User,
    ) -> AsyncGenerator[str, None]:

        start_time = self.latency_tracker.start()

        try:

            # ==================================================
            # 1. Input Security Validation
            # ==================================================

            secured_question = (

                self.security.secure_input(

                    question

                )

            )

            # ==================================================
            # 2. Conversation History
            # ==================================================

            history = await self.conversation_service.get_history(

                session=self.session,

                user_id=user.id,

            )

            # ==================================================
            # 3. Retrieve Context
            # ==================================================

            documents = await self.retriever_service.search(

                query=secured_question,

                top_k=5,

            )

            # ==================================================
            # 4. Build Prompt
            # ==================================================

            messages = self.prompt_builder.build(

                question=secured_question,

                context=documents,

                history=history,

            )

            full_response = ""

            # ==================================================
            # 5. Stream Azure OpenAI Response
            # ==================================================

            async for token in self.azure_client.stream_chat_completion(

                messages

            ):

                full_response += token

                yield token

            # ==================================================
            # 6. Output Security
            # ==================================================

            secured_answer = (

                self.security.secure_output(

                    full_response

                )

            )

            # ==================================================
            # 7. Latency Tracking
            # ==================================================

            latency = self.latency_tracker.end(

                start_time

            )

            # ==================================================
            # 8. Token Tracking
            # ==================================================

            # Streaming response does not contain usage metadata

            token_usage = self.token_tracker.calculate(

                None

            )

            self.llm_logger.log_request(

                model="azure-openai",

                latency=latency,

                tokens=token_usage,

            )

            # ==================================================
            # 9. Save Conversation
            # ==================================================

            await self.conversation_service.save(

                session=self.session,

                user_id=user.id,

                question=secured_question,

                answer=secured_answer,

            )

            # ==================================================
            # 10. Audit Logging
            # ==================================================

            await self.audit_service.log(

                session=self.session,

                user=user.username,

                event=SecurityEvent.CHAT_COMPLETED,

                resource="KNOWLEDGE_ASSISTANT_STREAM",

                details={

                    "streaming": True,

                    "documents_used": len(documents),

                    "response_length":
                    len(secured_answer),

                    "latency": latency,

                    "prompt_tokens":
                    token_usage.prompt_tokens,

                    "completion_tokens":
                    token_usage.completion_tokens,

                    "total_tokens":
                    token_usage.total_tokens,

                },

            )

        except Exception as exc:

            latency = self.latency_tracker.end(

                start_time

            )

            await self.audit_service.log(

                session=self.session,

                user=user.username,

                event=SecurityEvent.CHAT_FAILED,

                resource="KNOWLEDGE_ASSISTANT_STREAM",

                details={

                    "error": str(exc),

                    "latency": latency,

                },

            )

            raise