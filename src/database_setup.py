import sqlite3

def create_warehouse():
    conn = sqlite3.connect('manufacturing_warehouse.db')
    cursor = conn.cursor()
    print("Initializing Star Schema Data Warehouse...")
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dim_machines (
            machine_id TEXT PRIMARY KEY,
            machine_model TEXT NOT NULL,
            factory_floor TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dim_products (
            product_id TEXT PRIMARY KEY,
            product_name TEXT NOT NULL,
            target_cycle_time_secs REAL NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fact_production_events (
            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            machine_id TEXT,
            product_id TEXT,
            units_produced INTEGER NOT NULL,
            units_defective INTEGER NOT NULL,
            actual_cycle_time_secs REAL NOT NULL,
            FOREIGN KEY (machine_id) REFERENCES dim_machines(machine_id),
            FOREIGN KEY (product_id) REFERENCES dim_products(product_id)
        )
    ''')
    conn.commit()
    conn.close()
    print("Warehouse Schema created successfully!")

if __name__ == "__main__":
    create_warehouse()
