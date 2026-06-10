CREATE TABLE ORDERS (order_id INT PRIMARY KEY, customer_id INT, order_date DATE, amount DECIMAL(12,2));
CREATE VIEW vw_orders_paid AS
SELECT o.order_id, o.amount, p.paid_at
FROM ORDERS o JOIN PAYMENTS p ON p.order_id = o.order_id;
CREATE VIEW vw_daily_rev AS
SELECT * FROM ORDERS;
CREATE VIEW rev_summary AS
SELECT order_date, SUM(amount) AS revenue FROM vw_daily_rev GROUP BY order_date;
