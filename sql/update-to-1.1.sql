-- Update db to v1.1
-- Sun, 7 Oct 2018, 16:55:55
-- Model: pyclub    Version: 1.1

USE 'pyclub';
ALTER TABLE user
    ADD UNIQUE (email);

ALTER TABLE event_membership
    CHANGE COLUMN event_club_idclub own_club_id int(11);