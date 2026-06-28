# Skill: Plan Conversion and Data Migration
**Skill-ID:** 32-Plan-Conversion-and-Data-Migration
**World:** Retirement World v1.0
**Category:** Implementation & Data Integration
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill defines the plan conversion and data migration process — what data must be migrated, how it is validated, the common failure points, and the reconciliation requirements before go-live. A failed or incomplete conversion silently corrupts participant records and creates compliance failures that may persist for years.

---

## 1. What a Plan Conversion Is

A plan conversion occurs when a plan transitions from one recordkeeper to another. The conversion involves:
- Migrating all participant-level data from the prior recordkeeper
- Reconciling migrated data to the prior provider's final records and the trust
- Configuring the new platform with the plan's design parameters
- Going live on the new platform while imposing a blackout period on the plan

Conversions are typically structured around a "conversion date" — the last business day on the prior system. Data as of that date is migrated to the new system.

---

## 2. Data Migration Scope

**Participant-level data to migrate:**

| Data Category | Detail |
|---|---|
| Account balances | By source/money type and by investment fund as of the conversion date |
| Transaction history | Typically 2–3 prior plan years; full history if contractually required |
| Vesting service records | Year-by-year service history per participant |
| Loan data | Outstanding principal balance, interest rate, origination date, repayment schedule |
| Beneficiary designations | Primary and contingent; spousal consent status |
| Enrollment status | Deferral rate; investment elections |
| Compliance testing history | Current and prior plan year testing data |
| Notice delivery records | SPD delivery; required notice history |

**Plan-level data to migrate:**
- Plan document and adoption agreement (all historical versions with effective dates)
- Plan design configuration (all parameters)
- Prior year 5500 data (for TPA continuity)
- Forfeiture account balance

---

## 3. Common Data Quality Issues in Census Data

**Census data** is the employer's employee data file — the foundation for eligibility, vesting, and compliance testing.

| Data Issue | Impact |
|---|---|
| Missing or invalid SSNs | Cannot match participant to account; prevents 1099-R filing |
| Incorrect dates of birth | Wrong eligibility age calculation; wrong RMD age |
| Incorrect dates of hire | Wrong service calculation; wrong vesting |
| Missing hours data | Cannot apply hours-based eligibility or vesting method |
| Incorrect employment status | Contributions processed for already-terminated employees |
| Inconsistent compensation data | Nondiscrimination testing errors |
| Missing rehire dates | Incorrect break-in-service and service restoration calculations |

**Platform requirements:**
- Validate all census records before loading to the participant database
- Generate a census validation exception report listing every failing record with the specific issue
- Require exception resolution before enrollment or contribution processing begins
- Maintain the source census file for audit purposes

---

## 4. Payroll Data Mapping Challenges

When a plan switches recordkeepers, the prior recordkeeper's contribution source codes must be mapped to the new platform's money types. Common challenges:

| Challenge | Description |
|---|---|
| Multiple payroll codes → one money type | Payroll may use separate codes for employee regular deferral and catch-up; both map to pre-tax deferral |
| Undifferentiated Roth | Payroll encodes all deferrals in one bucket; Roth not clearly separated |
| Loan repayments in contribution files | Loan repayments included without clear labeling; must be separated from contributions |
| Legacy money types | Prior recordkeeper may have used custom money types not matching standard categories |
| Off-cycle payroll periods | Supplemental and off-cycle payrolls may use different source codes |

**Platform requirements:**
- Document all payroll source code mappings in the integration configuration
- Test the mapping with actual prior-period payroll data before going live
- Flag any unmapped source codes as exceptions before accepting any payroll file
- Maintain mapping documentation for audit and future troubleshooting

---

## 5. Contribution Reconciliation Concepts

Conversion reconciliation ensures that the amounts migrated to the new recordkeeper match the prior provider's records and the trust.

**Three-way reconciliation at conversion:**
1. **Prior recordkeeper records:** Total account balances by participant and by fund
2. **Trust statement:** Total plan assets by fund as of the conversion date
3. **New recordkeeper intake:** Loaded balances as expected after conversion

All three must agree. Common discrepancy causes:
- In-flight transactions at the conversion date (trades not yet settled)
- Pending contributions not yet posted on the prior system
- Rounding differences accumulated over the plan's history
- Fund pricing differences (prior system used a stale NAV)
- Missing participants or accounts

**Platform requirements:**
- Generate a three-way reconciliation report as part of conversion validation
- Flag every discrepancy by participant, source, and fund
- Require all discrepancies to be resolved before the go-live date
- Maintain the reconciliation report and all supporting documents for audit

---

## 6. Blackout Period During Conversion

A blackout period is typically required during a plan conversion to prevent participant transactions while data is being migrated and the platform is being validated.

**Minimum blackout notice:** At least 30 days advance notice to participants [DATE-VERIFY — confirm current minimum notice requirement]

**Platform requirements:**
- Configure the blackout period start and end dates
- Restrict all participant-initiated transactions during the blackout period
- Generate the ERISA 101(i) blackout notice and track delivery
- After conversion goes live, verify all balances before lifting the blackout

See Skill 14 (Investment Management) for blackout period details.

---

## 7. Go-Live Validation Checklist

Before lifting the blackout and going live on the new platform:
- [ ] All participant records loaded and validated against prior provider's records
- [ ] Account balances by source and fund reconciled to trust
- [ ] Loan data verified (principal balance, repayment schedule, interest rate)
- [ ] Beneficiary designations loaded and verified
- [ ] Vesting service records loaded and verified against census data
- [ ] Payroll integration configured and tested with actual prior payroll data
- [ ] Trust/custodian integration tested and confirmed
- [ ] Plan design parameters configured and verified against adoption agreement
- [ ] Required notices generated and queued for delivery
- [ ] All compliance testing data loaded for the current plan year-to-date

---

## 8. Post-Conversion Monitoring

After go-live, the platform must monitor for:
- Discrepancies that emerge after the blackout is lifted (participant-reported balance errors)
- Payroll integration failures in the first 2–3 payroll cycles
- Vesting calculation errors (may not appear until termination processing)
- Loan repayment tracking errors (may appear after the first payment cycle)

**Platform requirements:**
- Maintain a conversion issue log for tracking and resolving post-go-live discrepancies
- Escalation path for conversion issues that affect participant account accuracy
- Retention of all conversion source data for reference during post-conversion resolution

---

## Agent Rules

- Data migration without a completed three-way reconciliation is not acceptable — every discrepancy must be resolved or formally accepted in writing by the plan sponsor before go-live.
- Blackout notice is mandatory for conversions — the 30-day minimum notice period must be respected. [DATE-VERIFY]
- Census data quality issues must be resolved before enrollment begins — unresolved census issues cascade into eligibility errors, vesting errors, and compliance testing failures.
- The conversion source data (prior provider records, census file, trust statement) must be retained for at least the ERISA record retention period even after conversion is complete.
- Payroll mapping must be tested with actual prior payroll data — sample data test is necessary but not sufficient.

---

## Sources

- ERISA Section 101(i) (Blackout Notice) | U.S. Department of Labor | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- SPARK Institute File Format Standards | https://www.sparkinstitute.org | Retrieved 2026-03-06
- DOL ERISA Regulations | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- ASPPA Plan Conversion Resources | https://www.asppa.org | Retrieved 2026-03-06
