CREATE TABLE IF NOT EXISTS users (
    id          SERIAL PRIMARY KEY,
    username    TEXT UNIQUE NOT NULL,
    email       TEXT NOT NULL,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS orders (
    id          SERIAL PRIMARY KEY,
    user_id     INT REFERENCES users(id),
    amount      NUMERIC(10,2),
    status      TEXT DEFAULT 'pending',
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status  ON orders(status);

INSERT INTO users (username, email)
SELECT 'user_' || i, 'user_' || i || '@lab.com'
FROM generate_series(1, 100) AS i;

INSERT INTO orders (user_id, amount, status)
SELECT
    (random() * 99 + 1)::INT,
    round((random() * 500)::NUMERIC, 2),
    (ARRAY['pending','complete','failed'])[ceil(random()*3)]
FROM generate_series(1, 1000);
