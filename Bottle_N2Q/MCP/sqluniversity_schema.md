# Database Semantic Schema (LLM Optimized)

## Table: `claim`

**Row Count:** 294

| Column | Declared Type | SQLite Affinity | PK | Nullable |
|--------|---------------|-----------------|----|----------|
| claim_id | INTEGER | INTEGER | True | False |
| coverage_id | INTEGER | INTEGER | False | False |
| claim_number | TEXT | TEXT | False | False |
| reported_loss | DECIMAL(14, 2) | NUMERIC | False | False |
| loss_date | DATE | NUMERIC | False | False |

**Relationships:**
- `claim.coverage_id` → `coverage.coverage_id`

**Indexes:**
- `sqlite_autoindex_claim_1` (claim_id) UNIQUE

**Column Intelligence:**
- `claim_id` → HIGH cardinality (294). Values not enumerated.
- `coverage_id` → HIGH cardinality (140). Values not enumerated.
- `claim_number` → HIGH cardinality (294). Values not enumerated.
- `reported_loss` → HIGH cardinality (294). Values not enumerated.
- `loss_date` → HIGH cardinality (271). Values not enumerated.

---

## Table: `coverage`

**Row Count:** 222

| Column | Declared Type | SQLite Affinity | PK | Nullable |
|--------|---------------|-----------------|----|----------|
| coverage_id | INTEGER | INTEGER | True | False |
| vehicle_id | INTEGER | INTEGER | False | False |
| coverage_description_id | INT UNSIGNED | INTEGER | False | False |
| premium | DECIMAL(14, 2) | NUMERIC | False | False |

**Relationships:**
- `coverage.coverage_description_id` → `coverage_description.coverage_description_id`
- `coverage.vehicle_id` → `vehicle.vehicle_id`

**Indexes:**
- `sqlite_autoindex_coverage_1` (coverage_id) UNIQUE

**Column Intelligence:**
- `coverage_id` → HIGH cardinality (222). Values not enumerated.
- `vehicle_id` → HIGH cardinality (51). Values not enumerated.
- `coverage_description_id` → LOW cardinality (5). Example values: ['1', '2', '3', '4', '5']
- `premium` → HIGH cardinality (222). Values not enumerated.

---

## Table: `coverage_description`

**Row Count:** 5

| Column | Declared Type | SQLite Affinity | PK | Nullable |
|--------|---------------|-----------------|----|----------|
| coverage_description_id | INTEGER | INTEGER | True | False |
| coverage_group_id | INTEGER | INTEGER | False | False |
| code | TEXT | TEXT | False | False |
| description_en | TEXT | TEXT | False | True |
| description_fr | TEXT | TEXT | False | True |

**Relationships:**
- `coverage_description.coverage_group_id` → `coverage_group.coverage_group_id`

**Indexes:**
- `sqlite_autoindex_coverage_description_1` (coverage_description_id) UNIQUE

**Column Intelligence:**
- `coverage_description_id` → LOW cardinality (5). Example values: ['1', '2', '3', '4', '5']
- `coverage_group_id` → LOW cardinality (2). Example values: ['1', '2']
- `code` → LOW cardinality (4). Example values: ['ACCG', 'ACCL', 'LIABC', 'LIABG']
- `description_en` → LOW cardinality (5). Example values: ['Civil', 'Criminal', 'General', 'Goods', 'Life']
- `description_fr` → LOW cardinality (5). Example values: ['Biens', 'Civile', 'Criminelle', 'Générale', 'Vie']

---

## Table: `coverage_group`

**Row Count:** 2

| Column | Declared Type | SQLite Affinity | PK | Nullable |
|--------|---------------|-----------------|----|----------|
| coverage_group_id | INTEGER | INTEGER | True | False |
| code | TEXT | TEXT | False | False |
| description_en | TEXT | TEXT | False | True |
| description_fr | TEXT | TEXT | False | True |

**Indexes:**
- `sqlite_autoindex_coverage_group_1` (coverage_group_id) UNIQUE

**Column Intelligence:**
- `coverage_group_id` → LOW cardinality (2). Example values: ['1', '2']
- `code` → LOW cardinality (2). Example values: ['ACC', 'LIA']
- `description_en` → LOW cardinality (2). Example values: ['Accidents', 'Liability']
- `description_fr` → LOW cardinality (2). Example values: ['Accidents', 'Responsabilité']

---

## Table: `policy`

**Row Count:** 16

| Column | Declared Type | SQLite Affinity | PK | Nullable |
|--------|---------------|-----------------|----|----------|
| policy_id | INTEGER | INTEGER | True | False |
| policy_number | TEXT | TEXT | False | False |
| effective_date | DATE | NUMERIC | False | False |
| expiry_date | DATE | NUMERIC | False | False |

**Indexes:**
- `sqlite_autoindex_policy_1` (policy_id) UNIQUE

**Column Intelligence:**
- `policy_id` → LOW cardinality (16). Example values: ['1', '2', '3', '4', '5']
- `policy_number` → LOW cardinality (16). Example values: ['2E2C545I0', '2U9V546I6', '2Z9M007T7', '3J3F799G8', '3O3D181E1']
- `effective_date` → LOW cardinality (15). Example values: ['2015-01-01', '2015-09-01', '2016-07-01', '2017-07-01', '2017-08-01']
- `expiry_date` → LOW cardinality (15). Example values: ['2016-01-01', '2016-09-01', '2017-07-01', '2018-07-01', '2018-08-01']

---

## Table: `province`

**Row Count:** 3

| Column | Declared Type | SQLite Affinity | PK | Nullable |
|--------|---------------|-----------------|----|----------|
| province_id | INTEGER | INTEGER | True | False |
| code | TEXT | TEXT | False | False |
| description_en | TEXT | TEXT | False | True |
| description_fr | TEXT | TEXT | False | True |

**Indexes:**
- `sqlite_autoindex_province_1` (province_id) UNIQUE

**Column Intelligence:**
- `province_id` → LOW cardinality (3). Example values: ['1', '2', '3']
- `code` → LOW cardinality (3). Example values: ['BC', 'ON', 'QC']
- `description_en` → LOW cardinality (3). Example values: ['British Columbia', 'Ontario', 'Quebec']
- `description_fr` → LOW cardinality (3). Example values: ['Colombie-Britannique', 'Ontario', 'Québec']

---

## Table: `vehicle`

**Row Count:** 52

| Column | Declared Type | SQLite Affinity | PK | Nullable |
|--------|---------------|-----------------|----|----------|
| vehicle_id | INTEGER | INTEGER | True | False |
| policy_id | INT UNSIGNED | INTEGER | False | False |
| province_id | INT UNSIGNED | INTEGER | False | False |
| vin | TEXT | TEXT | False | False |
| make | TEXT | TEXT | False | True |
| year | INTEGER | INTEGER | False | False |

**Relationships:**
- `vehicle.province_id` → `province.province_id`
- `vehicle.policy_id` → `policy.policy_id`

**Indexes:**
- `sqlite_autoindex_vehicle_1` (vehicle_id) UNIQUE

**Column Intelligence:**
- `vehicle_id` → HIGH cardinality (52). Values not enumerated.
- `policy_id` → LOW cardinality (16). Example values: ['1', '2', '3', '4', '5']
- `province_id` → LOW cardinality (3). Example values: ['1', '2', '3']
- `vin` → HIGH cardinality (52). Values not enumerated.
- `make` → LOW cardinality (4). Example values: ['None', 'BMW', 'Mazda', 'Mercedes', 'Toyota']
- `year` → LOW cardinality (20). Example values: ['1996', '1997', '1998', '1999', '2000']

---
