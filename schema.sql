CREATE TABLE user_details (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    mobile_number BIGINT UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    city VARCHAR(100),
    referred_by BIGINT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (referred_by) REFERENCES user_details(user_id) ON DELETE SET NULL
);

CREATE TABLE user_referral_code (
    user_id BIGINT PRIMARY KEY,
    referral_code VARCHAR(50) UNIQUE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user_details(user_id) ON DELETE CASCADE
);
