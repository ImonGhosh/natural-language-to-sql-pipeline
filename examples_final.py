examples = [
    {
        "input": "Which region has the highest profit share across all locations?",
        "query": "SELECT dim3_region, m_share\n"
                 "FROM fact_metrics_large\n"
                 "ORDER BY m_share DESC\n"
                 "LIMIT 1;"
    },
    {
        "input": "List the top 5 cities by total revenue, highest first.",
        "query": "SELECT dim4_city, SUM(m_revenue) AS total_revenue\n"
                 "FROM fact_metrics_large\n"
                 "GROUP BY dim4_city\n"
                 "ORDER BY total_revenue DESC\n"
                 "LIMIT 5;"
    },
    {
        "input": "How does revenue look by country in the European market?",
        "query": "SELECT dim2_country, SUM(m_revenue) AS total_revenue\n"
                 "FROM fact_metrics_large\n"
                 "WHERE dim1_market = 'EU'\n"
                 "GROUP BY dim2_country\n"
                 "ORDER BY total_revenue DESC;"
    },
    {
        "input": "Give me total revenue per market, aggregated over all countries and cities.",
        "query": "SELECT dim1_market, SUM(m_revenue) AS total_revenue\n"
                 "FROM fact_metrics_large\n"
                 "GROUP BY dim1_market\n"
                 "ORDER BY total_revenue DESC;"
    },
    {
        "input": "For Germany, show average purchase intent by city.",
        "query": "SELECT dim4_city, AVG(m_purchase_intent) AS avg_purchase_intent\n"
                 "FROM fact_metrics_large\n"
                 "WHERE dim2_country = 'DE'\n"
                 "GROUP BY dim4_city\n"
                 "ORDER BY avg_purchase_intent DESC;"
    },
    {
        "input": "Compare average purchase intent across markets. Which market scores highest on intent?",
        "query": "SELECT dim1_market, AVG(m_purchase_intent) AS avg_purchase_intent\n"
                 "FROM fact_metrics_large\n"
                 "GROUP BY dim1_market\n"
                 "ORDER BY avg_purchase_intent DESC;"
    },
    {
        "input": "Show all cities in France where purchase intent is above 0.6 and sample size is at least 150.",
        "query": "SELECT dim4_city, m_purchase_intent, m_n\n"
                 "FROM fact_metrics_large\n"
                 "WHERE dim2_country = 'FR'\n"
                 "  AND m_purchase_intent > 0.6\n"
                 "  AND m_n >= 150\n"
                 "ORDER BY m_purchase_intent DESC;"
    },
    {
        "input": "What is the weighted average price by region, using m_n as weights?",
        "query": "SELECT dim3_region,\n"
                 "       SUM(m_avg_price * m_n) / NULLIF(SUM(m_n), 0) AS weighted_avg_price\n"
                 "FROM fact_metrics_large\n"
                 "GROUP BY dim3_region\n"
                 "ORDER BY weighted_avg_price DESC;"
    },
    {
        "input": "How big is each market in terms of total revenue share of the whole dataset?",
        "query": "SELECT dim1_market,\n"
                 "       SUM(m_revenue) AS total_revenue,\n"
                 "       SUM(m_revenue) / NULLIF((SELECT SUM(m_revenue) FROM fact_metrics_large), 0) AS revenue_share_of_total\n"
                 "FROM fact_metrics_large\n"
                 "GROUP BY dim1_market\n"
                 "ORDER BY revenue_share_of_total DESC;"
    },
    {
        "input": "Within each market, what share of revenue does each country contribute?",
        "query": "SELECT fm.dim1_market,\n"
                 "       fm.dim2_country,\n"
                 "       SUM(fm.m_revenue) AS country_revenue,\n"
                 "       SUM(fm.m_revenue) / NULLIF(SUM(SUM(fm.m_revenue)) OVER (PARTITION BY fm.dim1_market), 0) AS revenue_share_in_market\n"
                 "FROM fact_metrics_large AS fm\n"
                 "GROUP BY fm.dim1_market, fm.dim2_country\n"
                 "ORDER BY fm.dim1_market, revenue_share_in_market DESC;"
    },
    {
        "input": "Drill down Germany: show revenue by region and then by city inside Germany.",
        "query": "SELECT dim2_country,\n"
                 "       dim3_region,\n"
                 "       dim4_city,\n"
                 "       SUM(m_revenue) AS total_revenue\n"
                 "FROM fact_metrics_large\n"
                 "WHERE dim2_country = 'DE'\n"
                 "GROUP BY dim2_country, dim3_region, dim4_city\n"
                 "ORDER BY dim3_region, total_revenue DESC;"
    },
    {
        "input": "Roll up the hierarchy and give me average purchase intent by market only (ignore lower levels).",
        "query": "SELECT dim1_market, AVG(m_purchase_intent) AS avg_purchase_intent\n"
                 "FROM fact_metrics_large\n"
                 "GROUP BY dim1_market\n"
                 "ORDER BY avg_purchase_intent DESC;"
    },
    {
        "input": "For a quick overview, list total revenue and average price per country.",
        "query": "SELECT dim2_country,\n"
                 "       SUM(m_revenue) AS total_revenue,\n"
                 "       AVG(m_avg_price) AS avg_price\n"
                 "FROM fact_metrics_large\n"
                 "GROUP BY dim2_country\n"
                 "ORDER BY total_revenue DESC;"
    },
    {
        "input": "Show the full hierarchy for Munich, with all metrics.",
        "query": "SELECT dim1_market,\n"
                 "       dim2_country,\n"
                 "       dim3_region,\n"
                 "       dim4_city,\n"
                 "       m_purchase_intent,\n"
                 "       m_revenue,\n"
                 "       m_share,\n"
                 "       m_avg_price,\n"
                 "       m_n\n"
                 "FROM fact_metrics_large\n"
                 "WHERE dim4_city = 'Munich';"
    },
    {
        "input": "Count how many distinct cities we have per country.",
        "query": "SELECT dim2_country,\n"
                 "       COUNT(DISTINCT dim4_city) AS city_count\n"
                 "FROM fact_metrics_large\n"
                 "GROUP BY dim2_country\n"
                 "ORDER BY city_count DESC;"
    },
    {
        "input": "Which city has the highest revenue but only among those with purchase intent at least 0.65?",
        "query": "SELECT dim4_city, m_revenue, m_purchase_intent\n"
                 "FROM fact_metrics_large\n"
                 "WHERE m_purchase_intent >= 0.65\n"
                 "ORDER BY m_revenue DESC\n"
                 "LIMIT 1;"
    },
    {
        "input": "Within each country, list the top 3 cities by revenue.",
        "query": "WITH ranked AS (\n"
                 "    SELECT dim2_country,\n"
                 "           dim4_city,\n"
                 "           SUM(m_revenue) AS total_revenue,\n"
                 "           ROW_NUMBER() OVER (PARTITION BY dim2_country ORDER BY SUM(m_revenue) DESC) AS rn\n"
                 "    FROM fact_metrics_large\n"
                 "    GROUP BY dim2_country, dim4_city\n"
                 ")\n"
                 "SELECT dim2_country, dim4_city, total_revenue\n"
                 "FROM ranked\n"
                 "WHERE rn <= 3\n"
                 "ORDER BY dim2_country, total_revenue DESC;"
    },
    {
        "input": "Give me markets where the average purchase intent is below 0.6 but the total sample size m_n is above 500.",
        "query": "SELECT dim1_market,\n"
                 "       AVG(m_purchase_intent) AS avg_purchase_intent,\n"
                 "       SUM(m_n) AS total_n\n"
                 "FROM fact_metrics_large\n"
                 "GROUP BY dim1_market\n"
                 "HAVING AVG(m_purchase_intent) < 0.6\n"
                 "   AND SUM(m_n) > 500\n"
                 "ORDER BY avg_purchase_intent ASC;"
    },
    {
        "input": "Show average purchase intent and average share by region, only for cities where avg price is above 50.",
        "query": "SELECT dim3_region,\n"
                 "       AVG(m_purchase_intent) AS avg_purchase_intent,\n"
                 "       AVG(m_share) AS avg_share\n"
                 "FROM fact_metrics_large\n"
                 "WHERE m_avg_price > 50\n"
                 "GROUP BY dim3_region\n"
                 "ORDER BY avg_purchase_intent DESC;"
    },
    {
        "input": "For APAC, show revenue by country and region together, grouped at that level.",
        "query": "SELECT dim2_country,\n"
                 "       dim3_region,\n"
                 "       SUM(m_revenue) AS total_revenue\n"
                 "FROM fact_metrics_large\n"
                 "WHERE dim1_market = 'APAC'\n"
                 "GROUP BY dim2_country, dim3_region\n"
                 "ORDER BY dim2_country, total_revenue DESC;"
    },
    {
        "input": "Which market has the highest average selling price overall?",
        "query": "SELECT dim1_market,\n"
                 "       AVG(m_avg_price) AS avg_price\n"
                 "FROM fact_metrics_large\n"
                 "GROUP BY dim1_market\n"
                 "ORDER BY avg_price DESC\n"
                 "LIMIT 1;"
    },
    {
        "input": "Across all locations, what is the overall weighted purchase intent using m_n as weights?",
        "query": "SELECT SUM(m_purchase_intent * m_n) / NULLIF(SUM(m_n), 0) AS overall_weighted_purchase_intent\n"
                 "FROM fact_metrics_large;"
    },
    {
        "input": "Show a simple roll-up table: market, country, region, city and total revenue at that exact grain.",
        "query": "SELECT dim1_market,\n"
                 "       dim2_country,\n"
                 "       dim3_region,\n"
                 "       dim4_city,\n"
                 "       SUM(m_revenue) AS total_revenue\n"
                 "FROM fact_metrics_large\n"
                 "GROUP BY dim1_market, dim2_country, dim3_region, dim4_city\n"
                 "ORDER BY dim1_market, dim2_country, dim3_region, dim4_city;"
    },
    {
        "input": "For each city, what is the total campaign spend and the overall purchase intent in that city?",
        "query": "SELECT f.dim4_city,\n"
                 "       SUM(c.spend) AS total_campaign_spend,\n"
                 "       AVG(f.m_purchase_intent) AS avg_purchase_intent\n"
                 "FROM fact_metrics_large f\n"
                 "JOIN fact_campaign_metrics c ON f.fact_id = c.fact_id\n"
                 "GROUP BY f.dim4_city\n"
                 "ORDER BY total_campaign_spend DESC;"
    },
    {
        "input": "List the top 5 campaigns by conversions, including the city and the market's revenue where they ran.",
        "query": "SELECT c.campaign_name,\n"
                 "       f.dim4_city,\n"
                 "       f.m_revenue,\n"
                 "       SUM(c.conversions) AS total_conversions\n"
                 "FROM fact_campaign_metrics c\n"
                 "JOIN fact_metrics_large f ON c.fact_id = f.fact_id\n"
                 "GROUP BY c.campaign_name, f.dim4_city, f.m_revenue\n"
                 "ORDER BY total_conversions DESC\n"
                 "LIMIT 5;"
    },
    {
        "input": "For each country, how many campaigns ran in total and what was the total market revenue for those countries?",
        "query": "SELECT f.dim2_country,\n"
                 "       COUNT(DISTINCT c.campaign_name) AS num_campaigns,\n"
                 "       SUM(f.m_revenue) AS total_revenue\n"
                 "FROM fact_metrics_large f\n"
                 "JOIN fact_campaign_metrics c ON f.fact_id = c.fact_id\n"
                 "GROUP BY f.dim2_country\n"
                 "ORDER BY total_revenue DESC;"
    },
    {
        "input": "Show the average purchase intent for the AGE_18_24 segment by city, only where this segment exists.",
        "query": "SELECT f.dim4_city,\n"
                 "       AVG(s.m_purchase_intent) AS avg_purchase_intent_age_18_24\n"
                 "FROM fact_metrics_large f\n"
                 "JOIN fact_segment_metrics s ON f.fact_id = s.fact_id\n"
                 "WHERE s.segment_code = 'AGE_18_24'\n"
                 "GROUP BY f.dim4_city\n"
                 "ORDER BY avg_purchase_intent_age_18_24 DESC;"
    },
    {
        "input": "In which markets does the AGE_18_24 segment have higher purchase intent than the overall market?",
        "query": "SELECT f.dim1_market,\n"
                 "       f.dim2_country,\n"
                 "       f.dim3_region,\n"
                 "       f.dim4_city,\n"
                 "       f.m_purchase_intent AS overall_purchase_intent,\n"
                 "       s.m_purchase_intent AS segment_purchase_intent\n"
                 "FROM fact_metrics_large f\n"
                 "JOIN fact_segment_metrics s ON f.fact_id = s.fact_id\n"
                 "WHERE s.segment_code = 'AGE_18_24'\n"
                 "  AND s.m_purchase_intent > f.m_purchase_intent\n"
                 "ORDER BY segment_purchase_intent - overall_purchase_intent DESC;"
    },
    {
        "input": "For each city, how many customer segments are tracked and what is the total segment sample size?",
        "query": "SELECT f.dim4_city,\n"
                 "       COUNT(DISTINCT s.segment_code) AS num_segments,\n"
                 "       SUM(s.m_n) AS total_segment_sample\n"
                 "FROM fact_metrics_large f\n"
                 "JOIN fact_segment_metrics s ON f.fact_id = s.fact_id\n"
                 "GROUP BY f.dim4_city\n"
                 "ORDER BY num_segments DESC;"
    },
    {
        "input": "For each region, what is the total Online channel campaign spend and the average purchase intent for HEAVY_USER segments?",
        "query": "SELECT f.dim3_region,\n"
                 "       SUM(c.spend) AS total_online_spend,\n"
                 "       AVG(s.m_purchase_intent) AS avg_heavy_user_purchase_intent\n"
                 "FROM fact_metrics_large f\n"
                 "JOIN fact_campaign_metrics c ON f.fact_id = c.fact_id\n"
                 "JOIN fact_segment_metrics s ON f.fact_id = s.fact_id\n"
                 "WHERE c.channel = 'Online'\n"
                 "  AND s.segment_code = 'HEAVY_USER'\n"
                 "GROUP BY f.dim3_region\n"
                 "ORDER BY total_online_spend DESC;"
    },
    {
        "input": "List cities where campaigns were active but no segment-level data is available.",
        "query": "SELECT DISTINCT f.dim4_city\n"
                 "FROM fact_metrics_large f\n"
                 "JOIN fact_campaign_metrics c ON f.fact_id = c.fact_id\n"
                 "LEFT JOIN fact_segment_metrics s ON f.fact_id = s.fact_id\n"
                 "WHERE s.fact_id IS NULL\n"
                 "ORDER BY f.dim4_city;"
    },
    {
        "input": "For each campaign channel, what is the average revenue of the markets where they ran and how many campaigns used that channel?",
        "query": "SELECT c.channel,\n"
                 "       COUNT(DISTINCT c.campaign_name) AS num_campaigns,\n"
                 "       AVG(f.m_revenue) AS avg_market_revenue\n"
                 "FROM fact_campaign_metrics c\n"
                 "JOIN fact_metrics_large f ON c.fact_id = f.fact_id\n"
                 "GROUP BY c.channel\n"
                 "ORDER BY avg_market_revenue DESC;"
    },
    {
        "input": "For each city, show the most recent campaign (by start_date) along with the city's purchase intent and share.",
        "query": "SELECT f.dim4_city,\n"
                 "       c.campaign_name,\n"
                 "       c.start_date,\n"
                 "       f.m_purchase_intent,\n"
                 "       f.m_share\n"
                 "FROM fact_metrics_large f\n"
                 "JOIN fact_campaign_metrics c ON f.fact_id = c.fact_id\n"
                 "JOIN (\n"
                 "    SELECT fact_id, MAX(start_date) AS max_start_date\n"
                 "    FROM fact_campaign_metrics\n"
                 "    GROUP BY fact_id\n"
                 ") latest ON c.fact_id = latest.fact_id AND c.start_date = latest.max_start_date;"
    }
]

from langchain_community.vectorstores import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
import streamlit as st

@st.cache_resource
def get_example_selector():
    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples,
        OpenAIEmbeddings(),
        Chroma,
        k=3,
        input_keys=["input"],
    )
    return example_selector