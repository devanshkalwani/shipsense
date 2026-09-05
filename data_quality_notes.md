# Data Quality Notes — Shipsense

## Row counts
- orders: 99,441
- order_items: 112,650
- customers, order_payments, order_reviews, products, sellers, geolocation, 
  product_category_name_translation: loaded successfully, 9 tables total

## Missing values (orders table)
- order_delivered_customer_date: 2,965 missing
- order_approved_at: 160 missing
- order_estimated_delivery_date: 0 missing

These missing delivery dates are NOT a data error — they correspond almost 
exactly to the 2,963 non-delivered orders (shipped/canceled/processing/etc.), 
confirmed via the order_status breakdown below. Only ~2 rows are unexplained 
edge cases.

## Duplicate check
- No duplicate order_id values found in orders table.

## Referential integrity
- order_items -> orders: 0 orphans
- order_payments -> orders: 0 orphans
- order_reviews -> orders: 0 orphans
- order_items -> products: 0 orphans
- order_items -> sellers: 0 orphans

All foreign keys are clean — no broken references anywhere in the dataset.

## Order status breakdown
| Status      | Count  |
|-------------|--------|
| delivered   | 96,478 |
| shipped     | 1,107  |
| canceled    | 625    |
| unavailable | 609    |
| invoiced    | 314    |
| processing  | 301    |
| created     | 5      |
| approved    | 2      |

## Conclusion
Dataset is unusually clean for a real-world source — no duplicates, no broken 
foreign keys, and missing delivery dates are fully explained by order status. 
The only real "cleaning" needed downstream is filtering to order_status = 
'delivered' when calculating delay metrics, since non-delivered orders have 
no delivery date to compare against the estimate.