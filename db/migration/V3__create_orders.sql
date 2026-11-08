CREATE TABLE orders (
    id      SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    amount  NUMERIC(10, 2) NOT NULL
);