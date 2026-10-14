"""WhatsApp automation flow (sandbox-ready, no live API required)."""

from datetime import datetime, timezone
from typing import List, Optional, Tuple
from uuid import UUID

from sqlalchemy.orm import Session, joinedload

from app.core.enums import ConversationStatus, MessageDirection, WhatsAppSessionStatus
from app.core.exceptions import NotFoundError
from app.models.whatsapp import WhatsAppConversation, WhatsAppMessage, WhatsAppOrderSession
from app.schemas import WhatsAppInboundMessage
from app.services.ai_service import AIAssistantService


class WhatsAppService:
    """Internal WhatsApp order automation orchestrator."""

    def __init__(self, db: Session):
        self.db = db
        self.ai = AIAssistantService()

    def list_conversations(self, restaurant_id: UUID) -> List[WhatsAppConversation]:
        return (
            self.db.query(WhatsAppConversation)
            .filter(WhatsAppConversation.restaurant_id == restaurant_id)
            .order_by(WhatsAppConversation.updated_at.desc())
            .all()
        )

    def get_conversation(self, restaurant_id: UUID, conversation_id: UUID) -> WhatsAppConversation:
        conversation = (
            self.db.query(WhatsAppConversation)
            .options(joinedload(WhatsAppConversation.messages))
            .filter(
                WhatsAppConversation.id == conversation_id,
                WhatsAppConversation.restaurant_id == restaurant_id,
            )
            .first()
        )
        if not conversation:
            raise NotFoundError("Conversation not found")
        return conversation

    def handle_inbound(self, data: WhatsAppInboundMessage) -> Tuple[WhatsAppConversation, WhatsAppMessage, str]:
        conversation = (
            self.db.query(WhatsAppConversation)
            .filter(
                WhatsAppConversation.restaurant_id == data.restaurant_id,
                WhatsAppConversation.customer_phone == data.customer_phone,
                WhatsAppConversation.status != ConversationStatus.CLOSED.value,
            )
            .order_by(WhatsAppConversation.created_at.desc())
            .first()
        )
        if not conversation:
            conversation = WhatsAppConversation(
                restaurant_id=data.restaurant_id,
                customer_phone=data.customer_phone,
                customer_name=data.customer_name,
                status=ConversationStatus.ACTIVE.value,
            )
            self.db.add(conversation)
            self.db.flush()

        inbound = WhatsAppMessage(
            conversation_id=conversation.id,
            direction=MessageDirection.INBOUND.value,
            body=data.body,
            external_message_id=data.external_message_id,
            is_ai_generated=False,
        )
        self.db.add(inbound)

        session = self._get_or_create_session(conversation)
        reply, intent, new_status = self._process_intent(data.body, session)

        inbound.intent = intent
        session.status = new_status
        conversation.last_message_at = datetime.now(timezone.utc)

        if conversation.human_handover:
            reply = (
                "A team member will assist you shortly. "
                "آپ سے جلد ہماری ٹیم رابطہ کرے گی۔"
            )
            intent = "human_handover"

        outbound = WhatsAppMessage(
            conversation_id=conversation.id,
            direction=MessageDirection.OUTBOUND.value,
            body=reply,
            intent=intent,
            is_ai_generated=True,
        )
        self.db.add(outbound)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation, outbound, reply

    def set_human_handover(
        self,
        restaurant_id: UUID,
        conversation_id: UUID,
        enabled: bool,
        staff_id: Optional[UUID] = None,
    ) -> WhatsAppConversation:
        conversation = self.get_conversation(restaurant_id, conversation_id)
        conversation.human_handover = enabled
        conversation.status = (
            ConversationStatus.HUMAN_HANDOVER.value if enabled else ConversationStatus.ACTIVE.value
        )
        conversation.assigned_staff_id = staff_id
        if enabled:
            session = (
                self.db.query(WhatsAppOrderSession)
                .filter(WhatsAppOrderSession.conversation_id == conversation.id)
                .order_by(WhatsAppOrderSession.created_at.desc())
                .first()
            )
            if session:
                session.status = WhatsAppSessionStatus.HANDED_OVER.value
        self.db.commit()
        self.db.refresh(conversation)
        return conversation

    def _get_or_create_session(self, conversation: WhatsAppConversation) -> WhatsAppOrderSession:
        session = (
            self.db.query(WhatsAppOrderSession)
            .filter(
                WhatsAppOrderSession.conversation_id == conversation.id,
                WhatsAppOrderSession.status.notin_(
                    [
                        WhatsAppSessionStatus.ORDER_CREATED.value,
                        WhatsAppSessionStatus.CANCELLED.value,
                    ]
                ),
            )
            .order_by(WhatsAppOrderSession.created_at.desc())
            .first()
        )
        if session:
            return session
        session = WhatsAppOrderSession(
            conversation_id=conversation.id,
            restaurant_id=conversation.restaurant_id,
            status=WhatsAppSessionStatus.STARTED.value,
            cart={"items": []},
        )
        self.db.add(session)
        self.db.flush()
        return session

    def _process_intent(
        self, body: str, session: WhatsAppOrderSession
    ) -> Tuple[str, str, str]:
        text = body.strip().lower()
        ai = self.ai.detect_intent(body)

        if "menu" in text or "مینو" in text or ai.get("intent") == "menu":
            return (
                "Here is our menu highlight:\n"
                "1. Chicken Karahi — PKR 1,200\n"
                "2. Chicken Biryani — PKR 450\n"
                "3. Zinger Burger — PKR 550\n"
                "4. BBQ Platter — PKR 2,200\n"
                "Reply with item number to add to cart.\n"
                "مینو کے لیے نمبر بھیجیں۔",
                "share_menu",
                WhatsAppSessionStatus.BROWSING_MENU.value,
            )

        if text.isdigit() or "add" in text or ai.get("intent") == "add_item":
            cart = session.cart or {"items": []}
            cart.setdefault("items", []).append({"raw": body, "qty": 1})
            session.cart = cart
            return (
                "Item added. Reply 'address' with your delivery address, or 'menu' for more items.",
                "add_item",
                WhatsAppSessionStatus.SELECTING_ITEMS.value,
            )

        if "address" in text or "پتہ" in text or ai.get("intent") == "address":
            session.delivery_address = body
            return (
                "Address saved. Reply 'confirm' to place your order.\n"
                "آرڈر کنفرم کرنے کے لیے confirm لکھیں۔",
                "collect_address",
                WhatsAppSessionStatus.COLLECTING_ADDRESS.value,
            )

        if "confirm" in text or "کنفرم" in text or ai.get("intent") == "confirm":
            # Order creation is completed by order service in a later integration step
            return (
                "Order confirmed! Our kitchen is preparing it. "
                "You will receive updates here.\n"
                "آپ کا آرڈر کنفرم ہو گیا ہے۔",
                "confirm_order",
                WhatsAppSessionStatus.CONFIRMING.value,
            )

        if "human" in text or "agent" in text or "نمائندہ" in text:
            return (
                "Connecting you to a human agent...",
                "human_handover",
                WhatsAppSessionStatus.HANDED_OVER.value,
            )

        return (
            "Assalamualaikum! Welcome to Online Restaurant.\n"
            "Reply *menu* to see items, or *human* to talk to staff.\n"
            "السلام علیکم! مینو کے لیے menu لکھیں۔",
            "greeting",
            session.status or WhatsAppSessionStatus.STARTED.value,
        )
