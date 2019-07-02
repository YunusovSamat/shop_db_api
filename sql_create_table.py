catalog_create = """\
CREATE TABLE catalog (
    id INTEGER NOT NULL 
        PRIMARY KEY 
        AUTOINCREMENT,
    name TEXT 
)
"""

subcatalog_create = """\
CREATE TABLE subcatalog (
    id INTEGER NOT NULL 
        PRIMARY KEY 
        AUTOINCREMENT,
    id_catalog INTEGER NOT NULL,
    name TEXT,
    FOREIGN KEY(id_catalog) REFERENCES catalog(id)
)
"""

product_create = """\
CREATE TABLE product (
    id INTEGER NOT NULL 
        PRIMARY KEY 
        AUTOINCREMENT,
    id_subcatalog INTEGER NOT NULL
        REFERENCES subcatalog,
    name TEXT,
    description TEXT,
    price INTEGER UNIQUE NOT NULL,
    old_price INTEGER UNIQUE DEFAULT 0,
    new INTEGER DEFAULT 0
)
"""

image_create = """\
CREATE TABLE image (
    id INTEGER NOT NULL 
        PRIMARY KEY 
        AUTOINCREMENT,
    id_product INTEGER NOT NULL 
        REFERENCES product,
    image TEXT
)
"""

size_create = """\
CREATE TABLE size (
    id INTEGER NOT NULL 
        PRIMARY KEY 
        AUTOINCREMENT,
    size INTEGER UNIQUE
)
"""

count_create = """\
CREATE TABLE count (
    id INTEGER NOT NULL 
        PRIMARY KEY 
        AUTOINCREMENT,
    id_product INTEGER NOT NULL 
        REFERENCES product,
    id_size INTEGER NOT NULL 
        REFERENCES size,
    count INTEGER UNIQUE DEFAULT 100
)
"""

user_create = """\
CREATE TABLE user (
    id INTEGER NOT NULL 
        PRIMARY KEY 
        AUTOINCREMENT,
    username TEXT NOT NULL,
    name TEXT,
    surname TEXT,
    email TEXT,
    password TEXT NOT NULL,
    address TEXT,
    phone INTEGER
)
"""

order_shop_create = """\
CREATE TABLE order_shop (
    id INTEGER NOT NULL 
        PRIMARY KEY 
        AUTOINCREMENT,
    id_user INTEGER
        REFERENCES user,
    name TEXT,
    surname TEXT,
    email TEXT,
    address TEXT,
    date TEXT DEFAULT CURRENT_TIMESTAMP,
    comment TEXT,
    delivery_price INTEGER UNIQUE,
    total INTEGER UNIQUE
)
"""

product_order_create = """\
CREATE TABLE product_order (
    id INTEGER NOT NULL 
        PRIMARY KEY 
        AUTOINCREMENT,
    id_product INTEGER NOT NULL 
        REFERENCES product,
    id_order_shop INTEGER NOT NULL 
        REFERENCES order_shop,
    size INTEGER UNIQUE,
    count INTEGER UNIQUE DEFAULT 1
)
"""