-- usp_BundleSalesReport — the data team's bundle reporting proc.
-- Inherited; the style is theirs. (Fully synthetic schema — illustrative only.)
CREATE PROC usp_BundleSalesReport @startDate date, @endDate date AS
;WITH bundle AS (
  SELECT o.ORDERID, o.ORDERDATE,
         ol.ORDERLINEID, ol.BUNDLEID,
         it.ITEMTYPEID,
         ol.ORDERLINEAMOUNT AS Amount,
         ol.ORDERLINEQTY    AS Qty
  FROM SALES_ORDER o
  JOIN ORDER_ITEM oi ON oi.ORDERID      = o.ORDERID
  JOIN ORDER_LINE ol ON ol.ORDERITEMID  = oi.ORDERITEMID
  JOIN ITEM_TYPE  it ON it.ITEMTYPEID    = ol.ITEMTYPEID
  WHERE ol.BUNDLEID IS NOT NULL                       -- bundles
    AND it.ITEMTYPEID NOT IN (8, 9, 12)               -- exclude fees / add-on lines / gift cards
    AND o.ORDERDATE BETWEEN @startDate AND @endDate
)
SELECT COUNT(DISTINCT ORDERID) AS BundleOrders,
       SUM(Qty)    AS Units,
       SUM(Amount) AS Revenue
FROM bundle;
