-- src/db/sql/create_tables.sql
CREATE TABLE property (
    property_id INT PRIMARY KEY,
    property_title VARCHAR(255),
    address VARCHAR(255),
    reviewed_status VARCHAR(50),
    most_recent_status VARCHAR(50),
    source VARCHAR(100),
    market VARCHAR(100),
    occupancy VARCHAR(50),
    flood VARCHAR(50),
    street_address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    zip VARCHAR(20),
    property_type VARCHAR(100),
    highway VARCHAR(50),
    train VARCHAR(50),
    tax_rate DOUBLE,
    sqft_basement INT,
    htw VARCHAR(100),
    pool VARCHAR(100),
    commercial VARCHAR(100),
    water VARCHAR(100),
    sewage VARCHAR(100),
    year_built INT,
    sqft_mu INT,
    sqft_total VARCHAR(50),
    parking VARCHAR(100),
    bed INT,
    bath INT,
    basementyesno VARCHAR(50),
    layout VARCHAR(100),
    net_yield DOUBLE,
    irr DOUBLE,
    rent_restricted VARCHAR(50),
    neighborhood_rating INT,
    latitude DOUBLE,
    longitude DOUBLE,
    subdivision VARCHAR(255),
    taxes DOUBLE,
    selling_reason VARCHAR(255),
    seller_retained_broker VARCHAR(255),
    final_reviewer VARCHAR(255),
    school_average DOUBLE
);

CREATE TABLE valuation (
    valuation_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    list_price DOUBLE,
    previous_rent DOUBLE,
    arv DOUBLE,
    rent_zestimate DOUBLE,
    expected_rent DOUBLE,
    low_fmr DOUBLE,
    high_fmr DOUBLE,
    zestimate DOUBLE,
    redfin_value DOUBLE,
    FOREIGN KEY (property_id) REFERENCES property(property_id) ON DELETE CASCADE
);

CREATE TABLE hoa (
    hoa_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    hoa DOUBLE,
    hoa_flag VARCHAR(50),
    FOREIGN KEY (property_id) REFERENCES property(property_id) ON DELETE CASCADE
);

CREATE TABLE rehab (
    rehab_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    underwriting_rehab DOUBLE,
    rehab_calculation DOUBLE,
    paint VARCHAR(50),
    flooring_flag VARCHAR(50),
    foundation_flag VARCHAR(50),
    roof_flag VARCHAR(50),
    hvac_flag VARCHAR(50),
    kitchen_flag VARCHAR(50),
    bathroom_flag VARCHAR(50),
    appliances_flag VARCHAR(50),
    windows_flag VARCHAR(50),
    landscaping_flag VARCHAR(50),
    trashout_flag VARCHAR(50),
    FOREIGN KEY (property_id) REFERENCES property(property_id) ON DELETE CASCADE
);

CREATE TABLE leads (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    Reviewed_Status VARCHAR(255),
    Most_Recent_Status VARCHAR(255),
    Source VARCHAR(255),
    Net_Yield DOUBLE,
    IRR DOUBLE,
    Selling_Reason VARCHAR(255),
    Seller_Retained_Broker VARCHAR(255),
    Final_Reviewer VARCHAR(255),
    FOREIGN KEY (property_id) REFERENCES property(property_id) ON DELETE CASCADE
);

CREATE TABLE taxes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    Taxes DOUBLE,
    FOREIGN KEY (property_id) REFERENCES property(property_id) ON DELETE CASCADE
);
