"""AI assistant and phone agent placeholders (OpenAI-ready)."""

from typing import Any, Dict, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import NotFoundError
from app.models.ai_call import AICallLog
from app.schemas import AICallLogCreate, AIChatRequest, AIChatResponse


class AIAssistantService:
    """
    Placeholder for future OpenAI integration.
    Uses heuristic intent detection until OPENAI_API_KEY is configured.
    """

    def detect_intent(self, message: str) -> Dict[str, Any]:
        text = message.lower()
        if any(w in text for w in ("menu", "مینو", "items")):
            return {"intent": "menu", "confidence": 0.8}
        if any(w in text for w in ("order", "آرڈر", "add")):
            return {"intent": "add_item", "confidence": 0.7}
        if any(w in text for w in ("address", "پتہ", "deliver")):
            return {"intent": "address", "confidence": 0.75}
        if any(w in text for w in ("confirm", "کنفرم", "yes")):
            return {"intent": "confirm", "confidence": 0.8}
        if any(w in text for w in ("complaint", "شکایت", "problem")):
            return {"intent": "complaint", "confidence": 0.85}
        if any(w in text for w in ("human", "agent", "نمائندہ")):
            return {"intent": "human_handover", "confidence": 0.9}
        return {"intent": "general", "confidence": 0.4}

    def chat(self, request: AIChatRequest) -> AIChatResponse:
        intent_info = self.detect_intent(request.message)
        intent = intent_info["intent"]
        lang = request.language

        if settings.OPENAI_API_KEY:
            # Future: call OpenAI Chat Completions here using settings.OPENAI_API_KEY
            pass

        replies = {
            "menu": {
                "en": "I can help with our menu. Popular items: Chicken Karahi, Biryani, BBQ.",
                "ur": "میں مینو میں مدد کر سکتا ہوں۔ مشہور آئٹمز: چکن کڑاہی، بریانی، باربی کیو۔",
            },
            "complaint": {
                "en": "I'm sorry about the issue. I can note your complaint or connect you to staff.",
                "ur": "معذرت خواہ ہیں۔ میں آپ کی شکایت نوٹ کر سکتا ہوں یا عملے سے منسلک کر سکتا ہوں۔",
            },
            "human_handover": {
                "en": "Connecting you to a human agent.",
                "ur": "آپ کو انسانی نمائندے سے جوڑا جا رہا ہے۔",
            },
            "general": {
                "en": "I can take orders, answer menu questions, or connect you to staff. How can I help?",
                "ur": "میں آرڈر لے سکتا ہوں، مینو بت سکتا ہوں، یا عملے سے منسلک کر سکتا ہوں۔",
            },
        }
        bucket = replies.get(intent, replies["general"])
        reply = bucket.get(lang, bucket["en"])
        return AIChatResponse(
            reply=reply,
            intent=intent,
            language=lang,
            requires_human=intent in ("complaint", "human_handover"),
            meta={"provider": "placeholder", "openai_configured": bool(settings.OPENAI_API_KEY)},
        )


class AICallService:
    def __init__(self, db: Session):
        self.db = db

    def create_log(self, data: AICallLogCreate) -> AICallLog:
        log = AICallLog(**data.model_dump())
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log

    def list_logs(self, restaurant_id: UUID) -> list[AICallLog]:
        return (
            self.db.query(AICallLog)
            .filter(AICallLog.restaurant_id == restaurant_id)
            .order_by(AICallLog.created_at.desc())
            .all()
        )

    def get_log(self, restaurant_id: UUID, call_id: UUID) -> AICallLog:
        log = (
            self.db.query(AICallLog)
            .filter(AICallLog.id == call_id, AICallLog.restaurant_id == restaurant_id)
            .first()
        )
        if not log:
            raise NotFoundError("Call log not found")
        return log

    def update_transcript(
        self,
        restaurant_id: UUID,
        call_id: UUID,
        transcript: str,
        summary: Optional[str] = None,
        extracted_order: Optional[dict] = None,
        human_followup: bool = False,
        status: str = "completed",
    ) -> AICallLog:
        log = self.get_log(restaurant_id, call_id)
        log.transcript = transcript
        log.summary = summary
        log.extracted_order = extracted_order
        log.human_followup_required = human_followup
        log.status = status
        self.db.commit()
        self.db.refresh(log)
        return log
