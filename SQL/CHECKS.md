# Оставил запросы для проверки работоспособности :)
---

### Кол-во строк
```SQL
SELECT 'stg.api_posts' AS table_name, COUNT(*) AS rows_count FROM stg.api_posts
UNION ALL
SELECT 'dds.hub_user', COUNT(*) FROM dds.hub_user
UNION ALL
SELECT 'dds.hub_post', COUNT(*) FROM dds.hub_post
UNION ALL
SELECT 'dds.link_user_post', COUNT(*) FROM dds.link_user_post
UNION ALL
SELECT 'dds.sat_post', COUNT(*) FROM dds.sat_post;
```

---

### Стэйдж
```SQL
SELECT *
FROM stg.api_posts
ORDER BY post_id
LIMIT 10;
```

---

### Линки
```SQL
SELECT 
    hu.user_id,
    hp.post_id,
    lup.user_post_hk
FROM dds.link_user_post lup
JOIN dds.hub_user hu 
    ON lup.user_hk = hu.user_hk
JOIN dds.hub_post hp 
    ON lup.post_hk = hp.post_hk
ORDER BY hp.post_id
LIMIT 20;
```

---

### Cателлит
```SQL
SELECT 
    hp.post_id,
    sp.title,
    sp.body,
    sp.hashdiff,
    sp.load_dttm,
    sp.source
FROM dds.sat_post sp
JOIN dds.hub_post hp
    ON sp.post_hk = hp.post_hk
ORDER BY hp.post_id
LIMIT 10;
```