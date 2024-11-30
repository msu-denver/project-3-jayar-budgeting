CREATE TABLE IF NOT EXISTS users (
    id VARCHAR PRIMARY KEY,
    name VARCHAR,
    passwd BYTEA
);

CREATE TABLE IF NOT EXISTS category_types (
    code INT PRIMARY KEY, 
    description VARCHAR(50) NOT NULL
);

INSERT INTO category_types (code, description) VALUES 
    (1, 'Entertainment'), 
    (2, 'Transportation'), 
    (3, 'Food and Groceries'), 
    (4, 'Housing'), 
    (5, 'Utilities'),
    (6, 'Insurance'),
    (7, 'Health and Medical'),
    (8, 'Debt Payments'),
    (9, 'Savings and Investments'),
    (11, 'Recreation'),
    (12, 'Clothing and Personal Care'),
    (13, 'Education and Learning'),
    (14, 'Childcare and Dependent'),
    (15, 'Pets Gifts and Donations'),
    (16, 'Travel'),
    (17, 'Miscellaneous')
ON CONFLICT (code) DO NOTHING;

CREATE TABLE IF NOT EXISTS payment_types (
    code INT PRIMARY KEY, 
    description VARCHAR(50) NOT NULL
);

INSERT INTO payment_types (code, description) VALUES 
    (1, 'Cash'), 
    (2, 'Credit/Debit Card'), 
    (3, 'Digital Wallet'),  
    (4, 'Mobile App Payment'), 
    (5, 'Gift Card'),
    (6, 'Check')
ON CONFLICT (code) DO NOTHING;

CREATE TABLE IF NOT EXISTS merchants (
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    reoccuring BOOLEAN NOT NULL
);

CREATE TABLE IF NOT EXISTS expenses (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    merchant VARCHAR REFERENCES merchants(id),
    category VARCHAR(50) NOT NULL,
    category_code INTEGER REFERENCES category_types(code),
    amount NUMERIC(10, 2) NOT NULL,
    payment_type VARCHAR(50) NOT NULL,
    payment_type_code INTEGER REFERENCES payment_types(code)
);

CREATE TABLE IF NOT EXISTS receipt_images (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    expense_id INTEGER NOT NULL REFERENCES expenses(id) ON DELETE CASCADE,
    image BYTEA NOT NULL,
    name TEXT NOT NULL,
    mimetype TEXT NOT NULL
);
