-- ============================================================
-- OASST1 AI ASSISTANT CONVERSATION ANALYTICS
-- SQL BUSINESS / ANALYTICAL QUESTIONS
-- ============================================================


-- ============================================================
-- Q1. WHAT IS THE OVERALL SIZE OF THE DATASET?
-- Business Question:
-- How large is the AI assistant conversation dataset?
-- ============================================================

SELECT
    COUNT(*) AS total_messages,
    COUNT(DISTINCT message_tree_id) AS total_conversations,
    COUNT(DISTINCT user_id) AS total_users,
    COUNT(DISTINCT lang) AS total_languages
FROM messages;


-- ============================================================
-- Q2. USER VS ASSISTANT PARTICIPATION
-- Business Question:
-- Who contributes more messages: users or assistants?
-- ============================================================

SELECT
    role,
    COUNT(*) AS message_count,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM messages),
        2
    ) AS percentage
FROM messages
GROUP BY role
ORDER BY message_count DESC;


-- ============================================================
-- Q3. WHICH LANGUAGES ARE MOST REPRESENTED?
-- Business Question:
-- Which languages dominate the dataset?
-- ============================================================

SELECT
    lang,
    COUNT(*) AS message_count,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM messages),
        2
    ) AS percentage
FROM messages
WHERE lang IS NOT NULL
GROUP BY lang
ORDER BY message_count DESC
LIMIT 15;


-- ============================================================
-- Q4. HOW MANY MESSAGES ARE IN EACH CONVERSATION?
-- Business Question:
-- Are conversations generally short or long?
-- ============================================================

SELECT
    message_tree_id,
    COUNT(*) AS message_count
FROM messages
GROUP BY message_tree_id
ORDER BY message_count DESC
LIMIT 20;


-- ============================================================
-- Q5. CONVERSATION LENGTH DISTRIBUTION
-- Business Question:
-- How are conversations distributed by length?
-- ============================================================

SELECT
    CASE
        WHEN message_count = 1 THEN '1 message'
        WHEN message_count BETWEEN 2 AND 5 THEN '2-5 messages'
        WHEN message_count BETWEEN 6 AND 10 THEN '6-10 messages'
        WHEN message_count BETWEEN 11 AND 20 THEN '11-20 messages'
        ELSE '21+ messages'
    END AS conversation_length_group,
    COUNT(*) AS conversation_count
FROM (
    SELECT
        message_tree_id,
        COUNT(*) AS message_count
    FROM messages
    GROUP BY message_tree_id
)
GROUP BY conversation_length_group
ORDER BY conversation_count DESC;


-- ============================================================
-- Q6. REVIEW COVERAGE
-- Business Question:
-- How much of the dataset has review information?
-- ============================================================

SELECT
    CASE
        WHEN review_count IS NULL OR review_count = 0
            THEN 'No Reviews'
        ELSE 'Has Reviews'
    END AS review_status,
    COUNT(*) AS message_count,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM messages),
        2
    ) AS percentage
FROM messages
GROUP BY review_status
ORDER BY message_count DESC;


-- ============================================================
-- Q7. REVIEW RESULT DISTRIBUTION
-- Business Question:
-- What is the distribution of available review outcomes?
-- ============================================================

SELECT
    review_result,
    COUNT(*) AS message_count
FROM messages
WHERE review_result IS NOT NULL
GROUP BY review_result
ORDER BY message_count DESC;


-- ============================================================
-- Q8. SYNTHETIC VS NON-SYNTHETIC CONTENT
-- Business Question:
-- How much content is identified as synthetic?
-- ============================================================

SELECT
    synthetic,
    COUNT(*) AS message_count,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM messages),
        2
    ) AS percentage
FROM messages
GROUP BY synthetic
ORDER BY message_count DESC;


-- ============================================================
-- Q9. DELETED VS NON-DELETED MESSAGES
-- Business Question:
-- How much content is marked as deleted?
-- ============================================================

SELECT
    deleted,
    COUNT(*) AS message_count,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM messages),
        2
    ) AS percentage
FROM messages
GROUP BY deleted
ORDER BY message_count DESC;


-- ============================================================
-- Q10. MESSAGE ACTIVITY BY ROLE AND LANGUAGE
-- Business Question:
-- Which languages have the highest participation
-- across user/assistant roles?
-- ============================================================

SELECT
    lang,
    role,
    COUNT(*) AS message_count
FROM messages
WHERE lang IS NOT NULL
GROUP BY lang, role
ORDER BY message_count DESC
LIMIT 30;


-- ============================================================
-- Q11. MOST ACTIVE USERS
-- Business Question:
-- Which users contributed the most messages?
-- ============================================================

SELECT
    user_id,
    COUNT(*) AS message_count
FROM messages
WHERE user_id IS NOT NULL
GROUP BY user_id
ORDER BY message_count DESC
LIMIT 20;


-- ============================================================
-- Q12. CONVERSATION ACTIVITY OVER TIME
-- Business Question:
-- How does conversation activity change over time?
-- ============================================================

SELECT
    SUBSTR(created_date, 1, 7) AS year_month,
    COUNT(*) AS message_count,
    COUNT(DISTINCT message_tree_id) AS conversation_count
FROM messages
WHERE created_date IS NOT NULL
GROUP BY year_month
ORDER BY year_month;


-- ============================================================
-- Q13. AVERAGE CONVERSATION LENGTH
-- Business Question:
-- What is the average number of messages per conversation?
-- ============================================================

SELECT
    ROUND(
        AVG(message_count),
        2
    ) AS average_messages_per_conversation,

    MIN(message_count) AS minimum_messages,

    MAX(message_count) AS maximum_messages

FROM (
    SELECT
        message_tree_id,
        COUNT(*) AS message_count
    FROM messages
    GROUP BY message_tree_id
);


-- ============================================================
-- Q14. REVIEWED CONTENT BY ROLE
-- Business Question:
-- Which role receives more review activity?
-- ============================================================

SELECT
    role,
    COUNT(*) AS reviewed_messages
FROM messages
WHERE review_count IS NOT NULL
  AND review_count > 0
GROUP BY role
ORDER BY reviewed_messages DESC;


-- ============================================================
-- Q15. LANGUAGE QUALITY COVERAGE
-- Business Question:
-- Which languages have the highest review coverage?
-- ============================================================

SELECT
    lang,
    COUNT(*) AS total_messages,

    SUM(
        CASE
            WHEN review_count IS NOT NULL
             AND review_count > 0
            THEN 1
            ELSE 0
        END
    ) AS reviewed_messages,

    ROUND(
        SUM(
            CASE
                WHEN review_count IS NOT NULL
                 AND review_count > 0
                THEN 1
                ELSE 0
            END
        ) * 100.0 / COUNT(*),
        2
    ) AS review_coverage_percentage

FROM messages

WHERE lang IS NOT NULL

GROUP BY lang

HAVING COUNT(*) >= 100

ORDER BY review_coverage_percentage DESC;


-- ============================================================
-- Q16. FINAL DATA QUALITY SUMMARY
-- Business Question:
-- What is the current quality/completeness status of the
-- analytical database?
-- ============================================================

SELECT

    COUNT(*) AS total_records,

    SUM(
        CASE
            WHEN text IS NULL OR TRIM(text) = ''
            THEN 1
            ELSE 0
        END
    ) AS empty_text_records,

    SUM(
        CASE
            WHEN message_id IS NULL
            THEN 1
            ELSE 0
        END
    ) AS missing_message_ids,

    SUM(
        CASE
            WHEN lang IS NULL
            THEN 1
            ELSE 0
        END
    ) AS missing_language,

    SUM(
        CASE
            WHEN role IS NULL
            THEN 1
            ELSE 0
        END
    ) AS missing_role,

    SUM(
        CASE
            WHEN review_count IS NULL
            THEN 1
            ELSE 0
        END
    ) AS missing_review_count

FROM messages;