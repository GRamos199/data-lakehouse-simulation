# Architecture Decision Records (ADR)

This directory documents major architectural decisions made in the Data Lakehouse Simulation project.

## ADR-001: Three-Layer Lakehouse Architecture

### Status
ACCEPTED

### Context
We need to organize data in a way that separates raw data from processed data, enabling both data lineage and multiple processing approaches.

### Decision
Implement a three-layer architecture:
1. **RAW Layer**: Stores unprocessed data from source systems
2. **CLEAN Layer**: Stores validated and normalized data
3. **ANALYTICS Layer**: Stores aggregated and analysis-ready data

### Consequences
- **Positive**: Clear separation of concerns, easy data lineage tracking, supports multiple downstream use cases
- **Negative**: Requires more storage space, data duplication

## ADR-002: DuckDB for Analytics Layer

### Status
ACCEPTED

### Context
We need a lightweight analytical database that works well with local development and can handle SQL queries.

### Decision
Use DuckDB for the analytics layer instead of traditional data warehouses.

### Consequences
- **Positive**: No external dependencies, excellent SQL support, fast OLAP queries, ACID transactions
- **Negative**: Limited to single-machine deployment, not designed for petabyte-scale data

## ADR-003: Apache Airflow for Orchestration

### Status
ACCEPTED (for local development)

### Context
We need reliable task orchestration with scheduling, retries, and monitoring capabilities.

### Decision
Use Apache Airflow for local development and orchestration, with migration path to AWS Step Functions.

### Consequences
- **Positive**: Mature tool, excellent DAG visualization, rich monitoring, large community
- **Negative**: Requires separate metadata database, higher resource consumption

## ADR-004: LocalStack for Local AWS Simulation

### Status
ACCEPTED

### Context
We want to develop cloud-native features locally without creating real AWS resources.

### Decision
Use LocalStack to emulate AWS services locally during development and testing.

### Consequences
- **Positive**: No AWS costs, fast development cycles, reproducible environments
- **Negative**: Not 100% AWS API parity, some advanced features may not be supported

## ADR-005: GitHub Actions for CI/CD

### Status
ACCEPTED

### Context
We need automated testing, code quality checks, and deployment pipelines.

### Decision
Use GitHub Actions for CI/CD workflows, as it's built into GitHub and free for public repositories.

### Consequences
- **Positive**: No additional infrastructure, good GitHub integration, generous free tier
- **Negative**: Limited to GitHub, execution logs need GitHub access, no self-hosted runner by default

## ADR-006: Terraform for Infrastructure

### Status
ACCEPTED

### Context
We need to define and manage cloud infrastructure as code for reproducibility and version control.

### Decision
Use Terraform to define all AWS infrastructure with support for both LocalStack and real AWS.

### Consequences
- **Positive**: Infrastructure versioning, consistent deployments, easy to modify and extend
- **Negative**: Additional learning curve, state file management needed

## Implementation Timeline

1. **Phase 1** (Completed): Local development with Airflow and DuckDB
2. **Phase 2** (In Progress): Add testing and CI/CD with GitHub Actions
3. **Phase 3** (Planned): Infrastructure as Code with Terraform/LocalStack
4. **Phase 4** (Planned): Migration to serverless (Lambda, Step Functions)
5. **Phase 5** (Planned): Real-time streaming capabilities

## See Also

- [IMPROVEMENTS.md](IMPROVEMENTS.md) - Implementation details of improvements
- [terraform/README.md](terraform/README.md) - Infrastructure deployment guide
- [CONTRIBUTING.md](CONTRIBUTING.md) - Development guidelines
