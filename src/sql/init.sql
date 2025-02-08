create table if not exists users(
    id int primary key,
    password VARCHAR(512) NOT NULL,
    email VARCHAR(512) unique NOT NULL,
    gender VARCHAR(1) NOT NULL,
    first_name VARCHAR(512) NOT NULL,
    surname VARCHAR(512) NOT NULL,
    phone int unique NOT NULL,
    role VARCHAR(1) NOT NULL
);

create table if not exists muscles(
    id int primary key,
    title VARCHAR(512) NOT NULL,
    mgroup VARCHAR(512) NOT NULL,
    function VARCHAR(512) NOT NULL
);

create table if not exists gym(
    id int primary key,
    adress VARCHAR(512) NOT NULL,
    phone int NOT NULL,
    work_hours VARCHAR(512) NOT NULL
);

create table if not exists position(
    id int primary key,
    title VARCHAR(512) NOT NULL,
    experience int NOT NULL,
    function VARCHAR(512) NOT NULL
);

create table if not exists trainer(
    id int primary key,
    gender VARCHAR(1) NOT NULL,
    first_name VARCHAR(512) NOT NULL,
    surname VARCHAR(512) NOT NULL,
    number int NOT NULL,
    position_id int NOT NULL,
    foreign key (position_id) references position(id),
    gym_id int NOT NULL,
    foreign key (gym_id) references gym(id)
);

create table if not exists exercise(
    id int primary key,
    title VARCHAR(512) NOT NULL,
    muscles_id int NOT NULL,
    foreign key (muscles_id) references muscles(id),
    difficulty int NOT NULL
);

create table if not exists train(
    id int primary key,
    title VARCHAR(10) NOT NULL,
    dates VARCHAR(10) NOT NULL,
    times VARCHAR(5) NOT NULL,
    trainer_id int NOT NULL,
    foreign key (trainer_id) references trainer(id),
    gym_id int NOT NULL,
    foreign key (gym_id) references gym(id)
);

create table if not exists te_conn(
    train_id int NOT NULL,
    foreign key (train_id) references train(id),
    exercise_id int NOT NULL,
    foreign key (exercise_id) references exercise(id)
);

create table if not exists tu_conn(
    id int primary key,
    train_id int NOT NULL,
    foreign key (train_id) references train(id),
    users_id int NOT NULL,
    foreign key (users_id) references users(id)
);


CREATE OR REPLACE FUNCTION add_trainer()
RETURNS TRIGGER AS $$
DECLARE
    max_trainer_id INT;
BEGIN
    SELECT COALESCE(MAX(id), 0) + 1 INTO max_trainer_id FROM trainer;
    IF NEW.role = 't' THEN
        INSERT INTO trainer (id, gender, first_name, surname, number, position_id, gym_id)
        VALUES (max_trainer_id, NEW.gender, NEW.first_name, NEW.surname, NEW.phone, 1, 1);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER add_trainer_trigger
AFTER INSERT ON users
FOR EACH ROW
EXECUTE FUNCTION add_trainer();


drop trigger add_trainer_trigger on users


INSERT INTO users (id, password, email, gender, first_name, surname, phone, role)
VALUES (1, 'password123', 'example@email.com', 'm', 'Иван', 'Иванов', 12345, 't');



CREATE ROLE db_user;
CREATE ROLE db_trainer;
CREATE ROLE db_admin WITH LOGIN PASSWORD 'admin' CREATEDB CREATEROLE;
GRANT ALL PRIVILEGES ON DATABASE fitnes TO db_admin;

select from users where users.email = 'no-email';

DELETE FROM users WHERE id > 18;








