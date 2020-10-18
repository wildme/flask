-- TABLE: users
CREATE TABLE users
(id TINYINT UNSIGNED AUTO_INCREMENT,
    login VARCHAR(20),
    password_h VARCHAR(128),
    firstname VARCHAR(30),
    lastname VARCHAR(30),
    administrator TINYINT(1),
    email VARCHAR(64),
    dep_id TINYINT UNSIGNED,
    CONSTRAINT pk_user PRIMARY KEY (id)
    );
-- TABLE: departments
CREATE TABLE departments
(id TINYINT UNSIGNED AUTO_INCREMENT,
    name VARCHAR(30),
    CONSTRAINT pk_deps PRIMARY KEY (id)
);
-- TABLE: outbox
CREATE TABLE outbox
(id TINYINT UNSIGNED AUTO_INCREMENT,
    subject VARCHAR(256),
    reg_date DATETIME,
    recipient VARCHAR(128),
    user_id TINYINT UNSIGNED,
    notes VARCHAR(256),
    attachment VARCHAR(128),
    CONSTRAINT pk_outbox PRIMARY KEY (id)
);
-- FOREIGN KEYS
-- Reference: fk_deps_id table: users
ALTER TABLE users ADD CONSTRAINT fk_deps_id
    FOREIGN KEY (dep_id)
    REFERENCES departments (id);
-- Reference: fk_users_id table: outbox
ALTER TABLE outbox ADD CONSTRAINT fk_users_id
    FOREIGN KEY (user_id)
    REFERENCES users (id);
-- INSERT VALUES
INSERT INTO users (login, firstname, lastname, administrator, email) VALUES ('admin', 'Admin', 'Admin', 1, "admin@example.com");  
