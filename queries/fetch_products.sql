SELECT id, title, price, image_url, description 
FROM products 
WHERE is_searchable = 1 AND is_deleted = 0 AND is_hidden = 0
