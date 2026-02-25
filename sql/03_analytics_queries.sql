-- ============================================================
-- TELEGRAM ANALYTICS (ATHENA)
-- Table: telegram
-- ============================================================

-- 1) Quantidade de mensagens por dia
SELECT
  context_date,
  COUNT(1) AS message_amount
FROM telegram
GROUP BY context_date
ORDER BY context_date DESC;


-- 2) Quantidade de mensagens por usuário por dia
SELECT
  user_id,
  user_first_name,
  context_date,
  COUNT(1) AS message_amount
FROM telegram
GROUP BY
  user_id,
  user_first_name,
  context_date
ORDER BY context_date DESC;


-- 3) Média do tamanho das mensagens por usuário por dia
SELECT
  user_id,
  user_first_name,
  context_date,
  CAST(AVG(LENGTH(text)) AS INT) AS average_message_length
FROM telegram
GROUP BY
  user_id,
  user_first_name,
  context_date
ORDER BY context_date DESC;


-- 4) Quantidade de mensagens por hora / dia da semana / número da semana
WITH parsed_date_cte AS (
  SELECT
    *,
    CAST(date_format(from_unixtime("date"), '%Y-%m-%d %H:%i:%s') AS timestamp) AS parsed_date
  FROM telegram
),
hour_week_cte AS (
  SELECT
    *,
    EXTRACT(hour FROM parsed_date) AS parsed_date_hour,
    EXTRACT(dow FROM parsed_date) AS parsed_date_weekday,
    EXTRACT(week FROM parsed_date) AS parsed_date_weeknum
  FROM parsed_date_cte
)
SELECT
  parsed_date_hour,
  parsed_date_weekday,
  parsed_date_weeknum,
  COUNT(1) AS message_amount
FROM hour_week_cte
GROUP BY
  parsed_date_hour,
  parsed_date_weekday,
  parsed_date_weeknum
ORDER BY
  parsed_date_weeknum,
  parsed_date_weekday,
  parsed_date_hour;


-- 5) Palavras mais faladas do grupo (word frequency)
-- Observações:
-- - Remove pontuação e coloca em lowercase
-- - Ignora texto nulo e tokens vazios
-- - Opcional: filtre stopwords (eu deixei um exemplo comentado)
WITH cleaned AS (
  SELECT
    regexp_replace(lower(coalesce(text, '')), '[^a-zà-ú0-9\\s]', '') AS clean_text
  FROM telegram
  WHERE text IS NOT NULL
),
tokens AS (
  SELECT
    word
  FROM cleaned
  CROSS JOIN UNNEST(split(clean_text, ' ')) AS t(word)
  WHERE word <> ''
  -- AND word NOT IN ('de','da','do','e','a','o','que','pra','para','com','um','uma','na','no','em')
)
SELECT
  word AS palavra,
  COUNT(1) AS total
FROM tokens
GROUP BY word
ORDER BY total DESC
LIMIT 50;
