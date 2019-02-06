INSERT  INTO consumer_attributes VALUES ('132131', NULL, NULL, NULL, NULL, NULL);

INSERT INTO face_encodings VALUES ('132131', ARRAY[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128])

INSERT INTO dish_attributes VALUES ('dish1');
INSERT INTO dish_attributes VALUES ('dish2');
INSERT INTO store_attributes VALUES ('store1', 10);
INSERT INTO store_menu VALUES ('store1', 'dish1', 20, 1);
INSERT INTO store_menu VALUES ('store1', 'dish2', 10, 2);


INSERT INTO dish_attributes VALUES ('dish3');
INSERT INTO dish_attributes VALUES ('dish4');
INSERT INTO store_menu VALUES ('store1', 'dish1', 'coffee', 'worlds best coffee', 'https://storage.googleapis.com/digital_menu/testing/store1/dish1.jpg', 'Beverage', 50.0, NULL, 4.6, 0);
INSERT INTO store_menu VALUES ('store1', 'dish2', 'coffee', 'worlds best coffee', 'https://storage.googleapis.com/digital_menu/testing/store1/dish1.jpg', 'Beverage', 50.0, NULL, 4.6, 1);
INSERT INTO store_menu VALUES ('store1', 'dish3', 'coffee', 'worlds best coffee', 'https://storage.googleapis.com/digital_menu/testing/store1/dish1.jpg', 'Beverage', 50.0, NULL, 4.6, 2);
INSERT INTO store_menu VALUES ('store1', 'dish4', 'coffee', 'worlds best coffee', 'https://storage.googleapis.com/digital_menu/testing/store1/dish1.jpg', 'Beverage', 50.0, NULL, 4.6, 3);
INSERT INTO dish_attributes VALUES ('dish5');
INSERT INTO dish_attributes VALUES ('dish6');
INSERT INTO dish_attributes VALUES ('dish7');
INSERT INTO dish_attributes VALUES ('dish8');

INSERT INTO store_menu VALUES ('store1', 'dish5', 'pancake', 'worlds best pancake', 'https://storage.googleapis.com/digital_menu/testing/store1/dish5.jpg', 'Snacks', 50.0, NULL, 4.6, 5);
INSERT INTO store_menu VALUES ('store1', 'dish6', 'pizza', 'worlds best pizza', 'https://storage.googleapis.com/digital_menu/testing/store1/dish6.jpg', 'Snacks', 50.0, NULL, 4.6, 6);
INSERT INTO store_menu VALUES ('store1', 'dish7', 'samosa', 'worlds best samosa', 'https://storage.googleapis.com/digital_menu/testing/store1/dish7.jpg', 'Snacks', 50.0, NULL, 4.6, 7);
INSERT INTO store_menu VALUES ('store1', 'dish8', 'burger', 'worlds best burger', 'https://storage.googleapis.com/digital_menu/testing/store1/dish8.jpg', 'Snacks', 50.0, NULL, 4.6, 8);




SELECT ConsumerId, distance(encodings, ARRAY[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128]) FROM consumer_faces ORDER BY distance(consumer_faces.encodings, ARRAY[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128]) DESC LIMIT 1
