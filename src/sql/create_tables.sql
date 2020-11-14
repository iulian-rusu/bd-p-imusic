CREATE TABLE card_types (
    type_id  SMALLINT NOT NULL,
    name     VARCHAR2(16) NOT NULL
);

ALTER TABLE card_types ADD CHECK ( REGEXP_LIKE ( name,
                                                 '^[a-zA-Z0-9 ]+$' ) );

ALTER TABLE card_types ADD CONSTRAINT card_types_pk PRIMARY KEY ( type_id );

ALTER TABLE card_types ADD CONSTRAINT card_types_name_uk UNIQUE ( name );

CREATE TABLE music_albums (
    album_id      INTEGER NOT NULL,
    name          VARCHAR2(64) NOT NULL,
    price         NUMBER(5, 2) NOT NULL,
    release_date  DATE NOT NULL,
    artist_id     INTEGER NOT NULL
);

ALTER TABLE music_albums
    ADD CONSTRAINT album_name_ck CHECK ( REGEXP_LIKE ( name,
                                                       '^[a-zA-Z0-9 ,''.&!?\-]+$' ) );

ALTER TABLE music_albums ADD CONSTRAINT music_albums_pk PRIMARY KEY ( album_id );

CREATE TABLE music_artists (
    artist_id  INTEGER NOT NULL,
    name       VARCHAR2(64) NOT NULL
);

ALTER TABLE music_artists
    ADD CONSTRAINT artist_name_ck CHECK ( REGEXP_LIKE ( name,
                                                        '^[a-zA-Z0-9 ,''.&!?\-]+$' ) );

ALTER TABLE music_artists ADD CONSTRAINT music_artists_pk PRIMARY KEY ( artist_id );

CREATE TABLE music_genres (
    genre_id  SMALLINT NOT NULL,
    name      VARCHAR2(32) NOT NULL
);

ALTER TABLE music_genres
    ADD CONSTRAINT genre_name_ck CHECK ( REGEXP_LIKE ( name,
                                                       '^[a-zA-Z ]+$' ) );

ALTER TABLE music_genres ADD CONSTRAINT music_genres_pk PRIMARY KEY ( genre_id );

ALTER TABLE music_genres ADD CONSTRAINT music_genres_uk UNIQUE ( name );

CREATE TABLE payment_info (
    user_id          INTEGER NOT NULL,
    card_nr          CHAR(16) NOT NULL,
    expiration_date  DATE NOT NULL,
    account_balance  NUMBER(10, 2) NOT NULL,
    card_type_id     SMALLINT NOT NULL
);

ALTER TABLE payment_info ADD CONSTRAINT account_balance_ck CHECK ( account_balance >= 0 );

ALTER TABLE payment_info ADD CONSTRAINT payment_info_pk PRIMARY KEY ( user_id );

CREATE TABLE songs (
    song_id   INTEGER NOT NULL,
    name      VARCHAR2(64) NOT NULL,
    album_id  INTEGER NOT NULL,
    genre_id  SMALLINT NOT NULL
);

ALTER TABLE songs
    ADD CONSTRAINT song_name_ck CHECK ( REGEXP_LIKE ( name,
                                                      '^[a-zA-Z0-9 ,''.&!?\-]+$' ) );

ALTER TABLE songs ADD CONSTRAINT songs_pk PRIMARY KEY ( song_id );

CREATE TABLE transactions (
    tr_id     INTEGER NOT NULL,
    user_id   INTEGER NOT NULL,
    album_id  INTEGER NOT NULL,
    amount    NUMBER(5, 2) NOT NULL,
    "date"    DATE NOT NULL
);

ALTER TABLE transactions ADD CONSTRAINT transaction_amount_ck CHECK ( amount >= 0 );

ALTER TABLE transactions ADD CONSTRAINT transactions_pk PRIMARY KEY ( tr_id );

CREATE TABLE users (
    user_id     INTEGER NOT NULL,
    username    VARCHAR2(32) NOT NULL,
    first_name  VARCHAR2(64) NOT NULL,
    last_name   VARCHAR2(64) NOT NULL,
    password    VARCHAR2(64) NOT NULL,
    email       VARCHAR2(64)
);

ALTER TABLE users
    ADD CONSTRAINT username_ck CHECK ( REGEXP_LIKE ( username,
                                                     '^[a-zA-Z0-9_]+[.]?[a-zA-Z0-9_]+$' )
                                       AND length(username) >= 3 );

ALTER TABLE users
    ADD CONSTRAINT first_name_ck CHECK ( REGEXP_LIKE ( first_name,
                                                       '^[A-Z][a-z]+[ \-]?[A-Za-z]*$' )
                                         AND length(first_name) >= 2 );

ALTER TABLE users
    ADD CONSTRAINT last_name_ck CHECK ( REGEXP_LIKE ( last_name,
                                                      '^[A-Z][a-z]+[ \-]?[A-Za-z]*$' )
                                        AND length(last_name) >= 2 );

ALTER TABLE users
    ADD CONSTRAINT email_ck CHECK ( REGEXP_LIKE ( email,
                                                  '^[a-z0-9._%-]+@[a-z0-9._%-]+\.[a-z]{2,4}$' ) );

ALTER TABLE users ADD CONSTRAINT users_pk PRIMARY KEY ( user_id );

ALTER TABLE users ADD CONSTRAINT usersname_uk UNIQUE ( username,
                                                       email );

ALTER TABLE music_albums
    ADD CONSTRAINT music_albums_music_artists_fk FOREIGN KEY ( artist_id )
        REFERENCES music_artists ( artist_id );

ALTER TABLE payment_info
    ADD CONSTRAINT payment_info_card_types_fk FOREIGN KEY ( card_type_id )
        REFERENCES card_types ( type_id );

ALTER TABLE payment_info
    ADD CONSTRAINT payment_info_users_fk FOREIGN KEY ( user_id )
        REFERENCES users ( user_id );

ALTER TABLE songs
    ADD CONSTRAINT songs_music_albums_fk FOREIGN KEY ( album_id )
        REFERENCES music_albums ( album_id );

ALTER TABLE songs
    ADD CONSTRAINT songs_music_genres_fk FOREIGN KEY ( genre_id )
        REFERENCES music_genres ( genre_id );

ALTER TABLE transactions
    ADD CONSTRAINT transactions_music_albums_fk FOREIGN KEY ( album_id )
        REFERENCES music_albums ( album_id );

ALTER TABLE transactions
    ADD CONSTRAINT transactions_users_fk FOREIGN KEY ( user_id )
        REFERENCES users ( user_id );

CREATE SEQUENCE card_types_type_id_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER card_types_type_id_trg BEFORE
    INSERT ON card_types
    FOR EACH ROW
    WHEN ( new.type_id IS NULL )
BEGIN
    :new.type_id := card_types_type_id_seq.nextval;
END;
/

CREATE SEQUENCE music_albums_album_id_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER music_albums_album_id_trg BEFORE
    INSERT ON music_albums
    FOR EACH ROW
    WHEN ( new.album_id IS NULL )
BEGIN
    :new.album_id := music_albums_album_id_seq.nextval;
END;
/

CREATE SEQUENCE music_artists_artist_id_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER music_artists_artist_id_trg BEFORE
    INSERT ON music_artists
    FOR EACH ROW
    WHEN ( new.artist_id IS NULL )
BEGIN
    :new.artist_id := music_artists_artist_id_seq.nextval;
END;
/

CREATE SEQUENCE music_genres_genre_id_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER music_genres_genre_id_trg BEFORE
    INSERT ON music_genres
    FOR EACH ROW
    WHEN ( new.genre_id IS NULL )
BEGIN
    :new.genre_id := music_genres_genre_id_seq.nextval;
END;
/

CREATE SEQUENCE songs_song_id_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER songs_song_id_trg BEFORE
    INSERT ON songs
    FOR EACH ROW
    WHEN ( new.song_id IS NULL )
BEGIN
    :new.song_id := songs_song_id_seq.nextval;
END;
/

CREATE SEQUENCE transactions_tr_id_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER transactions_tr_id_trg BEFORE
    INSERT ON transactions
    FOR EACH ROW
    WHEN ( new.tr_id IS NULL )
BEGIN
    :new.tr_id := transactions_tr_id_seq.nextval;
END;
/

CREATE SEQUENCE users_user_id_seq START WITH 1 NOCACHE ORDER;

CREATE OR REPLACE TRIGGER users_user_id_trg BEFORE
    INSERT ON users
    FOR EACH ROW
    WHEN ( new.user_id IS NULL )
BEGIN
    :new.user_id := users_user_id_seq.nextval;
END;
/
 -- triggere pentru validarea datelor
CREATE OR REPLACE TRIGGER transactions_date_trg BEFORE
	INSERT OR UPDATE ON transactions
	FOR EACH ROW
BEGIN
	IF( :new."date" > SYSDATE )
	THEN
		RAISE_APPLICATION_ERROR( -20001,
		'Data invalida: ' || TO_CHAR( :new."date", 'DD.MM.YYYY HH24:MI:SS' ) || ' nu poate fi mai mare decat data curenta.' );
	END IF;
END;
/

CREATE OR REPLACE TRIGGER music_albums_release_date_trg BEFORE
	INSERT OR UPDATE ON music_albums
	FOR EACH ROW
BEGIN
	IF( :new.release_date > SYSDATE )
	THEN
		RAISE_APPLICATION_ERROR( -20001,
		'Data invalida: ' || TO_CHAR( :new.release_date, 'DD.MM.YYYY HH24:MI:SS' ) || ' nu poate fi mai mare decat data curenta.' );
	END IF;
END;
/

CREATE OR REPLACE TRIGGER payment_info_exp_date_trg BEFORE
	INSERT OR UPDATE ON payment_info
	FOR EACH ROW
BEGIN
	IF( :new.expiration_date <= SYSDATE )
	THEN
		RAISE_APPLICATION_ERROR( -20001,
		'Data invalida: ' || TO_CHAR( :new.expiration_date, 'DD.MM.YYYY HH24:MI:SS' ) || ' nu poate fi mai mica decat data curenta.' );
	END IF;
END;
/

