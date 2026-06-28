# Skill: Glossary — Retirement World Term Reference
**Skill-ID:** 39-Glossary
**World:** Retirement World v1.0
**Category:** Reference
**Last-Reviewed:** 2026-03-06

---

## Purpose

This glossary is the authoritative term reference for the Retirement World domain. Every term used in the Retirement World documents and skills is defined here with its regulatory context and platform implication. Cross-reference skill files for full operational detail.

---

## A

**ACP Test (Actual Contribution Percentage Test)**
Annual nondiscrimination test comparing the average contribution percentage of HCEs (employer matching and employee after-tax contributions) to that of NHCEs. Failure requires corrective action.
*System context:* Driven by contribution data by source; applies to plans with matching or after-tax contributions not using ACP safe harbor. See Skill 05, Skill 36.

**ADP Test (Actual Deferral Percentage Test)**
Annual nondiscrimination test comparing the average elective deferral percentage of HCEs to that of NHCEs. Failure requires refunds to HCEs or QNEC/QMAC contributions to NHCEs.
*System context:* Applies to 401(k) plans not using ADP safe harbor; requires HCE/NHCE classification of all eligible employees. See Skill 05, Skill 36.

**Adoption Agreement**
The plan sponsor's documented elections within a prototype or volume submitter plan document — the configuration source of truth for all plan design parameters.
*System context:* Every platform configuration parameter must trace to an adoption agreement provision. See Skill 09, Skill 22.

**Annual Additions (IRC 415)**
The total of all employer contributions, employee elective deferrals (pre-tax and Roth), employee after-tax contributions, and forfeitures allocated to a participant's account in a plan year. Does not include rollover contributions or loan repayments.
*System context:* Monitored against the 415 limit (plan-configurable per current IRS table) throughout the year. See Skill 05.

**Anti-Cutback Rule (ERISA Section 204(g), IRC Section 411(d)(6))**
Prohibition on plan amendments that eliminate or restrict optional forms of benefit already accrued by participants.
*System context:* Applies to vesting schedule amendments and plan mergers/spinoffs. [RECOMMEND LEGAL/COMPLIANCE REVIEW]. See Skill 25, Skill 34.

**Auto-Enrollment**
A plan design feature where eligible employees are automatically enrolled at a default deferral rate unless they affirmatively opt out. Mandatory for new 401(k) and 403(b) plans under SECURE 2.0 (effective date plan-configurable).
*System context:* Default deferral rate and QDIA must be configured; opt-out workflow required; notice delivery required. See Skill 12.

**Auto-Escalation**
A plan feature that automatically increases a participant's deferral rate by a plan-configured increment on a plan-configured schedule until a plan-configured maximum is reached.
*System context:* Scheduled trigger logic; opt-out capability; notice requirement. See Skill 13.

**Auto-Rollover IRA**
An IRA established on behalf of a terminated participant for their plan balance when it falls within the mandatory rollover range and the participant does not affirmatively elect otherwise.
*System context:* Force-out processing; balance threshold monitoring; DOL safe harbor compliance. See Skill 17.

---

## B

**Beneficiary**
A person or entity designated by the participant to receive the account balance upon the participant's death. May be primary or contingent; spousal consent rules may apply.
*System context:* Beneficiary record tied to participant; triggers death distribution workflow upon participant death. See Skill 20.

**Blackout Period**
A period during which participant rights to direct investments or obtain loans or distributions are temporarily suspended (e.g., during a plan conversion or fund mapping change).
*System context:* Requires ERISA 101(i) advance notice; investment and transaction restrictions enforced; blackout dates logged. See Skill 14.

**Break in Service**
A plan year in which an employee fails to complete a minimum number of hours of service (or equivalent under elapsed time method), potentially interrupting vesting service accrual.
*System context:* Tracked in participant service record; affects vesting and eligibility upon rehire. See Skill 06, Skill 21.

---

## C

**Catch-Up Contribution**
An additional elective deferral permitted for participants who have reached a plan-configurable age threshold (per IRS rules), allowing contributions above the standard annual deferral limit. Super Catch-Up (ages 60–63) introduced by SECURE 2.0.
*System context:* Age-based eligibility flag; separate limit monitoring from standard deferrals; mandatory Roth for higher earners per SECURE 2.0 [DATE-VERIFY]. See Skill 07, Skill 13.

**Compensation (415, W-2, Includible)**
Three primary compensation definitions used in retirement plans:
- **415 Compensation:** Under IRC Section 415(c)(3); basis for annual additions limit
- **W-2 Compensation:** Wages reported on Form W-2
- **Includible Compensation:** Used in 403(b) plans; generally W-2 from the plan sponsor employer
*System context:* Compensation definition is a plan-configurable parameter in the adoption agreement; drives contribution formulas, limit calculations, and nondiscrimination testing. See Skill 05.

**Controlled Group**
Two or more business entities under common ownership treated as a single employer for retirement plan qualification purposes under IRC Section 414.
*System context:* Multi-EIN configuration; aggregated testing data; shared employee tracking. See Skill 35.

---

## D

**Deemed Distribution**
The tax event that occurs when a participant loan is treated as distributed due to failure to repay within the cure period, without an actual cash payment.
*System context:* Triggered after cure period expiration; generates 1099-R; loan status updated; post-deemed repayments are after-tax basis. See Skill 15.

**Deferred Vested Participant**
A terminated participant who retains a vested balance in the plan but has not yet taken a distribution.
*System context:* Ongoing account maintenance; RMD monitoring; DOL Lost and Found reporting obligation (SECURE 2.0, when effective). See Skill 17.

**Designated Roth Account**
A separately accounted portion of an employee's account representing designated Roth contributions (after-tax) and their earnings. Qualified distributions are tax-free. No lifetime RMDs under SECURE 2.0.
*System context:* Separate source tracking; distinct tax treatment for distributions; Roth RMD exemption for living participants. See Skill 10.

**Directed Trustee**
A trustee that acts only on instructions from a named fiduciary; does not exercise investment discretion. Most common trustee type in DC plans.
*System context:* Platform sends explicit trade instructions; trustee confirms execution. See Skill 37.

**Distribution Code (1099-R)**
IRS-designated codes that appear on Form 1099-R to describe the nature of a retirement distribution. Common codes: 1 (early, no exception), 4 (death), 7 (normal), B (Roth), G (direct rollover).
*System context:* Must be accurate for all 1099-R filings; incorrect codes create IRS matching and participant tax issues. See Skill 18.

---

## E

**EACA (Eligible Automatic Contribution Arrangement)**
An automatic enrollment plan arrangement meeting IRS requirements, including a permissive 90-day withdrawal right and default investment in a QDIA.
*System context:* 90-day withdrawal window must be enforced; QDIA notice required. See Skill 12.

**Eligible Rollover Distribution (ERD)**
A distribution from a qualified plan that is eligible to be rolled over to another eligible retirement plan or IRA. Subject to mandatory 20% federal withholding unless directly rolled over. Excludes RMDs, hardship distributions, and certain periodic payments.
*System context:* Triggers 402(f) Special Tax Notice; mandatory 20% withholding if not directly rolled over. See Skill 18.

**Elective Deferral**
A contribution made by an employee from their compensation to a qualified plan on a pre-tax (Traditional) or after-tax (Roth) basis pursuant to a salary reduction agreement. Always 100% immediately vested.
*System context:* Subject to annual limit (plan-configurable per IRS table); tracked as separate source from employer contributions. See Skill 10, Skill 13.

**Entry Date**
The date on which a newly eligible employee is permitted to begin participation in the plan. Entry dates are plan-configurable.
*System context:* Eligibility engine calculates projected entry date; enrollment workflow triggered on entry date. See Skill 11.

**EPCRS (Employee Plans Compliance Resolution System)**
The IRS framework for correcting retirement plan qualification failures through self-correction (SCP), voluntary correction (VCP), or audit correction (Audit CAP).
*System context:* Correction workflows must support EPCRS documentation; audit trail required. See Skill 33.

**ERISA (Employee Retirement Income Security Act of 1974)**
Federal law establishing minimum standards for most voluntarily established retirement and health plans in private industry to protect plan participants and beneficiaries.
*System context:* Governs fiduciary duties, participant rights, reporting and disclosure, and enforcement for ERISA-covered plans. ERISA applicability is arrangement-dependent, not plan-type-dependent. See Skill 04, Skill 08.

---

## F

**Fiduciary (ERISA)**
Under ERISA Section 3(21), any person who exercises discretionary authority or control over plan management or assets, renders investment advice for a fee, or has discretionary responsibility in plan administration.
*System context:* Fiduciary actions must be logged with audit trail; platform must not assume fiduciary functions without explicit design authorization. See Skill 04.

**Force-Out Distribution**
An involuntary distribution of a terminated participant's small balance when it falls below the plan-configured mandatory distribution threshold (per IRS rules). Balances in the mid-range must be rolled over to an auto-rollover IRA.
*System context:* Balance threshold monitoring; automatic rollover IRA processing; participant notification. See Skill 17.

**Forfeiture**
The unvested portion of an employer contribution account that a participant loses upon termination before satisfying the plan's vesting schedule.
*System context:* Credited to forfeiture account; used per plan document (reduce contributions, pay expenses, fund QNEC/QMAC); timing governed by plan document and IRS rules. See Skill 06, Skill 24.

**Form 1099-R**
IRS tax form reporting distributions from retirement plans. Issued to distributees and filed with the IRS. Distribution codes determine tax treatment.
*System context:* Generated from distribution records; codes must be accurate; delivery and IRS filing are time-sensitive. See Skill 18.

**Form 5500**
Annual information return filed by most ERISA-covered plans with the DOL and IRS, reporting plan financial condition, investments, and operations.
*System context:* Recordkeeper provides financial and participant data to plan sponsor or TPA for 5500 preparation. See Skill 24.

---

## H

**Hardship Withdrawal**
A distribution from a 401(k) or 403(b) plan due to an immediate and heavy financial need that cannot be satisfied from other reasonably available resources.
*System context:* Qualifying reason validation; self-certification workflow (SECURE 2.0); documentation and audit trail; generally not an ERD (no mandatory 20% withholding). See Skill 16.

**HCE (Highly Compensated Employee)**
An employee who meets IRS-defined ownership or prior-year compensation criteria (thresholds are IRS-indexed plan-configurable parameters). HCE classification affects ADP/ACP testing.
*System context:* Annual HCE determination workflow; prior-year compensation lookback required; plan-level HCE list used in testing. See Skill 05, Skill 36.

**Hours of Service**
A measure of employee service used for eligibility and vesting calculations. An employee earns hours of service for each hour for which they are paid or entitled to be paid.
*System context:* Hours tracked per computation period; source data is payroll or HR system; used in eligibility and vesting engines. See Skill 11, Skill 06.

---

## I–K

**In-Service Withdrawal**
A distribution from a plan while the participant is still employed. Permitted only if the plan document allows and IRC requirements are met.
*System context:* In-service distribution type must be authorized in plan design; age eligibility check; applicable tax and withholding rules apply. See Skill 16.

**Key Employee**
An employee who meets IRS-defined officer, ownership, or compensation criteria (thresholds are IRS-indexed plan-configurable parameters). Key Employee classification is used in top-heavy testing.
*System context:* Annual Key Employee determination; used in 416 top-heavy test; minimum contribution obligations if plan is top-heavy. See Skill 05.

---

## L

**Loan (Plan Loan)**
A loan made to a participant from their vested account balance, governed by IRC Section 72(p) and the plan's loan policy.
*System context:* Origination, repayment, deemed distribution, and offset workflows; balance tracking; 72(p) limit calculation. See Skill 15.

**LTPT Employee (Long-Term Part-Time Employee)**
Under SECURE Act and SECURE 2.0, a part-time employee who meets consecutive-year qualifying hours thresholds must be permitted to make elective deferrals. The plan may exclude LTPT employees from employer contributions.
*System context:* Multi-year hours tracking; eligibility flag; separate treatment from standard eligibility. See Skill 11.

---

## M–N

**Match True-Up**
A year-end corrective employer matching contribution for participants whose match, calculated annually, exceeds the match funded on a per-payroll basis throughout the year.
*System context:* Year-end match recalculation; corrective contribution; interaction with 415 limits. See Skill 24.

**Money Type / Contribution Source**
The classification of a contribution or balance by its origin and regulatory characteristics (employee pre-tax, Roth, employer match, profit sharing, rollover, after-tax, QNEC, QMAC, PLESA). Drives vesting, distribution eligibility, and tax treatment.
*System context:* Every transaction tagged by source; vesting and distribution logic driven by source. See Skill 10.

**NAV (Net Asset Value)**
The per-unit price of a mutual fund or collective investment trust calculated after market close each business day.
*System context:* Applied to participant account unit balances for daily valuation; drives recordkeeper-trust reconciliation. See Skill 29, Skill 37.

**NHCE (Non-Highly Compensated Employee)**
Any eligible employee who is not an HCE. NHCEs are the comparison group in ADP/ACP nondiscrimination testing.
*System context:* NHCE list determined as complement of HCE list; average NHCE ADP/ACP is the test benchmark. See Skill 05.

---

## P–Q

**Participant-Directed Investment**
A plan design where participants control the investment of their own account balances among plan investment options. Enables ERISA Section 404(c) fiduciary relief.
*System context:* Investment election capture; fund transfer processing; QDIA default logic. See Skill 14.

**PEP (Pooled Employer Plan)**
A type of multiple employer plan operated by a registered Pooled Plan Provider (PPP), allowing unrelated employers to participate in a single plan structure with the PPP as plan administrator and named fiduciary.
*System context:* Multi-employer data structure; PPP as administrative fiduciary; employer-level plan design segmentation. See Skill 02.

**Plan Document**
The legal document establishing and governing the retirement plan, including all terms, eligibility rules, contribution formulas, vesting schedules, and participant rights.
*System context:* All platform configuration must align with the plan document; version controlled in document management system. See Skill 30.

**Plan Sponsor**
The employer or employee organization that establishes and maintains the retirement plan. Holds ultimate responsibility for plan operation.
*System context:* Plan sponsor portal; approval workflows; amendment authority. See Skill 03.

**Plan Year**
The 12-month period designated in the plan document for plan operations and compliance testing. Most plans use the calendar year; any 12-month period may be elected.
*System context:* Drives all annual calculation periods, testing cycles, and filing deadlines.

**PLESA (Pension-Linked Emergency Savings Account)**
A short-term savings account linked to a DC plan (SECURE 2.0) allowing non-HCE participants to save after-tax dollars for emergency use with flexible withdrawal rights.
*System context:* New account/source type; contribution limit monitoring; employer match interaction; withdrawal processing without penalty. [DATE-VERIFY]. See Skill 10, Skill 16.

**QACA (Qualified Automatic Contribution Arrangement)**
An automatic enrollment arrangement meeting QACA requirements, including minimum default deferral rates, auto-escalation, and required employer contributions. Provides ADP/ACP safe harbor.
*System context:* Auto-enrollment engine with QACA minimums; up to 2-year cliff vesting on safe harbor contributions; QACA notice required. See Skill 12.

**QDRO (Qualified Domestic Relations Order)**
A domestic relations order creating or recognizing the right of an alternate payee to plan benefits. Must meet specific ERISA and IRC requirements.
*System context:* Written QDRO procedures required; qualification determination workflow; alternate payee account creation. [RECOMMEND LEGAL/COMPLIANCE REVIEW]. See Skill 20.

**QDIA (Qualified Default Investment Alternative)**
An investment alternative designated as the default investment for participants who do not make an affirmative investment election. Provides fiduciary relief when QDIA requirements are met.
*System context:* QDIA designation in plan configuration; default routing of unapplied contributions; QDIA notice generation. See Skill 12, Skill 14.

**QMAC (Qualified Matching Contribution)**
A corrective employer matching contribution that meets specific IRS requirements (100% immediate vesting; satisfies ACP test requirements). Used to correct ACP test failures.
*System context:* Corrective contribution; immediate vesting; 415 inclusion. See Skill 05, Skill 36.

**QNEC (Qualified Non-Elective Contribution)**
A corrective employer non-elective contribution that meets specific IRS requirements (100% immediate vesting; satisfies ADP/ACP test requirements). Used to correct ADP or ACP test failures.
*System context:* Corrective contribution; immediate vesting; 415 inclusion. See Skill 05, Skill 36.

**Qualified Plan**
A retirement plan meeting the requirements of IRC Section 401(a) or other applicable IRC sections, entitling the employer to a tax deduction and participants to tax-deferred growth.
*System context:* Platform must enforce all qualification requirements through configuration and processing controls. See Skill 08.

---

## R

**RBD (Required Beginning Date)**
The deadline by which a participant must begin receiving Required Minimum Distributions. Determined by the participant's required beginning age (plan-configurable per IRS RMD rules, modified by SECURE 2.0) and employment status.
*System context:* Automated RBD calculation; RMD trigger event. [DATE-VERIFY — confirm current RMD age rules]. See Skill 19.

**Recordkeeper**
The service provider that maintains individual participant account records, processes transactions, and serves as the technology platform for plan administration.
*System context:* CORE is the recordkeeping system. See Skill 03, Skill 27.

**Rehire**
The re-employment of a former employee. Triggers re-evaluation of eligibility, vesting service restoration, forfeiture restoration, and break-in-service rules.
*System context:* Rehire date required; prior service retrieval; re-eligibility determination. See Skill 21.

**Required Beginning Date** — see RBD.

**RMD (Required Minimum Distribution)**
The minimum amount that must be distributed from a retirement account each year after the participant reaches the required beginning date. Calculated using account balance and IRS life expectancy tables. No lifetime RMD for designated Roth accounts in employer plans (SECURE 2.0).
*System context:* Annual RMD calculation; automated distribution trigger; penalty tracking if underdistributed; Roth exemption logic. See Skill 19.

**Rollover (Direct vs. Indirect)**
- **Direct rollover:** Distribution paid directly to an eligible retirement plan or IRA; avoids mandatory 20% withholding.
- **Indirect rollover:** Distribution paid to the participant; must be re-contributed within 60 days; subject to 20% mandatory withholding.
*System context:* Rollover election capture at distribution; withholding logic differs; rollover-in processing. See Skill 18.

---

## S

**Safe Harbor Plan**
A 401(k) plan meeting safe harbor requirements (Traditional or QACA) that is deemed to pass ADP and, in some cases, ACP nondiscrimination testing. Requires required employer contributions and advance notice.
*System context:* Safe harbor flag in plan design; notice generation; employer contribution formula enforcement. See Skill 02, Skill 05.

**SAR (Summary Annual Report)**
A summary of the Form 5500 annual report distributed to plan participants. Must be provided within regulatory deadlines after Form 5500 filing.
*System context:* Generated from year-end financial data; delivery tracked. See Skill 24.

**Short Plan Year**
A plan year of less than 12 months, occurring at plan establishment, termination, or change of plan year. Affects compliance testing, contribution limits, and filing requirements.
*System context:* [EDGE CASE — short plan year logic must be explicitly addressed in acceptance criteria for any affected feature].

**SPARK Institute**
An industry association for retirement plan service providers. Its API Integration Guidelines (June 2025) define standard APIs for retirement data exchange; its DSOB defines cybersecurity standards.
*System context:* SPARK API standards are the reference for all new payroll and custodian integrations. See Skill 28.

**SPD (Summary Plan Description)**
A plain-language document explaining plan terms, participant rights, and claims procedures. Required to be provided to all plan participants within regulatory deadlines.
*System context:* Document management and delivery; version control; delivery tracking. See Skill 08, Skill 30.

---

## T

**Top-Heavy Plan**
A plan in which the account balances of Key Employees exceed a regulatory threshold percentage of total plan assets (plan-configurable per IRS rules). Triggers minimum employer contribution requirements for non-Key employees.
*System context:* Annual top-heavy determination; minimum contribution calculation if top-heavy. See Skill 05.

**TPA (Third Party Administrator)**
A service provider performing plan administration functions (compliance testing, 5500 preparation, plan document maintenance, distribution processing) on behalf of the plan sponsor. May be appointed as Section 3(16) plan administrator.
*System context:* TPA portal access; data exchange; 3(16) appointment tracking. See Skill 03.

**Trustee**
The legal holder of plan assets. May be directed (acts on instructions) or discretionary (exercises independent judgment). In most DC plans, a directed corporate trustee.
*System context:* Trust accounting system integration; trade instruction flow; asset reconciliation. See Skill 37.

---

## U–V

**Universal Availability Rule (403(b))**
Under IRC Section 403(b)(12), all employees of a 403(b) plan sponsor must be permitted to make elective deferrals unless specifically excluded by statute. Permitted exclusions are different from and more limited than 401(k) exclusions.
*System context:* Eligibility logic must enforce Universal Availability for 403(b) plans. See Skill 02, Skill 11.

**VFCP (Voluntary Fiduciary Correction Program)**
A DOL program allowing plan fiduciaries to self-correct certain prohibited transactions (including late deposits) and obtain a no-action letter from DOL. Requires lost earnings calculation and payment.
*System context:* Late deposit correction workflow; lost earnings calculation; DOL application support. See Skill 23, Skill 38.

**Vesting**
The process by which a participant acquires a non-forfeitable right to employer contributions in their account. Elective deferrals are always 100% immediately vested. Employer contributions vest per the plan's vesting schedule.
*System context:* Vesting record tracking; service calculation; vested balance calculation drives distribution and loan eligibility. See Skill 06.

**Vesting Service**
Service credited toward the participant's vesting schedule. May be measured by hours of service or elapsed time, as specified in the plan document.
*System context:* Service tracking from hire date; break-in-service monitoring; vesting percentage calculation engine. See Skill 06.

---

## W–Y

**W-2 Compensation**
Wages reported on Form W-2; a common compensation definition used in plan documents for contribution formulas and nondiscrimination testing.
*System context:* Compensation definition is plan-configurable; the platform must apply the elected definition consistently for all contribution and testing calculations.

**Year of Service**
A 12-month computation period in which an employee completes a plan-configured minimum number of hours of service, earning credit for eligibility or vesting purposes.
*System context:* Hours tracking; computation period determination; year-of-service credit in eligibility and vesting engines. See Skill 06, Skill 11.

---

## Agent Usage Rules Reminder

When using this glossary:
1. **[COMPLIANCE-SENSITIVE]** — Tag requirements involving contribution limits, testing, distributions, RMDs, notices, fiduciary actions, or plan amendments.
2. **[DATE-VERIFY]** — Confirm any effective date or IRS-indexed value before using in a finalized requirement.
3. **Never hardcode** annual dollar limits, compensation thresholds, or percentage caps — reference as plan-configurable parameters.
4. **[GOVERNMENT PLAN — NON-ERISA]** — Tag all 457(b) governmental plan requirements.
5. **[RECOMMEND LEGAL/COMPLIANCE REVIEW]** — Tag QDRO processing, fiduciary boundary questions, and complex anti-cutback scenarios.
6. **[EDGE CASE]** — Explicitly address controlled groups, mid-year amendments, rehire scenarios, QDROs, plan mergers/spinoffs, short plan years, and correction workflows in acceptance criteria.

---

## Sources

- IRS Retirement Plans Glossary | https://www.irs.gov/retirement-plans | Retrieved 2026-03-06
- DOL ERISA Glossary | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- ASPPA Retirement Dictionary | https://www.asppa.org | Retrieved 2026-03-06
- NIPA Retirement Plan Terminology | https://www.nipa.org | Retrieved 2026-03-06
