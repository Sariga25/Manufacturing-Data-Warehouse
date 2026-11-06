import sqlite3
import pandas as pd
import io

def run_etl():
    print("Starting Synchronized ETL Pipeline Execution...")
    
    # 1. EXTRACT: Reading the production records data stream
    # (Using an IO stream to directly parse the data you provided)
    factory_data = """Production ID,Date,Product Type,Machine ID,Shift,Units Produced,Defects,Production Time Hours,Material Cost Per Unit,Labour Cost Per Hour,Energy Consumption kWh,Operator Count,Maintenance Hours,Down time Hours,Production Volume Cubic Meters,Scrap Rate,Rework Hours,Quality Checks Failed,Average Temperature C,Average Humidity Percent
1899-12-31,2020-01-01,Automotive,3,Swing,142,3,23.42,38.68,15.38,413.97,1,4.86,1.57,2.34,0.048,1.65,1,22.8,47.2
1900-01-01,2020-01-02,Textiles,8,Night,170,4,7.51,21.35,25.36,181.16,2,2.51,0.18,1.52,0.03,,1,23.8,37.9
1900-01-02,2020-01-03,Appliances,11,Swing,182,4,20.58,47.54,16.46,452.15,2,0.34,2.88,0.57,0.026,0.26,0,24.5,56.1
1900-03-05,2020-03-05,Textiles,5,Swing,178,,23.25,14.09,27.47,381.39,1,4.17,1.62,1.81,0.031,0.18,0,20.4,46.6
2998,2028-03-16,Appliances,9,Day,141,3,23.61,47.18,25.44,106.32,3,4.15,,1.91,0.029,1.9,2,22.5,52.6
2999,2028-03-17,Furniture,20,Swing,199,3,1.01,24.35,29.73,245.47,3,2.73,0.26,0.93,0.029,1.26,1,24.9,56.3
3000,2028-03-18,Appliances,12,Night,121,2,5.36,12.41,22.96,221.97,3,0.07,,2.18,0.018,1.07,2,19.9,37.8"""

    df = pd.read_csv(io.StringIO(factory_data))
    
    # 2. TRANSFORM: Standardising and scrubbing data anomalies
    print("Transforming and scrubbing factory datasets...")
    
    # Standardise Column Names to match SQL database fields
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    
    # Fill any missing metrics or empty rows cleanly
    df['defects'] = pd.to_numeric(df['defects']).fillna(0).astype(int)
    df['rework_hours'] = pd.to_numeric(df['rework_hours']).fillna(0.0)
    df['down_time_hours'] = pd.to_numeric(df['down_time_hours']).fillna(0.0)
    df['maintenance_hours'] = pd.to_numeric(df['maintenance_hours']).fillna(0.0)
    df['operator_count'] = pd.to_numeric(df['operator_count']).fillna(1).astype(int)

    # Connect to the target SQLite analytical environment
    conn = sqlite3.connect('manufacturing_warehouse.db')
    
    # 3. LOAD: Appending metrics to optimized dimensions and facts
    print("Loading data directly into database structures...")

    # Load Unique Dimensions for Machines
    machines_dim = df[['machine_id', 'operator_count', 'maintenance_hours']].drop_duplicates(subset=['machine_id'])
    machines_dim.to_sql('dim_machines', conn, if_exists='append', index=False)

    # Load Unique Dimensions for Products 
    products_dim = df[['product_type', 'material_cost_per_unit']].drop_duplicates(subset=['product_type'])
    products_dim.to_sql('dim_products', conn, if_exists='append', index=False)

    # Load Structural Operational Facts
    fact_columns = [
        'production_id', 'date', 'product_type', 'machine_id', 'shift', 
        'units_produced', 'defects', 'production_time_hours', 'labour_cost_per_hour', 
        'energy_consumption_kwh', 'down_time_hours', 'scrap_rate', 'rework_hours', 
        'quality_checks_failed', 'average_temperature_c', 'average_humidity_percent'
    ]
    # Filter only columns present in table to avoid errors
    facts_table = df[[col for col in fact_columns if col in df.columns]]
    
    # Rename column internally to map precisely to DB schema if needed
    if 'down_time_hours' in facts_table.columns:
        facts_table = facts_table.rename(columns={'down_time_hours': 'downtime_hours'})

    facts_table.to_sql('fact_production_events', conn, if_exists='append', index=False)

    conn.close()
    print("ETL System run completed! Production data loaded into warehouse maps securely.")

if __name__ == "__main__":
    run_etl()
