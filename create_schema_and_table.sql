-- CREATE SCHEMA IF NOT EXISTS hier_data_large;

# Create fact_metrics_large table

-- CREATE TABLE IF NOT EXISTS hier_data_large.fact_metrics_large (
--     dim1_market        VARCHAR(50),
--     dim2_country       VARCHAR(50),
--     dim3_region        VARCHAR(100),
--     dim4_city          VARCHAR(100),
--     m_purchase_intent  DECIMAL(5,4),
--     m_revenue          BIGINT,
--     m_share            DECIMAL(5,4),
--     m_avg_price        DECIMAL(10,2),
--     m_n                INT
-- );

# Add data to fact_metrics_large table

-- INSERT INTO hier_data_large.fact_metrics_large (
--     dim1_market, dim2_country, dim3_region, dim4_city,
--     m_purchase_intent, m_revenue, m_share, m_avg_price, m_n
-- ) VALUES
-- -- Europe
-- ('EU', 'DE', 'Bavaria', 'Munich',           0.62, 1250000, 0.2100, 49.90, 180),
-- ('EU', 'DE', 'Hamburg', 'Hamburg',          0.58, 1180000, 0.1900, 47.50, 160),
-- ('EU', 'FR', 'Île-de-France', 'Paris',      0.64, 1340000, 0.2200, 51.00, 170),
-- ('EU', 'FR', 'Occitanie', 'Toulouse',       0.59, 1020000, 0.1850, 46.40, 150),
-- ('EU', 'IT', 'Lombardy', 'Milan',           0.63, 1285000, 0.2150, 50.10, 175),
-- ('EU', 'ES', 'Catalonia', 'Barcelona',      0.61, 1220000, 0.2050, 48.30, 168),
-- ('EU', 'NL', 'North Holland', 'Amsterdam',  0.60, 1100000, 0.1950, 47.80, 158),

-- -- US
-- ('US', 'US', 'California', 'San Francisco', 0.68, 1900000, 0.2500, 59.00, 210),
-- ('US', 'US', 'California', 'Los Angeles',   0.66, 1750000, 0.2400, 57.50, 205),
-- ('US', 'US', 'New York', 'New York City',   0.67, 1850000, 0.2450, 58.20, 215),
-- ('US', 'US', 'Texas', 'Austin',             0.63, 1500000, 0.2100, 54.10, 190),
-- ('US', 'US', 'Illinois', 'Chicago',         0.64, 1605000, 0.2200, 55.80, 198),

-- -- APAC
-- ('APAC', 'JP', 'Kantō', 'Tokyo',            0.61, 1300000, 0.2000, 48.00, 190),
-- ('APAC', 'JP', 'Kansai', 'Osaka',           0.60, 1230000, 0.1950, 47.20, 185),
-- ('APAC', 'IN', 'Maharashtra', 'Mumbai',     0.58, 980000,  0.1800, 39.50, 220),
-- ('APAC', 'IN', 'Karnataka', 'Bengaluru',    0.59, 1025000, 0.1850, 41.00, 215),
-- ('APAC', 'AU', 'New South Wales', 'Sydney', 0.62, 1185000, 0.2050, 50.50, 175),
-- ('APAC', 'AU', 'Victoria', 'Melbourne',     0.61, 1150000, 0.1980, 49.80, 169),

-- -- LATAM
-- ('LATAM', 'BR', 'São Paulo', 'São Paulo',   0.57, 920000,  0.1700, 37.20, 210),
-- ('LATAM', 'MX', 'CDMX', 'Mexico City',      0.56, 880000,  0.1650, 36.10, 205);

# Add primary key to fact_metrics_large table
-- USE hier_data_large;

-- ALTER TABLE fact_metrics_large
--     ADD COLUMN fact_id INT AUTO_INCREMENT PRIMARY KEY FIRST;fact_metrics_large



# Create fact_campaign_metrics table

-- CREATE TABLE hier_data_large.fact_campaign_metrics (
--     campaign_id     BIGINT AUTO_INCREMENT PRIMARY KEY,
--     fact_id         INT NOT NULL,
--     campaign_name   VARCHAR(100) NOT NULL,
--     channel         VARCHAR(50)  NOT NULL,   -- e.g. TV, Online, OOH, Social
--     spend           DECIMAL(12,2) DEFAULT 0,
--     impressions     BIGINT        DEFAULT 0,
--     clicks          BIGINT        DEFAULT 0,
--     conversions     INT           DEFAULT 0,
--     start_date      DATE,
--     end_date        DATE,
--     
--     INDEX idx_fcm_fact_id (fact_id),
--     CONSTRAINT fk_fcm_fact
--         FOREIGN KEY (fact_id)
--         REFERENCES hier_data_large.fact_metrics_large (fact_id)
--         ON UPDATE CASCADE
--         ON DELETE RESTRICT
-- );

# Add data to fact_campaign_metrics table

-- INSERT INTO hier_data_large.fact_campaign_metrics
--     (fact_id, campaign_name, channel, spend, impressions, clicks, conversions, start_date, end_date)
-- VALUES
--     -- Munich
--     (1, 'DE Q2 Brand Relaunch',      'Online',   250000.00, 3200000, 210000,  18500, '2025-04-01', '2025-06-30'),
--     (1, 'DE TV Awareness Spring',    'TV',       310000.00, 5400000,  85000,  12000, '2025-03-15', '2025-05-15'),

--     -- Paris
--     (3, 'FR Paris Metro Takeover',   'OOH',      180000.00, 1900000,  25000,   4200, '2025-05-01', '2025-05-31'),
--     (3, 'FR Influencer Push Q2',     'Social',   130000.00, 2700000, 190000,  16500, '2025-04-10', '2025-06-10'),

--     -- Milan
--     (5, 'IT Fashion Week Partner',   'Sponsorship', 220000.00, 1100000,  18000,  3500, '2025-02-20', '2025-03-10'),
--     (5, 'IT Performance Always-On',  'Search',   95000.00,  900000,  98000,   8700, '2025-03-01', '2025-06-30'),

--     -- Barcelona
--     (6, 'ES Summer Launch Barcelona','Social',   140000.00, 2100000, 150000,  13200, '2025-06-01', '2025-07-31'),

--     -- Amsterdam
--     (7, 'NL Digital Only Test',      'Online',    80000.00, 1200000,  90000,   7600, '2025-04-01', '2025-05-15'),

--     -- San Francisco
--     (8, 'US West Coast Awareness',   'TV',       400000.00, 6500000, 110000,  15000, '2025-03-01', '2025-04-30'),
--     (8, 'US SF Performance Max',     'Online',   210000.00, 3500000, 260000,  23000, '2025-04-15', '2025-06-30'),

--     -- New York City
--     (10, 'US NYC Subway Domination', 'OOH',      260000.00, 3000000,  38000,   6400, '2025-05-01', '2025-05-31'),
--     (10, 'US NYC Social Video',      'Social',   190000.00, 4200000, 310000,  27500, '2025-04-10', '2025-06-10'),

--     -- Tokyo
--     (13, 'JP Golden Week Promo',     'Online',   150000.00, 2400000, 170000,  15000, '2025-04-20', '2025-05-10'),
--     (13, 'JP Rail Station Screens',  'OOH',      120000.00, 2000000,  22000,   3800, '2025-05-01', '2025-05-31'),

--     -- São Paulo
--     (19, 'BR Retail Co-op Campaign', 'TV',       130000.00, 3100000,  52000,   6200, '2025-03-15', '2025-04-30'),
--     (19, 'BR Social + Influencers',  'Social',    90000.00, 2200000, 180000,  15500, '2025-04-01', '2025-05-31');
    
    
# Add data to fact_segment_metrics table
    
-- INSERT INTO hier_data_large.fact_segment_metrics
--     (fact_id, segment_code, segment_label,
--      m_purchase_intent, m_share, m_avg_price, m_n)
-- VALUES
--     -- Munich (fact_id = 1, n = 180)
--     (1, 'AGE_18_34',  'Age 18–34',  0.68, 0.2400, 51.20, 70),
--     (1, 'AGE_35_54',  'Age 35–54',  0.61, 0.2100, 49.50, 75),
--     (1, 'AGE_55_PLUS','Age 55+',    0.54, 0.1700, 48.10, 35),

--     -- Paris (fact_id = 3, n = 170)
--     (3, 'AGE_18_34',  'Age 18–34',  0.70, 0.2500, 52.30, 65),
--     (3, 'AGE_35_54',  'Age 35–54',  0.64, 0.2250, 51.10, 70),
--     (3, 'AGE_55_PLUS','Age 55+',    0.56, 0.1850, 49.40, 35),

--     -- Milan (fact_id = 5, n = 175)
--     (5, 'HEAVY_USER', 'Heavy users', 0.76, 0.3100, 52.80, 60),
--     (5, 'MED_USER',   'Medium users',0.64, 0.2250, 50.00, 75),
--     (5, 'LIGHT_USER', 'Light users', 0.49, 0.1500, 47.90, 40),

--     -- Barcelona (fact_id = 6, n = 168)
--     (6, 'HEAVY_USER', 'Heavy users', 0.73, 0.2950, 50.20, 55),
--     (6, 'MED_USER',   'Medium users',0.62, 0.2150, 48.40, 70),
--     (6, 'LIGHT_USER', 'Light users', 0.48, 0.1500, 46.90, 43),

--     -- San Francisco (fact_id = 8, n = 210)
--     (8, 'INCOME_HIGH', 'High income', 0.74, 0.3100, 63.50, 80),
--     (8, 'INCOME_MID',  'Middle income',0.67,0.2450, 58.40, 90),
--     (8, 'INCOME_LOW',  'Low income',  0.58, 0.1950, 54.20, 40),

--     -- New York City (fact_id = 10, n = 215)
--     (10, 'INCOME_HIGH', 'High income', 0.75, 0.3200, 64.10, 85),
--     (10, 'INCOME_MID',  'Middle income',0.68,0.2500, 59.20, 95),
--     (10, 'INCOME_LOW',  'Low income',  0.57, 0.1800, 53.50, 35),

--     -- Tokyo (fact_id = 13, n = 190)
--     (13, 'AGE_18_34',  'Age 18–34',  0.66, 0.2250, 49.50, 70),
--     (13, 'AGE_35_54',  'Age 35–54',  0.60, 0.2050, 48.10, 80),
--     (13, 'AGE_55_PLUS','Age 55+',    0.53, 0.1700, 46.70, 40),

--     -- São Paulo (fact_id = 19, n = 210)
--     (19, 'HEAVY_USER', 'Heavy users', 0.65, 0.2600, 39.80, 75),
--     (19, 'MED_USER',   'Medium users',0.56, 0.1800, 37.10, 90),
--     (19, 'LIGHT_USER', 'Light users', 0.44, 0.1400, 35.00, 45);



# Create fact_segment_metrics table

-- CREATE TABLE hier_data_large.fact_segment_metrics (
--     segment_metric_id  BIGINT AUTO_INCREMENT PRIMARY KEY,
--     fact_id            INT NOT NULL,
--     segment_code       VARCHAR(50)  NOT NULL,   -- e.g. AGE_18_24, HEAVY_USER
--     segment_label      VARCHAR(100) NOT NULL,   -- human-readable
--     m_purchase_intent  DECIMAL(5,4),
--     m_share            DECIMAL(5,4),
--     m_avg_price        DECIMAL(10,2),
--     m_n                INT,
--     
--     INDEX idx_fsm_fact_id (fact_id),
--     CONSTRAINT fk_fsm_fact
--         FOREIGN KEY (fact_id)
--         REFERENCES hier_data_large.fact_metrics_large (fact_id)
--         ON UPDATE CASCADE
--         ON DELETE RESTRICT
-- );




