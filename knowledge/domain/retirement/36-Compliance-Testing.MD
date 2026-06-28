# Skill: Compliance Testing — Operational Cycle and Platform Architecture
**Skill-ID:** 36-Compliance-Testing
**World:** Retirement World v1.0
**Category:** Compliance Operations
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill defines the operational compliance testing cycle — how testing data is collected throughout the plan year, how tests are executed (platform-integrated vs. TPA-exported), what the platform must do to support each test, and how corrective actions are posted. This is the operational complement to Skill 05 (Nondiscrimination-Testing), which defines the regulatory test frameworks. Both skills must be used together.

---

## 1. The Compliance Testing Cycle

Compliance testing is not purely a year-end event — it requires data collection and monitoring throughout the plan year.

| Phase | Timing | Activities |
|---|---|---|
| **Ongoing monitoring** | Throughout year | 415 annual additions monitoring; elective deferral limit monitoring; HCE flagging; LTPT hours tracking |
| **Mid-year check** | Optional (Q2/Q3) | ADP/ACP projection testing; identify trends; plan design adjustments if needed |
| **Year-end data freeze** | After final payroll | Close contribution data for the plan year; HCE list finalized |
| **Test execution** | After year-end data freeze | Run all tests (ADP, ACP, 415, 416, 410(b), 401(a)(4)) |
| **Results review** | Within days of test run | TPA and plan sponsor review test results |
| **Corrective action** | Per IRS correction deadlines | Post QNEC/QMAC or process excess refunds |
| **Documentation** | After corrections complete | Retain test data, results, and correction evidence for 6+ years |

---

## 2. Data Collection Requirements Per Test

### ADP Test Data

For each eligible employee (HCE and NHCE):
- Total elective deferrals (pre-tax and Roth) for the plan year
- W-2 compensation for the plan year (or the compensation definition elected by the plan)
- HCE / NHCE classification for the plan year
- Eligibility status for the plan year (eligible vs. excluded)

**Platform collection:** Aggregate from Contribution Records (source = employee pre-tax + designated Roth) and the Participant Record (compensation, eligibility status, HCE flag).

### ACP Test Data

For each eligible employee:
- Total employer matching contributions and employee after-tax contributions for the plan year
- Compensation (same definition as ADP test, per plan election)
- HCE / NHCE classification

**Platform collection:** Aggregate from Contribution Records (source = employer match + after-tax).

### 415 Annual Additions Data

For each participant:
- All annual additions: employee pre-tax + Roth + employer match + employer non-elective + after-tax + forfeitures allocated
- Compensation (415 compensation definition per plan document)
- Prior-year data if the participant participated in another plan of the same employer

**Platform collection:** Running total maintained throughout the year; updated with each payroll cycle.

### 416 / Top-Heavy Data

For each participant:
- Account balances as of the determination date (generally December 31 of the prior plan year)
- Key Employee vs. Non-Key Employee classification
- In-service distributions made during the 5-year period preceding the determination date (must be added back)
- Rollovers from non-related employers made within the determination year

**Platform collection:** Snapshot of account balances at determination date; Key Employee classification from ownership data.

### 410(b) Coverage Data

For each employee (all controlled group employees, not just plan participants):
- Employment status (eligible vs. excluded)
- HCE / NHCE classification
- Whether the employee is "benefiting" under the plan (receiving an employer contribution for the plan year, or eligible to make deferrals)

**Platform collection:** Full census data including excluded employees; requires controlled group aggregation.

### 401(a)(4) General Nondiscrimination Data

Depends on the testing method (contributions-based or benefits-based cross-testing):
- For contributions-based: same data as ADP/ACP
- For cross-testing (general test on benefits): projected benefit calculations

---

## 3. HCE Determination Workflow

The HCE list is finalized after the plan year closes but before testing is run.

**HCE determination process:**
1. Compile all employees who were active during the plan year
2. Identify 5%-or-greater owners for both the current and prior plan year
3. Apply the prior-year compensation test: identify employees whose compensation in the prior plan year exceeded the IRS-indexed HCE threshold (plan-configurable per current IRS table — do not hardcode)
4. If the top-paid group election is in effect, limit the HCE list to the top-paid 20% of employees by compensation
5. Finalize the HCE list for the plan year
6. Identify NHCEs as the complement of HCEs among all eligible employees

**Platform requirements:**
- Maintain prior-year compensation data per employee
- Support ownership percentage tracking for 5% owner identification
- Support top-paid group election configuration
- Generate and store the HCE list with the plan year it applies to

---

## 4. ADP/ACP Test Execution

**Step 1 — Calculate ADPs and ACPs:**
- For each eligible employee, calculate the deferral percentage: deferrals ÷ compensation
- Average the ADPs for HCEs → HCE ADP
- Average the ADPs for NHCEs → NHCE ADP

**Step 2 — Apply the permitted disparity (IRS formula):**
- The HCE ADP may not exceed the NHCE ADP by more than the IRS-permitted spread (plan-configurable per current IRS rules — do not hardcode)
- If HCE ADP exceeds the permitted maximum: the test fails

**Step 3 — Calculate corrective amounts (if test fails):**
- **Excess contribution per HCE:** Determine the level at which HCE deferrals must be reduced to pass
- **Corrective refund amount:** The amount each HCE must receive as a taxable refund, calculated starting from the HCE with the highest deferral percentage and working down (leveling method)
- **Or QNEC alternative:** Calculate the QNEC amount needed to raise the NHCE ADP to a level that satisfies the test

**Platform requirements:**
- Perform ADP/ACP calculations per the IRS test methodology
- Apply the prior-year or current-year NHCE data method per the plan's election
- Generate test results with detailed output (HCE ADP, NHCE ADP, permitted maximum, excess amount)
- Calculate corrective refund amounts per HCE using the leveling method
- Or: calculate QNEC amount needed for each NHCE to correct via employer contribution

---

## 5. Integration vs. Export Testing Models

### Platform-Integrated Testing

The compliance testing engine is built into the recordkeeping platform. Test calculations are performed within the platform using the platform's own data.

**Advantages:**
- No data export required
- Results available immediately
- Data integrity maintained within a single system

**Platform requirements:**
- Compliance testing engine as a native module
- Real-time or near-real-time test execution
- Results stored in the platform with audit trail

### TPA-Export Testing Model

The recordkeeper exports compliance testing data to the TPA's separate testing system (e.g., FIS Relius, Pension Pro, ASC). The TPA runs the tests and imports results or corrective actions back into the recordkeeping system.

**Data export requirements:**
- Standardized export format (SPARK-format or agreed TPA format)
- Participant-level data: compensation, deferrals, employer contributions, by source, by HCE/NHCE status
- Export must be auditable (hash or record count confirmation)

**Data import requirements:**
- Import corrective action amounts (QNEC/QMAC, excess refund amounts) from TPA system
- Post corrective transactions based on TPA-calculated results

---

## 6. Corrective Action Processing

**Excess refund processing:**
1. Receive corrective refund amounts from the test engine or TPA
2. Validate that the amounts are accurate and within the test window
3. Process excess contribution refunds as distributions to each affected HCE
4. Apply appropriate tax withholding (excess contributions are generally taxable in the year of the refund, not the year of contribution)
5. Generate 1099-R for each refund with the appropriate distribution code
6. Verify the plan passes the test after refunds

**QNEC/QMAC processing:**
1. Receive QNEC/QMAC amounts from the test engine or TPA
2. Post corrective contributions to the QNEC or QMAC source for each eligible NHCE
3. Apply 100% immediate vesting to QNEC/QMAC contributions
4. Verify the plan passes the test after corrective contributions
5. Include QNEC/QMAC amounts in 415 annual additions monitoring

---

## 7. Testing Documentation and Retention

All compliance testing documentation must be retained for the ERISA Section 107 minimum retention period (at least 6 years). [DATE-VERIFY]

**Documentation to retain:**
- Test data extract (the input data used for testing)
- Test calculations (showing each step of the test)
- Test results (pass/fail; amounts by HCE/NHCE)
- Corrective action documentation (amounts, recipients, dates)
- Correction evidence (contribution records, distribution records)

---

## Agent Rules

- **[COMPLIANCE-SENSITIVE]** — Compliance testing deadlines are regulatory. ADP/ACP correction deadlines are different for excise-tax-free correction vs. late correction. [DATE-VERIFY before writing any correction timeline requirement]
- HCE determination is the foundation of ADP/ACP testing — an error in HCE classification invalidates the test results.
- Never hardcode HCE compensation thresholds, ADP/ACP permitted spreads, or 415 limits — all are IRS-indexed parameters.
- If the plan is a safe harbor plan (Traditional or QACA), ADP/ACP testing is not required — verify safe harbor status before designing testing workflows.
- Controlled group aggregation is mandatory for 410(b) and 401(a)(4) testing — the platform must aggregate all controlled group employees for coverage analysis.

---

## Sources

- IRC Sections 401(k), 401(m), 415, 416, 410(b), 401(a)(4) | IRS | https://www.irs.gov/retirement-plans | Retrieved 2026-03-06
- IRS ADP/ACP Test Guidance | https://www.irs.gov/retirement-plans/401k-plan-fix-it-guide-the-adp-and-acp-tests | Retrieved 2026-03-06
- ASPPA Compliance Testing Resources | https://www.asppa.org | Retrieved 2026-03-06
- SPARK Institute Data Standards | https://www.sparkinstitute.org | Retrieved 2026-03-06
