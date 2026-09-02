# OASST1 Data Dictionary

## Dataset
OpenAssistant Conversations Dataset (OASST1)

## Messages Table

| Field | Description | Data Type |
|---|---|---|
| message_id | Unique identifier for each message | Text |
| parent_id | Identifier of the parent message | Text |
| user_id | Anonymous user identifier | Text |
| created_date | Message creation timestamp | DateTime |
| text | Message content | Text |
| role | Message author role | Text |
| lang | Message language | Text |
| review_count | Number of reviews associated with message | Integer |
| review_result | Recorded review-result value | Numeric |
| deleted | Indicates whether message is marked deleted | Integer |
| rank | Message ranking information | Numeric |
| synthetic | Synthetic-data indicator | Integer |
| detoxify | Detoxify/safety metadata | Numeric/Text |
| message_tree_id | Conversation tree identifier | Text |
| tree_state | Conversation tree state | Text |
| emojis | Emoji metadata | Text |
| labels | Message labels/metadata | Text |

## Conversations Table

| Field | Description | Data Type |
|---|---|---|
| message_tree_id | Unique conversation-tree identifier | Text |
| root_message_id | Root message of the conversation | Text |
| conversation_created_at | Conversation creation timestamp | DateTime |

## Dataset Statistics

- Total Messages: 88,838
- Total Conversations: 10,364
- Total Users: 13,249
- Total Languages: 25
- Dataset Period: January–April 2023