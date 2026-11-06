import sqlite3

def create_warehouse():
    # Connects to the SQLite database file
    conn = sqlite3.connect('manufacturing_warehouse.db')
    cursor = conn.cursor()
    
    print("Initializing Synchronized Star Schema Data Warehouse...")

    # 1. Machine Dimension Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dim_machines (
            machine_id INTEGER PRIMARY KEY,
            operator_count INTEGER,
            maintenance_hours REAL
        )
    ''')

    # 2. Product Dimension Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dim_products (
            product_type TEXT PRIMARY KEY,
            material_cost_per_unit REAL
        )
    ''')

    # 3. Central Production Fact Table (Maps directly to your CSV metrics)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fact_production_events (
            production_id TEXT PRIMARY KEY,
            date TEXT NOT NULL,
            product_type TEXT,
            machine_id INTEGER,
            shift TEXT,
            units_produced INTEGER,
            defects INTEGER,
            production_time_hours REAL,
            labour_cost_per_hour REAL,
            energy_consumption_kwh REAL,
            downtime_hours REAL,
            scrap_rate REAL,
            rework_hours REAL,
            quality_checks_failed INTEGER,
            average_temperature_c REAL,
            average_humidity_percent REAL,
            FOREIGN KEY (machine_id) REFERENCES dim_machines(machine_id),
            FOREIGN KEY (product_type) REFERENCES dim_products(product_type)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database Schema updated and synchronized with factory source data!")

if __name__ == "__main__":
    create_warehouse()
