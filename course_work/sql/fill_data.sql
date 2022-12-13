INSERT INTO planets_universe (name)
VALUES ('Minecraft'),
       ('Main universe');

INSERT INTO planets_planet (name, universe_id)
VALUES ('world', 1), -- 1
       ('earth', 2), -- 2
       ('rick`s station', 2); -- 3

INSERT INTO creatures_creature (name, power, planet_id, icon)
VALUES ('creeper', 100, 1,'https://www.giantbomb.com/a/uploads/original/3/34651/3407207-creepycreep.png'),             -- 1
       ('zombie', 50, 1, 'https://preview.redd.it/n3q3suk8hkn61.png?width=640&crop=smart&auto=webp&s=15b42d9eb1487d0cceae0c68a4347de4ec07a3e1'),               -- 2
       ('rick-from-minecraft', 80, 1, 'https://i.pinimg.com/originals/94/52/c6/9452c65d742722acfa293e85f8fe3978.jpg'),  -- 3
       ('morty-from-minecraft', 10, 1, 'https://openseauserdata.com/files/2668cfe8dbcd4e4f0b94ac0f66a38a78.png'), -- 4
       ('angry-rick', 110, 3,'https://sun9-37.userapi.com/impf/c858220/v858220608/bcb48/TSVbPyzUmEk.jpg?size=807x807&quality=96&sign=34de48794c709da2770cc68ed2c717a3&type=album'),          -- 5
       ('morty', 25, 2,'https://m.media-amazon.com/images/S/aplus-media-library-service-media/365e5edb-7b7f-415a-81c7-a848936e9e38.__CR0,0,300,300_PT0_SX300_V1___.jpg'),                -- 6
       ('nimbus', 150, 2,'https://www.looper.com/img/gallery/why-mr-nimbus-from-rick-and-morty-season-5-sounds-so-familiar/l-intro-1624299443.jpg'),              -- 7
       ('jerry', 75, 2,'https://i.pinimg.com/564x/58/5e/d3/585ed37dc0b06a6c455d5904f630372b.jpg'),                -- 8
       ('smart-rick', 111, 3,'https://www.soyuz.ru/public/uploads/files/3/7614199/20221115172240ac927631f6.jpg'),          -- 9
       ('old-rick', 65, 3,'https://cs8.pikabu.ru/post_img/2016/02/05/8/145467954719748335.jpg'); -- 10
INSERT INTO affects_weapon (name, power, icon)
VALUES ('diamond sword', 32, 'https://cdn.shopify.com/s/files/1/0318/2649/products/415cCM_2ByNsL._AC_SL1000.jpg?v=1632792655'),
       ('portal gun', 13, 'https://media.sketchfab.com/models/12d1962f1816435fbfd91f87d8f02532/thumbnails/843c05c901114e35b0e811e6e166fcd2/e9791261e0cd413ea6d267649b6244f8.jpeg'),
       ('blaster', 56, 'https://upload.wikimedia.org/wikipedia/commons/2/25/StormTrooper_Blaster.jpg'),
       ('BFG', 100, 'https://media.sketchfab.com/models/6eee147e8ad54844b0237249f6ff20f8/thumbnails/cbf3d02533ff407eafd14c14070599aa/6462710cf0094e80bacbe6d74990f02f.jpeg'),
       ('ANTI-BFG', -100, 'https://i.imgur.com/3grJzel.jpg');

INSERT INTO affects_effect (name, power_affect)
VALUES ('baff', 50), -- 1
       ('debaff', -50); -- 2
INSERT INTO affects_planeteffectrule (planet_id, creature_to_id, effect_id)
VALUES (2, 9, 2),
       (2, 10, 1),
       (2, 6, 1),
       (2, 5, 2),
       (2, 7, 1),
       (3, 9, 1),
       (3, 10, 1),
       (3, 5, 1),
       (3, 6, 2),
       (3, 8, 1);
INSERT INTO affects_creatureeffectrule (creature_from_id, creature_to_id, effect_id, is_to_ally)
VALUES (8, 6, 1, False),
       (8, 7, 1, False),
       (10, 8, 1, False),
       (8, 8, 1, False),
       (6, 8, 1, True),
       (7, 7, 1, True),
       (5, 10, 1, True),
       (5, 9, 2, False),
       (8, 9, 2, True),
       (3, 3, 2, True),
       (7, 10, 2, True),
       (1, 3, 1, True),
       (10, 10, 2, False),
       (5, 8, 1, True),
       (10, 6, 2, False),
       (4, 1, 2, False),
       (5, 9, 1, True),
       (10, 6, 1, False),
       (8, 10, 1, True),
       (9, 9, 1, True),
       (7, 5, 1, False),
       (6, 8, 1, False),
       (8, 6, 2, False),
       (4, 4, 1, False),
       (7, 8, 2, True),
       (10, 10, 1, True),
       (1, 3, 1, False),
       (1, 4, 1, False),
       (9, 8, 1, False),
       (4, 2, 2, False),
       (1, 2, 2, True),
       (9, 7, 2, False),
       (8, 7, 1, True),
       (7, 6, 2, False),
       (9, 9, 1, False),
       (8, 8, 1, True),
       (1, 3, 2, True),
       (5, 10, 2, False),
       (7, 9, 2, False),
       (5, 5, 1, False),
       (7, 10, 1, False),
       (7, 8, 1, True),
       (6, 7, 2, False),
       (7, 8, 2, False),
       (9, 5, 1, False),
       (1, 1, 2, True);




