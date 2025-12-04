# Data Generators Lab

Data Generators Lab is a modular synthetic data generation framework designed for data engineering, analytics, data science, and machine learning workflows.  
It enables creation of high-quality, realistic, constraint-aware datasets that simulate production environments for experimentation, prototyping, development, benchmarking, and training.

The framework is designed for extensibility, reproducibility, code clarity, and practical use in real-world engineering environments.

---

## 1. Introduction

Modern data-driven projects require access to representative datasets for:

- Pipeline development and testing  
- Experimentation in notebooks  
- Prototyping ML models  
- Simulating ETL workloads  
- Teaching and demonstrations  
- Building professional portfolio projects  

However, real datasets are often unavailable due to privacy, compliance, or access restrictions.  
Data Generators Lab solves this problem by providing:

- Scenario-based generators that model realistic business processes  
- Domain-specific generators for scientific, engineering, and analytics-driven data  
- Configurable generation through Python classes and YAML schemas  
- A unified CLI entry point  
- A highly structured codebase designed for maintainability and extension  

The framework supports arbitrary scaling of dataset size, injection of noise and missingness, timestamps, categorical distributions, and rule-based constraints.

---

## 2. Key Features

### 2.1 Scenario-Based Architecture
Each scenario represents a well-defined real-world context such as attendance logs, Spark job execution logs, or loan applications.  
Scenarios include:

- Data schema definition  
- Configurable parameters  
- Rule-based data generation logic  
- Optional missingness and noise patterns  

### 2.2 Modular Domain Generators
Reusable generators for specific domains such as:

- Engineering (sensor readings)  
- Science (experimental measurements)  
- Analytics (sales, user events)  

These modules can be combined or extended to create new datasets.

### 2.3 CLI Integration
A unified command-line interface allows quick dataset generation without writing code.  
This supports automated workflows, pipeline demonstrations, and ETL testing.

### 2.4 Extensible Template System
Developers can add new datasets rapidly using the provided template structure.

### 2.5 Reproducibility
Every generator supports deterministic configuration through parameterized seeds.

### 2.6 Production-Style Project Layout
The repository is structured following modern Python packaging standards, enabling:

- Editable installs  
- Unit testing with pytest  
- Static analysis tools  
- Clear separation of source, tests, documentation, and examples  

---

## 3. Repository Structure

```
data-generators-lab/
├─ src/data_generators/
│  ├─ cli.py                      # Main CLI entry point
│  ├─ __main__.py                 # Enables "python -m data_generators"
│  ├─ core/                       # Base classes and utilities
│  │  ├─ base_generator.py
│  │  ├─ utils.py
│  │  └─ faker_utils.py
│  ├─ domains/                    # Domain-level generators
│  │  ├─ engineering/
│  │  ├─ science/
│  │  └─ analytics/
│  ├─ scenarios/                  # Scenario-specific datasets
│  │  ├─ attendance/
│  │  ├─ spark_logs/
│  │  └─ loan_applications/
│  └─ __init__.py
│
├─ projects/                      # End-to-end workflow notebooks and examples
├─ templates/                     # Templates for new scenarios
├─ configs/                       # Global configuration files
├─ data/                          # Generated and sample datasets
├─ tests/                         # Pytest-based unit test suite
├─ docs/                          # Design documentation
├─ pyproject.toml                 # Build configuration
├─ .gitignore
└─ README.md
```

---

## 4. Installation

### 4.1. Create a Virtual Environment

```
python -m venv .venv
```

### 4.2. Activate the Environment

**Windows (PowerShell):**
```
.\.venv\Scripts\Activate.ps1
```

### 4.3. Install the Package in Editable Mode

```
pip install -e .
```

This allows modifying the codebase without reinstalling.

---

## 5. Command-Line Interface Usage

Dataset generation is performed using:

```
python -m data_generators generate <scenario> --rows <n> --out <file>
```

Supported scenarios:

### 5.1 Attendance Data

Simulates employee attendance events with realistic patterns.

```
python -m data_generators generate attendance --rows 10000 --out data/raw/attendance.csv
```

### 5.2 Spark Logs

Generates synthetic Spark job → stage → task execution logs.

```
python -m data_generators generate spark_logs --rows 5000 --out data/raw/spark_logs.csv
```

### 5.3 Loan Applications (Financial Dataset)

Produces synthetic loan application records with controlled missingness and categorical distributions.

```
python -m data_generators generate loans --rows 1000 --out data/raw/loans.csv
```

Output format:

- `.csv` produces comma-separated files  
- `.parquet` produces columnar storage files for analytics tools  

---

## 6. Scenario Details

### 6.1 Attendance

Includes:

- Employee identifiers  
- Departments  
- Date boundaries  
- Status categories (Present, Late, Absent, WFH)  
- Realistic time-of-day variation  
- Weekend constraints  
- Configurable seasonality and noise  

Useful for:

- Productivity analysis  
- Time-series transformations  
- Feature engineering practice  
- Spark aggregation tests  

---

### 6.2 Spark Logs

Simulates logs typically produced by Apache Spark applications.

Fields include:

- Job ID  
- Stage ID  
- Task ID  
- Timestamp sequences  
- Log severity  
- Programmatically generated messages  

Useful for:

- Observability tool demonstrations  
- Log parsing exercises  
- Data engineering interview prep  
- ETL pipeline prototyping  

---

### 6.3 Loan Applications

Matches a realistic financial loan application schema.

Includes:

- Loan identifiers  
- Customer identifiers  
- Timestamps  
- Loan amounts and interest rate ranges  
- Tenure in months  
- Loan status categories  
- Product type, branch, and credit score band  
- Configurable missing-value injection  
- Deterministic generation with seeds  

Useful for:

- Financial modeling  
- Risk analysis  
- Feature engineering  
- Classification or segmentation tasks  

---

## 7. Extending the Framework

### 7.1 Creating a New Scenario

A new scenario requires:

1. A directory:
   ```
   src/data_generators/scenarios/<scenario_name>/
   ```

2. A `schema.yml` describing fields and constraints  
3. A `generator.py` implementing a generator class  
4. A configuration dataclass  
5. Registration inside `cli.py`

### 7.2 Recommended Development Workflow

- Define schema and metadata  
- Implement configuration dataclass  
- Write generator logic (with optional noise or missingness)  
- Validate using a notebook in `projects/`  
- Register with CLI for repeatability  

The modular design allows you to build dozens of real-world datasets rapidly.

---

## 8. Using Generators Programmatically

Generators may be invoked directly from Python scripts or notebooks:

```python
from data_generators.scenarios.loan_applications.generator import (
    LoanApplicationsGenerator,
    LoanApplicationsConfig
)

config = LoanApplicationsConfig(num_rows=2000)
df = LoanApplicationsGenerator(config).generate()

print(df.head())
```

---

## 9. Testing

The repository includes a pytest-based testing framework.

Run tests with:

```
pytest
```

Tests verify:

- Schema consistency  
- Generator behavior  
- Deterministic outputs with seeds  
- CLI execution  

---

## 10. Documentation

Documentation is stored in the `docs/` directory and includes:

- System architecture  
- Scenario guides  
- Development workflow  
- Data model descriptions  

---

## 11. License

This project is distributed under the MIT License.  
See the `LICENSE` file for details.

---

## 12. Authors and Acknowledgements

**Aadarsh Shrestha**  
Data Engineer specializing in Python, ETL systems, distributed processing, and applied analytics.

The project structure and engineering approach draw from industry best practices in open-source data engineering tools.

---

## 13. Contribution Guidelines

Contributions are welcome.

Areas suitable for contribution:

- New dataset scenarios  
- Enhancements to existing generators  
- Improvements to the CLI  
- Documentation extensions  
- Test coverage improvements  
- Performance optimizations  

---

