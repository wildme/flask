CREATE TABLE users
(id TINYINT UNSIGNED AUTO_INCREMENT,
    login VARCHAR(20),
    password_h VARCHAR(128),
    firstname VARCHAR(30),
    lastname VARCHAR(30),
    email VARCHAR(64),
    dep_id TINYINT UNSIGNED,
    CONSTRAINT pk_user PRIMARY KEY (id),
    CONSTRAINT fk_deps_id FOREIGN KEY (dep_id)
    REFERENCES departments (id)
);
CREATE TABLE departments
(id TINYINT UNSIGNED AUTO_INCREMENT,
    name VARCHAR(30),
    CONSTRAINT pk_deps PRIMARY KEY (id)
);
CREATE TABLE outbox
(id TINYINT UNSIGNED AUTO_INCREMENT,
    subject VARCHAR(256),
    reg_date DATETIME,
    recipient VARCHAR(128),
    user_id TINYINT UNSIGNED,
    notes VARCHAR(256),
    attachment VARCHAR(128),
    CONSTARINT pk_outbox PRIMARY KEY (id),
    CONSTRAINT fk_users_id FOREIGN KEY (user_id)
    REFERENCES users (id)
);
