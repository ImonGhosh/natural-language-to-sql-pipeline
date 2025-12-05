-- SQL test queries for fact_metrics_large, fact_campaign_metrics, fact_segment_metrics

-- 1. All markets in a given country (simple filter, single table)
SELECT dim1_market, dim2_country, dim3_region, dim4_city, m_purchase_intent, m_revenue
FROM fact_metrics_large
WHERE dim2_country = 'Germany';

-- 2. Top 10 cities by revenue where sample size is large enough (single table, aggregation + filter + sort)
SELECT dim4_city,
       SUM(m_revenue) AS total_revenue,
       SUM(m_n)       AS total_sample
FROM fact_metrics_large
GROUP BY dim4_city
HAVING SUM(m_n) > 100
ORDER BY total_revenue DESC
LIMIT 10;

-- 3. Average purchase intent per country (single table, group by)
SELECT dim2_country,
       AVG(m_purchase_intent) AS avg_purchase_intent
FROM fact_metrics_large
GROUP BY dim2_country
ORDER BY avg_purchase_intent DESC;

-- 4. Total campaign spend and impressions per channel (campaign table only)
SELECT channel,
       SUM(spend)       AS total_spend,
       SUM(impressions) AS total_impressions
FROM fact_campaign_metrics
GROUP BY channel
ORDER BY total_spend DESC;

-- 5. Total conversions and revenue by country (join campaigns to markets)
SELECT f.dim2_country,
       SUM(c.conversions) AS total_conversions,
       SUM(f.m_revenue)   AS total_revenue
FROM fact_metrics_large f
JOIN fact_campaign_metrics c ON f.fact_id = c.fact_id
GROUP BY f.dim2_country
ORDER BY total_conversions DESC;

-- 6. Number of campaigns per city and total spend (join, aggregation)
SELECT f.dim4_city,
       COUNT(DISTINCT c.campaign_name) AS num_campaigns,
       SUM(c.spend)                    AS total_spend
FROM fact_metrics_large f
JOIN fact_campaign_metrics c ON f.fact_id = c.fact_id
GROUP BY f.dim4_city
ORDER BY num_campaigns DESC, total_spend DESC;

-- 7. Campaigns active in a given date range (campaign table, date filter)
SELECT campaign_name,
       channel,
       start_date,
       end_date,
       fact_id
FROM fact_campaign_metrics
WHERE start_date <= DATE '2025-06-30'
  AND end_date   >= DATE '2025-06-01';

-- 8. Average purchase intent for each segment across all markets (segment table)
SELECT segment_code,
       segment_label,
       AVG(m_purchase_intent) AS avg_segment_purchase_intent,
       SUM(m_n)               AS total_segment_sample
FROM fact_segment_metrics
GROUP BY segment_code, segment_label
ORDER BY avg_segment_purchase_intent DESC;

-- 9. Markets where AGE_18_24 segment purchase intent is higher than overall market (join segments to main)
SELECT f.dim1_market,
       f.dim2_country,
       f.dim3_region,
       f.dim4_city,
       f.m_purchase_intent      AS overall_purchase_intent,
       s.m_purchase_intent      AS age_18_24_purchase_intent
FROM fact_metrics_large f
JOIN fact_segment_metrics s ON f.fact_id = s.fact_id
WHERE s.segment_code = 'AGE_18_24'
  AND s.m_purchase_intent > f.m_purchase_intent
ORDER BY (s.m_purchase_intent - f.m_purchase_intent) DESC;

-- 10. Number of segments tracked per city and total segment sample size (segments + main)
SELECT f.dim4_city,
       COUNT(DISTINCT s.segment_code) AS num_segments,
       SUM(s.m_n)                     AS total_segment_sample
FROM fact_metrics_large f
JOIN fact_segment_metrics s ON f.fact_id = s.fact_id
GROUP BY f.dim4_city
ORDER BY num_segments DESC;

-- 11. Online campaign spend for HEAVY_USER segments by country (join all three tables)
SELECT f.dim2_country,
       SUM(c.spend)             AS total_online_spend,
       AVG(s.m_purchase_intent) AS avg_heavy_user_purchase_intent,
       SUM(s.m_n)               AS heavy_user_sample
FROM fact_metrics_large f
JOIN fact_campaign_metrics c ON f.fact_id = c.fact_id
JOIN fact_segment_metrics s ON f.fact_id = s.fact_id
WHERE c.channel = 'Online'
  AND s.segment_code = 'HEAVY_USER'
GROUP BY f.dim2_country
ORDER BY total_online_spend DESC;

-- 12. Cities whose average purchase intent is above the global average (subquery)
SELECT dim4_city,
       AVG(m_purchase_intent) AS avg_city_purchase_intent
FROM fact_metrics_large
GROUP BY dim4_city
HAVING AVG(m_purchase_intent) >
       (SELECT AVG(m_purchase_intent)
        FROM fact_metrics_large)
ORDER BY avg_city_purchase_intent DESC;

-- 13. Countries with large total sample size and strong share (HAVING with multiple conditions)
SELECT dim2_country,
       SUM(m_n)     AS total_sample,
       AVG(m_share) AS avg_share
FROM fact_metrics_large
GROUP BY dim2_country
HAVING SUM(m_n) > 1000
   AND AVG(m_share) > 0.20
ORDER BY avg_share DESC;

-- 14. Rank cities by revenue within each country (window function)
SELECT dim2_country,
       dim4_city,
       SUM(m_revenue) AS total_revenue,
       RANK() OVER (PARTITION BY dim2_country
                    ORDER BY SUM(m_revenue) DESC) AS revenue_rank_in_country
FROM fact_metrics_large
GROUP BY dim2_country, dim4_city;

-- 15. Most recent campaign per city with that city's KPIs (join + derived table)
SELECT f.dim4_city,
       c.campaign_name,
       c.start_date,
       f.m_purchase_intent,
       f.m_share,
       f.m_revenue
FROM fact_metrics_large f
JOIN fact_campaign_metrics c ON f.fact_id = c.fact_id
JOIN (
    SELECT fact_id, MAX(start_date) AS max_start_date
    FROM fact_campaign_metrics
    GROUP BY fact_id
) latest ON c.fact_id = latest.fact_id
       AND c.start_date = latest.max_start_date;
