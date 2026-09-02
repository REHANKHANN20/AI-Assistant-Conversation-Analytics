-- ============================================================
-- OASST1 AI ASSISTANT CONVERSATION ANALYTICS DATABASE
-- ============================================================

PRAGMA foreign_keys = ON;


-- ============================================================
-- 1. CONVERSATIONS TABLE
-- ============================================================

CREATE TABLE IF NOT EXISTS conversations (
    message_tree_id TEXT PRIMARY KEY,
    root_message_id TEXT,
    conversation_created_at TEXT
);


-- ============================================================
-- 2. MESSAGES TABLE
-- ============================================================

CREATE TABLE IF NOT EXISTS messages (
    message_id TEXT PRIMARY KEY,
    message_tree_id TEXT NOT NULL,
    parent_id TEXT,
    user_id TEXT,
    created_date TEXT,
    text TEXT,
    role TEXT,
    lang TEXT,
    review_count INTEGER,
    review_result INTEGER,
    deleted INTEGER,
    rank REAL,
    synthetic INTEGER,
    detoxify TEXT,
    tree_state TEXT,
    emojis TEXT,
    labels TEXT,
    source_split TEXT,

    FOREIGN KEY (message_tree_id)
        REFERENCES conversations(message_tree_id)
);


-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_messages_tree
ON messages(message_tree_id);

CREATE INDEX IF NOT EXISTS idx_messages_parent
ON messages(parent_id);

CREATE INDEX IF NOT EXISTS idx_messages_role
ON messages(role);

CREATE INDEX IF NOT EXISTS idx_messages_lang
ON messages(lang);

CREATE INDEX IF NOT EXISTS idx_messages_created_date
ON messages(created_date);

CREATE INDEX IF NOT EXISTS idx_messages_user
ON messages(user_id);