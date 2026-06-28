# Skill: Plan Setup and Onboarding
**Skill-ID:** 22-Plan-Setup-and-Onboarding
**World:** Retirement World v1.0
**Category:** Plan Administration Lifecycle
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill defines the plan setup and onboarding process — from adoption agreement intake through live production. A misconfigured plan setup creates compliance failures that may not be discovered until the first compliance testing cycle. Every plan parameter must be traceable to an adoption agreement provision before the plan goes live.

---

## 1. Plan Document and Adoption Agreement Intake

The plan document and adoption agreement define all plan parameters. The platform must capture and version the adoption agreement as the **configuration source of truth**.

**Key principle:** Every plan design parameter in the platform must trace to an adoption agreement provision. Platform configuration that has no corresponding adoption agreement provision represents unauthorized plan operation.

**Process:**
1. Receive the executed plan document and adoption agreement from the plan sponsor or TPA
2. Review the adoption agreement for all plan design parameters
3. Enter all parameters into the platform configuration
4. Verify configured parameters against the adoption agreement
5. Document the verification with a sign-off from the plan sponsor or TPA

**Platform requirements:**
- Store the plan document and adoption agreement in the document management system with an effective date
- Version-control the adoption agreement (each amendment creates a new version)
- Link platform configuration parameters to their adoption agreement source
- Maintain prior adoption agreement versions for audit and retroactive recalculation

---

## 2. Plan Design Parameter Configuration

All of the following must be configured before the plan goes live:

| Parameter Category | Key Parameters |
|---|---|
| **Eligibility** | Age requirement; service requirement; computation method (hours/elapsed time); entry date frequency; exclusion classes; LTPT tracking requirement |
| **Contributions** | Employee deferral limits (pre-tax, Roth); employer match formula; non-elective formula; catch-up eligibility; auto-enrollment default deferral; auto-escalation settings |
| **Vesting** | Schedule type (immediate, cliff, graded) per source; computation method; break-in-service rule |
| **Distributions** | Hardship eligibility and permitted reasons; in-service distribution eligibility; force-out thresholds; loan policy |
| **Safe Harbor** | Election type (none, Traditional, QACA); safe harbor contribution formula |
| **Investment** | QDIA designation; available investment menu; rebalancing options |
| **Compliance Testing** | Safe harbor status; plan year; compensation definition; HCE determination method (prior-year/current-year) |
| **Notices** | Delivery method preferences (electronic/paper); annual notice generation schedule |
| **Tax and Reporting** | Plan year; plan EIN; plan number; TPA relationship; advisor relationship |

---

## 3. Data Migration and Plan Conversion

When a plan transitions from a prior recordkeeper (plan conversion), historical participant data must be migrated and validated.

**Data migration scope:**
- Account balances by source and investment fund as of the conversion date
- Transaction history (typically 2–3 years; full history if available)
- Vesting service records (year-by-year history)
- Loan balances and repayment schedules
- Beneficiary designations
- Compliance testing history (current and prior year)
- Plan document and adoption agreement versions

**Validation process:**
1. Receive conversion data from the prior provider
2. Load data into the platform staging environment
3. Validate participant-level balances by source against the prior provider's records
4. Validate aggregate balances against the trust reconciliation statement
5. Validate vesting service records against census data
6. Validate loan data (principal balance, interest rate, repayment schedule)
7. Resolve all discrepancies before going live

**Platform requirements:**
- Support data import from standard formats (fixed-width, delimited, SPARK-standard)
- Provide validation reports showing discrepancies by participant and data type
- Maintain a complete audit trail of the conversion data load and validation
- Implement a blackout period during the conversion (see Skill 14)
- Notify participants of the blackout period at least 30 days in advance [DATE-VERIFY]

---

## 4. Trust Setup and Custodian Connection

Before contributions can be funded, the trust account relationship must be established:
- New trust account opened with the custodian/trustee
- Trust account numbers assigned per contribution source or fund (depending on trust structure)
- Platform integrated with the trust accounting system
- Test transactions run to verify trust interface
- Initial asset transfer from prior custodian reconciled and confirmed

**Platform requirements:**
- Configure custodian relationship in the platform (custodian name, trust account numbers, settlement instructions)
- Test the trade instruction and NAV pricing feed interfaces
- Verify reconciliation workflow between recordkeeping and trust systems
- Confirm custodian-side trust account setup before accepting contributions

---

## 5. Initial Participant Data Load and Validation

Census data from the employer is loaded into the platform before enrollment begins.

**Required census data fields:**
- Employee name; SSN (PII — encrypted in transit and at rest)
- Date of birth; date of hire
- Compensation (YTD and prior year)
- Hours of service (YTD and prior year, if hours method)
- Employment status
- Employee class (union/non-union, full-time/part-time)

**Validation rules:**
- No duplicate SSNs
- Valid date formats for dates of birth and hire
- Date of birth precedes date of hire
- Required fields populated for all active employees
- Compensation amounts are positive and reasonable

**Platform requirements:**
- Validate all census records before loading to the participant database
- Generate a validation exception report for records failing validation
- Route exceptions to the plan sponsor or TPA for resolution before enrollment begins
- Maintain the initial load data file for audit purposes

---

## 6. Payroll Integration Setup

Payroll integration must be configured and tested before the first payroll cycle.

**Configuration steps:**
1. Define payroll file format (fixed-width, delimited, SPARK API)
2. Map payroll source codes to platform money types
3. Configure SFTP connection or API credentials
4. Perform end-to-end test with sample payroll data
5. Validate that test data maps correctly to participant records and money types
6. Confirm payroll cycle schedule and file delivery timing
7. Sign off on integration before first live payroll

**Platform requirements:**
- Support both file-based (SFTP) and API-based (SPARK June 2025 guidelines) integrations
- Maintain payroll source code mapping table per plan
- Validate integration configuration with a parallel test before go-live

---

## 7. Go-Live Checklist

Before the plan goes live, verify:
- [ ] Adoption agreement parameters fully configured and verified against signed document
- [ ] Plan document and adoption agreement stored in document management system
- [ ] All participant records loaded and validated
- [ ] Payroll integration configured and tested
- [ ] Trust/custodian integration tested
- [ ] QDIA designated and QDIA notice template prepared
- [ ] Safe harbor notice template prepared (if safe harbor plan)
- [ ] Auto-enrollment logic configured and tested (if auto-enrollment plan)
- [ ] 402(f) Special Tax Notice template prepared
- [ ] All required notice delivery workflows configured
- [ ] Blackout period established and participant notification sent (for conversions)
- [ ] TPA portal access configured and tested
- [ ] Compliance testing parameters configured

---

## Agent Rules

- **Every plan configuration parameter must trace to an adoption agreement provision.** Undocumented configuration is an operational risk and potential plan qualification failure.
- Data migration validation is mandatory before go-live — do not accept converted data without reconciliation to the prior provider and trust statements.
- The blackout period notification for plan conversions must be sent at least 30 days before the conversion date. [DATE-VERIFY — confirm current minimum notice period]
- Census data quality issues must be resolved before enrollment begins — do not enroll participants based on unvalidated census data.
- Payroll integration mapping must be tested with real payroll data, not just sample data — edge cases appear in real payroll files.

---

## Sources

- ERISA Sections 101, 104 | U.S. Department of Labor | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- SPARK Institute API Integration Guidelines, June 2025 | https://www.sparkinstitute.org | Retrieved 2026-03-06
- IRS Retirement Plans — Plan Document Requirements | https://www.irs.gov/retirement-plans | Retrieved 2026-03-06
- ASPPA Plan Setup and Conversion Resources | https://www.asppa.org | Retrieved 2026-03-06
