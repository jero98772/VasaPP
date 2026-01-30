from sqlalchemy import (
    Column, String, Text, DateTime, Boolean, Enum, 
    ForeignKey, Integer, BigInteger, func, CheckConstraint,Index
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, validates
import uuid
from datetime import datetime, timezone
from db.db import Base
import enum

# Enums as Python enums
class ChatType(str, enum.Enum):
    DIRECT = "direct"
    GROUP = "group"

class ParticipantRole(str, enum.Enum):
    ADMIN = "admin"
    MEMBER = "member"

class MessageType(str, enum.Enum):
    TEXT = "text"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    FILE = "file"

class ReceiptStatus(str, enum.Enum):
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    public_key = Column(Text, nullable=False)  # For Nostr/E2EE
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    
    # Relationships
    sent_messages = relationship("Message", back_populates="sender", foreign_keys="Message.sender_id")
    chat_participants = relationship("ChatParticipant", back_populates="user")
    message_receipts = relationship("MessageReceipt", back_populates="user")
    
    @validates('username')
    def validate_username(self, key, username):
        if len(username) < 3 or len(username) > 50:
            raise ValueError("Username must be between 3 and 50 characters")
        return username

class Chat(Base):
    __tablename__ = "chats"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(Enum(ChatType), nullable=False, default=ChatType.DIRECT)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    last_message_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    participants = relationship("ChatParticipant", back_populates="chat", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")
    
    __table_args__ = (
        CheckConstraint(
            "type IN ('direct', 'group')", 
            name="check_chat_type"
        ),
    )

class ChatParticipant(Base):
    __tablename__ = "chat_participants"
    
    chat_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("chats.id", ondelete="CASCADE"), 
        primary_key=True
    )
    user_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("users.id", ondelete="CASCADE"), 
        primary_key=True
    )
    role = Column(Enum(ParticipantRole), nullable=False, default=ParticipantRole.MEMBER)
    joined_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    left_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    chat = relationship("Chat", back_populates="participants")
    user = relationship("User", back_populates="chat_participants")
    
    @validates('role')
    def validate_role(self, key, role):
        if self.chat and self.chat.type == ChatType.DIRECT:
            if role != ParticipantRole.MEMBER:
                raise ValueError("Direct chats can only have members")
        return role

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("chats.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    sender_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False
    )
    type = Column(Enum(MessageType), nullable=False, default=MessageType.TEXT)
    content = Column(Text, nullable=False)  # Encrypted payload
    reply_to = Column(UUID(as_uuid=True), ForeignKey("messages.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    edited_at = Column(DateTime(timezone=True), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    chat = relationship("Chat", back_populates="messages")
    sender = relationship("User", back_populates="sent_messages", foreign_keys=[sender_id])
    media = relationship("Media", back_populates="message", cascade="all, delete-orphan")
    receipts = relationship("MessageReceipt", back_populates="message", cascade="all, delete-orphan")
    parent_message = relationship("Message", remote_side=[id], foreign_keys=[reply_to], post_update=True)
    
    __table_args__ = (
        CheckConstraint(
            "type IN ('text', 'image', 'video', 'audio', 'file')", 
            name="check_message_type"
        ),
        Index('idx_chat_created', 'chat_id', 'created_at'),
    )
    
    @validates('content')
    def validate_content(self, key, content):
        if not content or len(content.strip()) == 0:
            raise ValueError("Message content cannot be empty")
        return content

class MessageReceipt(Base):
    __tablename__ = "message_receipts"
    
    message_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("messages.id", ondelete="CASCADE"), 
        primary_key=True
    )
    user_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("users.id", ondelete="CASCADE"), 
        primary_key=True
    )
    status = Column(Enum(ReceiptStatus), nullable=False, default=ReceiptStatus.SENT)
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    message = relationship("Message", back_populates="receipts")
    user = relationship("User", back_populates="message_receipts")
    
    __table_args__ = (
        CheckConstraint(
            "status IN ('sent', 'delivered', 'read')", 
            name="check_receipt_status"
        ),
    )

class Media(Base):
    __tablename__ = "media"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    message_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("messages.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    url = Column(Text, nullable=False)
    mime_type = Column(String(100), nullable=False)
    size = Column(BigInteger, nullable=False)  # Size in bytes
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    
    # Relationships
    message = relationship("Message", back_populates="media")

class Contact(Base):
    __tablename__ = "contacts"
    
    owner_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("users.id", ondelete="CASCADE"), 
        primary_key=True
    )
    contact_user_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("users.id", ondelete="CASCADE"), 
        primary_key=True
    )
    alias = Column(String(100), nullable=True)
    blocked = Column(Boolean, default=False, nullable=False)
    
    # Relationships
    owner = relationship("User", foreign_keys=[owner_id])
    contact = relationship("User", foreign_keys=[contact_user_id])
    
    __table_args__ = (
        CheckConstraint("owner_id != contact_user_id", name="check_self_contact"),
    )