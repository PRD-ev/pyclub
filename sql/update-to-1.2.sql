-- Update db to v1.2 from v1.1
-- Sun, 30 Oct 2018, 08:28:55
-- Model: pyclub    Version: 1.2

ALTER TABLE event_membership
    DROP FOREIGN KEY fk_user_has_event_event1;

ALTER TABLE event_membership
    DROP COLUMN own_club_id;

ALTER TABLE user
    ALTER email_confirm SET DEFAULT 0;