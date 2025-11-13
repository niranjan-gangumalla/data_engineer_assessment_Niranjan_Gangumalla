# Data Engineering Assessment

Welcome!  
This exercise evaluates your core **data-engineering** skills:

| Competency | Focus                                                         |
| ---------- | ------------------------------------------------------------- |
| SQL        | relational modelling, normalisation, DDL/DML scripting        |
| Python ETL | data ingestion, cleaning, transformation, & loading (ELT/ETL) |

---

## 0 Prerequisites & Setup

> **Allowed technologies**

- **Python ≥ 3.8** – all ETL / data-processing code
- **MySQL 8** – the target relational database
- **Pydantic** – For data validation
- List every dependency in **`requirements.txt`** and justify selection of libraries in the submission notes.

---

## 1 Clone the skeleton repo

```
git clone https://github.com/100x-Home-LLC/data_engineer_assessment.git
```

✏️ Note: Rename the repo after cloning and add your full name.

**Start the MySQL database in Docker:**

```
docker-compose -f docker-compose.initial.yml up --build -d
```

- Database is available on `localhost:3306`
- Credentials/configuration are in the Docker Compose file
- **Do not change** database name or credentials

For MySQL Docker image reference:
[MySQL Docker Hub](https://hub.docker.com/_/mysql)

---

### Problem

- You are provided with a raw JSON file containing property records is located in data/
- Each row relates to a property. Each row mixes many unrelated attributes (property details, HOA data, rehab estimates, valuations, etc.).
- There are multiple Columns related to this property.
- The database is not normalized and lacks relational structure.
- Use the supplied Field Config.xlsx (in data/) to understand business semantics.

### Task

- **Normalize the data:**

  - Develop a Python ETL script to read, clean, transform, and load data into your normalized MySQL tables.
  - Refer the field config document for the relation of business logic
  - Use primary keys and foreign keys to properly capture relationships

- **Deliverable:**
  - Write necessary python and sql scripts
  - Place your scripts in `src/`
  - The scripts should take the initial json to your final, normalized schema when executed
  - Clearly document how to run your script, dependencies, and how it integrates with your database.

---

## Submission Guidelines

- Edit the section to the bottom of this README with your solutions and instructions for each section at the bottom.
- Ensure all steps are fully **reproducible** using your documentation
- DO NOT MAKE THE REPOSITORY PUBLIC. ANY CANDIDATE WHO DOES IT WILL BE AUTO REJECTED.
- Create a new private repo and invite the reviewer https://github.com/mantreshjain and https://github.com/siddhuorama

---

**Good luck! We look forward to your submission.**

## Solutions and Instructions (Filed by Candidate)

**Document your solution here:**

# Step 1 — Start MySQL using Docker

- From the project root run:'docker-compose -f docker-compose.initial.yml up --build -d'

# Step 2 — Create the Database Tables inside Docker MySQL
Run the below:
'Get-Content src/sql/create_tables.sql | docker exec -i mysql_ctn mysql -u db_user -p6equj5_db_user home_db'
# Step 3 — Install Python Dependencies
Run : "pip install -r requirements.txt"

# Step 4 — Run the ETL Pipeline

Run : "python src/main.py"

Note run all commands from repo root only.

At the end you may see logs like as below 

"""
2025-11-13 18:10:52,964 [INFO] PropertyETL: ETL Completed Successfully
2025-11-13 18:10:52,964 [INFO] PropertyETL: Total JSON Records Read     : 10088
2025-11-13 18:10:52,964 [INFO] PropertyETL: Successfully Inserted       : 10086
2025-11-13 18:10:52,964 [INFO] PropertyETL: Malformed JSON Records      : 2
2025-11-13 18:10:52,974 [INFO] DBService: Table 'property' contains 10086 rows.
2025-11-13 18:10:52,987 [INFO] DBService: Table 'valuation' contains 24892 rows.
2025-11-13 18:10:52,997 [INFO] DBService: Table 'hoa' contains 10097 rows.
2025-11-13 18:10:53,009 [INFO] DBService: Table 'rehab' contains 20213 rows.
2025-11-13 18:10:53,017 [INFO] DBService: Table 'leads' contains 10086 rows.
2025-11-13 18:10:53,025 [INFO] DBService: Table 'taxes' contains 10086 rows.

"""

malformed records are stored in audit_logs from where we can analysis the malformed records

# stop the docker mysql_ctn

'docker stop mysql_ctn'




