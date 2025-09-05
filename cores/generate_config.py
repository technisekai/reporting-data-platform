import json
import os
from dotenv import load_dotenv

def insert_config_to_file(job_name: str, team_name: str, own_name: str, cron_time: str, query: str, destination_config: dict):
    load_dotenv()

    queries_dir = os.getenv('queries_dir')
    os.makedirs(queries_dir, exist_ok=True)

    with open(f"{queries_dir}/{job_name}.sql", "w") as query_file:
        query_file.write(query)

    with open(f"config.json", "w") as query_file:
        query_file.write(
            json.dumps({"jobs": [{
                "job_name": job_name,
                "team_name": team_name,
                "own_name": own_name,
                "cron_time": cron_time,
                "query_path": f"{queries_dir}/{job_name}.sql",
                "destination_config": destination_config
            }]})
        )

def insert_config_to_database(
    connection, 
    job_name: str, 
    team_name: str, 
    own_name: str, 
    cron_time: str, 
    query: str, 
    destination_config: dict
):
    load_dotenv()

    queries_dir = os.getenv('queries_dir')
    os.makedirs(queries_dir, exist_ok=True)

    with open(f"{queries_dir}/{job_name}.sql", "w") as query_file:
        query_file.write(query)

    destination_config_table_name = os.getenv('destination_config_table_name')
    cursor = connection.cursor()
    create_table_query = f"""
        create table if not exists {os.getenv('destination_config_table_name')} (
            id serial primary key,
            job_name varchar(255),
            team_name varchar(50),
            own_name varchar(20),
            cron_time varchar(50),
            query_path varchar(255),
            destination_config json,
            created_at timestamp default current_timestamp,
            updated_at timestamp default current_timestamp,
        );
    """
    cursor.execute(create_table_query)
    insert_config_query = f"""
        insert into {destination_config_table_name} (job_name, team_name, own_name, cron_time, query_path, destination_config)
        values ('{job_name}', '{team_name}', '{own_name}', '{cron_time}', '{queries_dir}/{job_name}.sql', '{json.dumps(destination_config)}')
    """
    cursor.execute(insert_config_query) 