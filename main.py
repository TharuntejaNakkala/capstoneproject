lms-backend/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── permissions.py
│   │   ├── exceptions.py
│   │   └── constants.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   ├── session.py
│   │   └── init_db.py
│   │
│   ├── models/
│   │   ├── user_model.py
│   │   ├── role_model.py
│   │   ├── student_model.py
│   │   ├── faculty_model.py
│   │   ├── course_model.py
│   │   ├── enrollment_model.py
│   │   ├── assignment_model.py
│   │   ├── quiz_model.py
│   │   ├── question_model.py
│   │   ├── result_model.py
│   │   └── audit_log_model.py
│   │
│   ├── schemas/
│   │   ├── auth_schema.py
│   │   ├── user_schema.py
│   │   ├── student_schema.py
│   │   ├── faculty_schema.py
│   │   ├── course_schema.py
│   │   ├── enrollment_schema.py
│   │   ├── quiz_schema.py
│   │   ├── result_schema.py
│   │   └── ai_schema.py
│   │
│   ├── repositories/
│   │   ├── user_repository.py
│   │   ├── course_repository.py
│   │   ├── enrollment_repository.py
│   │   ├── quiz_repository.py
│   │   └── result_repository.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── student_service.py
│   │   ├── faculty_service.py
│   │   ├── course_service.py
│   │   ├── enrollment_service.py
│   │   ├── quiz_service.py
│   │   ├── result_service.py
│   │   ├── report_service.py
│   │   └── ai_service.py
│   │
│   ├── api/
│   │   ├── v1/
│   │   │   ├── routes/
│   │   │   │   ├── auth_routes.py
│   │   │   │   ├── user_routes.py
│   │   │   │   ├── student_routes.py
│   │   │   │   ├── faculty_routes.py
│   │   │   │   ├── course_routes.py
│   │   │   │   ├── enrollment_routes.py
│   │   │   │   ├── quiz_routes.py
│   │   │   │   ├── result_routes.py
│   │   │   │   ├── report_routes.py
│   │   │   │   └── ai_routes.py
│   │   │   │
│   │   │   └── api_router.py
│   │
│   ├── ai/
│   │   ├── tutor.py
│   │   ├── quiz_generator.py
│   │   ├── course_summarizer.py
│   │   ├── rag_assistant.py
│   │   ├── vector_store.py
│   │   └── prompts.py
│   │
│   ├── utils/
│   │   ├── password_utils.py
│   │   ├── jwt_utils.py
│   │   ├── response_utils.py
│   │   ├── file_utils.py
│   │   └── logger.py
│   │
│   └── tests/
│       ├── test_auth.py
│       ├── test_rbac.py
│       ├── test_courses.py
│       ├── test_quizzes.py
│       ├── test_ai_validation.py
│       └── test_functional.py
│
├── sql/
│   ├── 01_create_roles_users.sql
│   ├── 02_create_students_faculty.sql
│   ├── 03_create_courses_enrollments.sql
│   ├── 04_create_quizzes_results.sql
│   ├── 05_create_ai_tables.sql
│   └── seed_data.sql
│
├── docker/
│   └── Dockerfile
│
├── Jenkinsfile
├── docker-compose.yml
├── requirements.txt
├── .env
├── .gitignore
└── README.md

-------------------------------------

CREATE TABLE ROLES (
    ROLE_ID NUMBER PRIMARY KEY,
    ROLE_NAME VARCHAR2(50) UNIQUE NOT NULL,
    DESCRIPTION VARCHAR2(255),
    CREATED_AT DATE DEFAULT SYSDATE
);

CREATE SEQUENCE ROLES_SEQ START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER ROLES_TRG
BEFORE INSERT ON ROLES
FOR EACH ROW
BEGIN
    IF :NEW.ROLE_ID IS NULL THEN
        SELECT ROLES_SEQ.NEXTVAL INTO :NEW.ROLE_ID FROM DUAL;
    END IF;
END;
/

CREATE TABLE USERS (
    USER_ID NUMBER PRIMARY KEY,
    FULL_NAME VARCHAR2(100) NOT NULL,
    EMAIL VARCHAR2(150) UNIQUE NOT NULL,
    PASSWORD_HASH VARCHAR2(255) NOT NULL,
    PHONE VARCHAR2(20),
    IS_ACTIVE NUMBER(1) DEFAULT 1,
    CREATED_AT DATE DEFAULT SYSDATE,
    UPDATED_AT DATE
);

CREATE SEQUENCE USERS_SEQ START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER USERS_TRG
BEFORE INSERT ON USERS
FOR EACH ROW
BEGIN
    IF :NEW.USER_ID IS NULL THEN
        SELECT USERS_SEQ.NEXTVAL INTO :NEW.USER_ID FROM DUAL;
    END IF;
END;
/

CREATE TABLE USER_ROLES (
    USER_ROLE_ID NUMBER PRIMARY KEY,
    USER_ID NUMBER NOT NULL,
    ROLE_ID NUMBER NOT NULL,
    CREATED_AT DATE DEFAULT SYSDATE,

    CONSTRAINT FK_USER_ROLES_USER 
        FOREIGN KEY (USER_ID) REFERENCES USERS(USER_ID),

    CONSTRAINT FK_USER_ROLES_ROLE 
        FOREIGN KEY (ROLE_ID) REFERENCES ROLES(ROLE_ID),

    CONSTRAINT UK_USER_ROLE UNIQUE (USER_ID, ROLE_ID)
);

CREATE SEQUENCE USER_ROLES_SEQ START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER USER_ROLES_TRG
BEFORE INSERT ON USER_ROLES
FOR EACH ROW
BEGIN
    IF :NEW.USER_ROLE_ID IS NULL THEN
        SELECT USER_ROLES_SEQ.NEXTVAL INTO :NEW.USER_ROLE_ID FROM DUAL;
    END IF;
END;
/
-------------------------------
CREATE TABLE STUDENTS (
    STUDENT_ID NUMBER PRIMARY KEY,
    USER_ID NUMBER UNIQUE NOT NULL,
    ROLL_NUMBER VARCHAR2(50) UNIQUE NOT NULL,
    DEPARTMENT VARCHAR2(100),
    SEMESTER NUMBER,
    ADMISSION_YEAR NUMBER,
    CREATED_AT DATE DEFAULT SYSDATE,

    CONSTRAINT FK_STUDENT_USER 
        FOREIGN KEY (USER_ID) REFERENCES USERS(USER_ID)
);

CREATE SEQUENCE STUDENTS_SEQ START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER STUDENTS_TRG
BEFORE INSERT ON STUDENTS
FOR EACH ROW
BEGIN
    IF :NEW.STUDENT_ID IS NULL THEN
        SELECT STUDENTS_SEQ.NEXTVAL INTO :NEW.STUDENT_ID FROM DUAL;
    END IF;
END;
/

CREATE TABLE FACULTY (
    FACULTY_ID NUMBER PRIMARY KEY,
    USER_ID NUMBER UNIQUE NOT NULL,
    EMPLOYEE_CODE VARCHAR2(50) UNIQUE NOT NULL,
    DEPARTMENT VARCHAR2(100),
    DESIGNATION VARCHAR2(100),
    CREATED_AT DATE DEFAULT SYSDATE,

    CONSTRAINT FK_FACULTY_USER 
        FOREIGN KEY (USER_ID) REFERENCES USERS(USER_ID)
);

CREATE SEQUENCE FACULTY_SEQ START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER FACULTY_TRG
BEFORE INSERT ON FACULTY
FOR EACH ROW
BEGIN
    IF :NEW.FACULTY_ID IS NULL THEN
        SELECT FACULTY_SEQ.NEXTVAL INTO :NEW.FACULTY_ID FROM DUAL;
    END IF;
END;
/

-------------------------------------

CREATE TABLE COURSES (
    COURSE_ID NUMBER PRIMARY KEY,
    COURSE_CODE VARCHAR2(50) UNIQUE NOT NULL,
    COURSE_TITLE VARCHAR2(150) NOT NULL,
    DESCRIPTION CLOB,
    FACULTY_ID NUMBER NOT NULL,
    CATEGORY VARCHAR2(100),
    CREDITS NUMBER DEFAULT 0,
    IS_ACTIVE NUMBER(1) DEFAULT 1,
    CREATED_AT DATE DEFAULT SYSDATE,
    UPDATED_AT DATE,

    CONSTRAINT FK_COURSE_FACULTY 
        FOREIGN KEY (FACULTY_ID) REFERENCES FACULTY(FACULTY_ID)
);

CREATE SEQUENCE COURSES_SEQ START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER COURSES_TRG
BEFORE INSERT ON COURSES
FOR EACH ROW
BEGIN
    IF :NEW.COURSE_ID IS NULL THEN
        SELECT COURSES_SEQ.NEXTVAL INTO :NEW.COURSE_ID FROM DUAL;
    END IF;
END;
/

CREATE TABLE ENROLLMENTS (
    ENROLLMENT_ID NUMBER PRIMARY KEY,
    STUDENT_ID NUMBER NOT NULL,
    COURSE_ID NUMBER NOT NULL,
    ENROLLMENT_DATE DATE DEFAULT SYSDATE,
    STATUS VARCHAR2(30) DEFAULT 'ACTIVE',

    CONSTRAINT FK_ENROLL_STUDENT 
        FOREIGN KEY (STUDENT_ID) REFERENCES STUDENTS(STUDENT_ID),

    CONSTRAINT FK_ENROLL_COURSE 
        FOREIGN KEY (COURSE_ID) REFERENCES COURSES(COURSE_ID),

    CONSTRAINT UK_STUDENT_COURSE UNIQUE (STUDENT_ID, COURSE_ID)
);

CREATE SEQUENCE ENROLLMENTS_SEQ START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER ENROLLMENTS_TRG
BEFORE INSERT ON ENROLLMENTS
FOR EACH ROW
BEGIN
    IF :NEW.ENROLLMENT_ID IS NULL THEN
        SELECT ENROLLMENTS_SEQ.NEXTVAL INTO :NEW.ENROLLMENT_ID FROM DUAL;
    END IF;
END;
/

---------------------------------------

CREATE TABLE QUIZZES (
    QUIZ_ID NUMBER PRIMARY KEY,
    COURSE_ID NUMBER NOT NULL,
    TITLE VARCHAR2(150) NOT NULL,
    DESCRIPTION CLOB,
    TOTAL_MARKS NUMBER DEFAULT 0,
    DURATION_MINUTES NUMBER,
    START_TIME DATE,
    END_TIME DATE,
    CREATED_BY NUMBER NOT NULL,
    CREATED_AT DATE DEFAULT SYSDATE,

    CONSTRAINT FK_QUIZ_COURSE 
        FOREIGN KEY (COURSE_ID) REFERENCES COURSES(COURSE_ID),

    CONSTRAINT FK_QUIZ_FACULTY 
        FOREIGN KEY (CREATED_BY) REFERENCES FACULTY(FACULTY_ID)
);

CREATE SEQUENCE QUIZZES_SEQ START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER QUIZZES_TRG
BEFORE INSERT ON QUIZZES
FOR EACH ROW
BEGIN
    IF :NEW.QUIZ_ID IS NULL THEN
        SELECT QUIZZES_SEQ.NEXTVAL INTO :NEW.QUIZ_ID FROM DUAL;
    END IF;
END;
/

CREATE TABLE QUESTIONS (
    QUESTION_ID NUMBER PRIMARY KEY,
    QUIZ_ID NUMBER NOT NULL,
    QUESTION_TEXT CLOB NOT NULL,
    QUESTION_TYPE VARCHAR2(30) DEFAULT 'MCQ',
    OPTION_A VARCHAR2(500),
    OPTION_B VARCHAR2(500),
    OPTION_C VARCHAR2(500),
    OPTION_D VARCHAR2(500),
    CORRECT_OPTION VARCHAR2(10),
    MARKS NUMBER DEFAULT 1,

    CONSTRAINT FK_QUESTION_QUIZ 
        FOREIGN KEY (QUIZ_ID) REFERENCES QUIZZES(QUIZ_ID)
);

CREATE SEQUENCE QUESTIONS_SEQ START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER QUESTIONS_TRG
BEFORE INSERT ON QUESTIONS
FOR EACH ROW
BEGIN
    IF :NEW.QUESTION_ID IS NULL THEN
        SELECT QUESTIONS_SEQ.NEXTVAL INTO :NEW.QUESTION_ID FROM DUAL;
    END IF;
END;
/

CREATE TABLE QUIZ_ATTEMPTS (
    ATTEMPT_ID NUMBER PRIMARY KEY,
    QUIZ_ID NUMBER NOT NULL,
    STUDENT_ID NUMBER NOT NULL,
    STARTED_AT DATE DEFAULT SYSDATE,
    SUBMITTED_AT DATE,
    SCORE NUMBER DEFAULT 0,
    STATUS VARCHAR2(30) DEFAULT 'IN_PROGRESS',

    CONSTRAINT FK_ATTEMPT_QUIZ 
        FOREIGN KEY (QUIZ_ID) REFERENCES QUIZZES(QUIZ_ID),

    CONSTRAINT FK_ATTEMPT_STUDENT 
        FOREIGN KEY (STUDENT_ID) REFERENCES STUDENTS(STUDENT_ID)
);

CREATE SEQUENCE QUIZ_ATTEMPTS_SEQ START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER QUIZ_ATTEMPTS_TRG
BEFORE INSERT ON QUIZ_ATTEMPTS
FOR EACH ROW
BEGIN
    IF :NEW.ATTEMPT_ID IS NULL THEN
        SELECT QUIZ_ATTEMPTS_SEQ.NEXTVAL INTO :NEW.ATTEMPT_ID FROM DUAL;
    END IF;
END;
/

CREATE TABLE RESULTS (
    RESULT_ID NUMBER PRIMARY KEY,
    STUDENT_ID NUMBER NOT NULL,
    COURSE_ID NUMBER NOT NULL,
    QUIZ_ID NUMBER,
    MARKS_OBTAINED NUMBER DEFAULT 0,
    TOTAL_MARKS NUMBER DEFAULT 0,
    GRADE VARCHAR2(10),
    RESULT_DATE DATE DEFAULT SYSDATE,

    CONSTRAINT FK_RESULT_STUDENT 
        FOREIGN KEY (STUDENT_ID) REFERENCES STUDENTS(STUDENT_ID),

    CONSTRAINT FK_RESULT_COURSE 
        FOREIGN KEY (COURSE_ID) REFERENCES COURSES(COURSE_ID),

    CONSTRAINT FK_RESULT_QUIZ 
        FOREIGN KEY (QUIZ_ID) REFERENCES QUIZZES(QUIZ_ID)
);

CREATE SEQUENCE RESULTS_SEQ START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER RESULTS_TRG
BEFORE INSERT ON RESULTS
FOR EACH ROW
BEGIN
    IF :NEW.RESULT_ID IS NULL THEN
        SELECT RESULTS_SEQ.NEXTVAL INTO :NEW.RESULT_ID FROM DUAL;
    END IF;
END;
/

--------------------------

CREATE TABLE AI_INTERACTIONS (
    AI_INTERACTION_ID NUMBER PRIMARY KEY,
    USER_ID NUMBER NOT NULL,
    COURSE_ID NUMBER,
    INTERACTION_TYPE VARCHAR2(50),
    USER_QUERY CLOB,
    AI_RESPONSE CLOB,
    CREATED_AT DATE DEFAULT SYSDATE,

    CONSTRAINT FK_AI_USER 
        FOREIGN KEY (USER_ID) REFERENCES USERS(USER_ID),

    CONSTRAINT FK_AI_COURSE 
        FOREIGN KEY (COURSE_ID) REFERENCES COURSES(COURSE_ID)
);

CREATE SEQUENCE AI_INTERACTIONS_SEQ START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER AI_INTERACTIONS_TRG
BEFORE INSERT ON AI_INTERACTIONS
FOR EACH ROW
BEGIN
    IF :NEW.AI_INTERACTION_ID IS NULL THEN
        SELECT AI_INTERACTIONS_SEQ.NEXTVAL INTO :NEW.AI_INTERACTION_ID FROM DUAL;
    END IF;
END;
/

CREATE TABLE COURSE_MATERIALS (
    MATERIAL_ID NUMBER PRIMARY KEY,
    COURSE_ID NUMBER NOT NULL,
    TITLE VARCHAR2(150),
    FILE_PATH VARCHAR2(500),
    CONTENT_TEXT CLOB,
    UPLOADED_BY NUMBER NOT NULL,
    CREATED_AT DATE DEFAULT SYSDATE,

    CONSTRAINT FK_MATERIAL_COURSE 
        FOREIGN KEY (COURSE_ID) REFERENCES COURSES(COURSE_ID),

    CONSTRAINT FK_MATERIAL_FACULTY 
        FOREIGN KEY (UPLOADED_BY) REFERENCES FACULTY(FACULTY_ID)
);

CREATE SEQUENCE COURSE_MATERIALS_SEQ START WITH 1 INCREMENT BY 1;

CREATE OR REPLACE TRIGGER COURSE_MATERIALS_TRG
BEFORE INSERT ON COURSE_MATERIALS
FOR EACH ROW
BEGIN
    IF :NEW.MATERIAL_ID IS NULL THEN
        SELECT COURSE_MATERIALS_SEQ.NEXTVAL INTO :NEW.MATERIAL_ID FROM DUAL;
    END IF;
END;
/

----------------------------
INSERT INTO ROLES (ROLE_NAME, DESCRIPTION)
VALUES ('ADMIN', 'System administrator');

INSERT INTO ROLES (ROLE_NAME, DESCRIPTION)
VALUES ('FACULTY', 'Faculty member');

INSERT INTO ROLES (ROLE_NAME, DESCRIPTION)
VALUES ('STUDENT', 'Student user');

COMMIT;

-----------------------------

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str
    APP_ENV: str
    APP_DEBUG: bool

    ORACLE_USER: str
    ORACLE_PASSWORD: str
    ORACLE_HOST: str
    ORACLE_PORT: int
    ORACLE_SERVICE_NAME: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    AI_PROVIDER: str | None = None
    AI_API_KEY: str | None = None

    class Config:
        env_file = ".env"


settings = Settings()

--------------------------------

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings


DATABASE_URL = (
    f"oracle+cx_oracle://{settings.ORACLE_USER}:"
    f"{settings.ORACLE_PASSWORD}@"
    f"{settings.ORACLE_HOST}:{settings.ORACLE_PORT}/"
    f"?service_name={settings.ORACLE_SERVICE_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

---------------------------------

from app.database.connection import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
--------------------------------

