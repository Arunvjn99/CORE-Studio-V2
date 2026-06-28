# Skill: Death and Beneficiary Processing
**Skill-ID:** 20-Death-and-Beneficiary-Processing
**World:** Retirement World v1.0
**Category:** Participant Lifecycle
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill defines the platform workflows triggered by a participant's death — beneficiary designation lookup, spousal consent validation, QDRO interaction, beneficiary classification, distribution options, and RMD rules for beneficiaries. Death processing requires sensitivity, precision, and rigorous compliance with ERISA and IRC beneficiary rules.

---

## 1. Death Notification

Upon notification of a participant's death, the platform initiates the death processing workflow. Notification may arrive via:
- Plan sponsor or employer HR notification
- Beneficiary or family member contact
- Social Security Administration death data match
- TPA notification

**Platform requirements:**
- Accept death notification and update participant record: status = Deceased, date of death recorded
- Suspend all participant-initiated transactions (loan requests, investment changes, new distributions) pending beneficiary determination
- Retain account in active status for processing; do not close the account until all beneficiary distributions are complete

---

## 2. Beneficiary Designation Lookup and Validation

Upon death, the platform retrieves the most recent valid beneficiary designation on file.

**Validation steps:**
1. Retrieve the most recent beneficiary designation record
2. Verify the designation was executed after any prior QDRO that may have changed beneficiary rights
3. Verify spousal consent (if applicable — see Section 3)
4. If no valid designation exists, apply the plan's default beneficiary rules

**Default beneficiary hierarchy (if no valid designation):**
- Typically: surviving spouse → surviving children (per stirpes) → participant's estate
- Default rules are defined in the plan document and are plan-configurable

**Platform requirements:**
- Retrieve and display the effective beneficiary designation
- Flag any missing or incomplete designations
- Apply plan document default rules if no designation exists
- Request beneficiary information and documentation from surviving beneficiary or estate representative

---

## 3. Spousal Consent Requirements

[COMPLIANCE-SENSITIVE]

If a married participant has designated a **non-spouse primary beneficiary**, the spouse must have provided valid spousal consent for the designation to be effective. ERISA requires:
- Written consent from the spouse
- Consent acknowledges the specific non-spouse beneficiary designated
- Consent is witnessed by a plan representative or a notary public

**Platform requirements:**
- Track marital status at the time of beneficiary designation
- Flag beneficiary designations where a non-spouse is designated as primary beneficiary but no spousal consent is recorded
- If spousal consent is missing and the participant was married at death, the designation may be invalid and the spouse may be the default beneficiary
- [RECOMMEND LEGAL/COMPLIANCE REVIEW] — Spousal consent validity disputes require legal review

---

## 4. QDRO Interaction with Beneficiary Processing

A valid Qualified Domestic Relations Order (QDRO) may have assigned a portion of the participant's benefit to an alternate payee (former spouse, child, dependent). The QDRO takes precedence over the participant's beneficiary designation for the portion assigned to the alternate payee.

**Platform requirements:**
- Review active QDROs before finalizing beneficiary distributions
- Allocate the QDRO-assigned portion to the alternate payee before applying the participant's beneficiary designation to the remaining balance
- If the alternate payee predeceased the participant, apply the QDRO's fallback provisions (or refer to legal review)

[RECOMMEND LEGAL/COMPLIANCE REVIEW]

---

## 5. Beneficiary Classification for RMD Purposes

The distribution options and timing rules for beneficiaries depend on their classification. See Skill 19 (RMD) for detailed beneficiary RMD rules.

**Classification categories:**

| Type | Who | Distribution Rules |
|---|---|---|
| Eligible Designated Beneficiary (EDB) | Surviving spouse; minor child (until majority); disabled; chronically ill; individual ≤10 years younger | May use own life expectancy; life expectancy stretch distributions |
| Designated Beneficiary | Any named individual not qualifying as EDB | 10-year rule — full distribution by December 31 of 10th year after participant's death |
| Non-Designated Beneficiary | Estates, charities, non-qualifying trusts | 5-year rule (if participant died before RBD) or participant's remaining life expectancy (if after RBD) |

**Platform requirements:**
- Determine beneficiary classification based on relationship and applicable law at the time of death
- Apply the correct distribution rule set for each beneficiary
- Track distribution deadlines (10-year or 5-year rule) per beneficiary

[COMPLIANCE-SENSITIVE]

---

## 6. Beneficiary Distribution Options

Distribution options available to beneficiaries depend on beneficiary type, plan terms, and applicable law:

| Beneficiary Type | Available Options |
|---|---|
| Surviving Spouse (EDB) | Rollover to own IRA; rollover to inherited IRA; life expectancy stretch; lump sum; keep in plan (if plan permits) |
| Other EDB | Rollover to inherited IRA; life expectancy stretch; lump sum |
| Designated Beneficiary (non-EDB) | Rollover to inherited IRA (subject to 10-year rule); lump sum; installments within 10-year window |
| Non-Designated Beneficiary | Lump sum; installments within 5-year window (or participant's remaining life expectancy) |

**Surviving spouse unique options:**
- The surviving spouse may roll the deceased participant's account into their own IRA or qualified plan, treating the funds as if they were always the spouse's own retirement savings
- This defers the surviving spouse's own RMD obligation rather than applying the beneficiary inherited IRA rules
- The surviving spouse may also delay RMDs beyond the participant's RBD if the participant had not yet reached their RBD

**Platform requirements:**
- Present eligible distribution options based on the beneficiary's classification and the plan's available distribution forms
- Create a separate account/sub-account for the beneficiary if the beneficiary retains funds in the plan
- Process beneficiary elections for direct rollover (to inherited IRA or own IRA for spouse) or direct distribution
- Apply mandatory 20% withholding for ERDs not directly rolled over
- Generate 402(f) Special Tax Notice for eligible rollover distributions to beneficiaries

---

## 7. QDRO — Qualified Domestic Relations Order

A QDRO is a domestic relations order issued by a state court that creates or recognizes the right of an alternate payee (current or former spouse, child, or other dependent) to receive all or a portion of a participant's plan benefits.

**ERISA Requirements:**
- Every plan must establish and maintain **written QDRO determination procedures**
- The written procedures must be provided free of charge to participants and alternate payees upon request
- The plan must promptly notify the participant and alternate payee upon receipt of a domestic relations order (DRO) and of the plan's procedures for determining qualified status

**QDRO Determination Workflow:**
1. Plan receives DRO
2. Platform logs receipt of DRO; notifies participant and alternate payee
3. Plan administrator (TPA or plan sponsor) reviews the DRO against the written procedures
4. Plan administrator determines whether the DRO meets the qualification requirements
5. If qualified: alternate payee account is created; benefits are segregated per the QDRO terms
6. If not qualified: plan administrator notifies the parties of the deficiency and the 18-month segregation period expires

**Platform requirements:**
- Log DRO receipt with date and acknowledgment
- Segregate the alternate payee's share during the determination period (up to 18 months)
- Create alternate payee account upon QDRO qualification
- Process distributions to alternate payee per the QDRO terms
- [RECOMMEND LEGAL/COMPLIANCE REVIEW] for all QDRO determination and processing requirements

[COMPLIANCE-SENSITIVE]

---

## 8. Agent Rules

- **[RECOMMEND LEGAL/COMPLIANCE REVIEW]** — All QDRO processing requirements and beneficiary RMD rules for complex scenarios (trusts as beneficiaries, non-qualified trusts, estates).
- **[COMPLIANCE-SENSITIVE]** — Spousal consent validation must occur before processing any distribution to a non-spouse primary beneficiary. A missing or invalid spousal consent may invalidate the designation.
- **[COMPLIANCE-SENSITIVE]** — Beneficiary classification determines distribution rules. Misclassifying a beneficiary creates incorrect RMD distribution timelines and potential IRS penalties.
- Death processing timelines are defined by the plan document and applicable law — coordinate with TPA and legal counsel for complex estates.
- Sensitive workflows (domestic abuse, death) must be designed with participant and beneficiary privacy protections in mind.

---

## Sources

- ERISA Sections 205, 206(d) | U.S. Department of Labor | https://www.dol.gov/agencies/ebsa | Retrieved 2026-03-06
- IRC Sections 401(a)(9), 401(a)(13), 414(p) | IRS | https://www.irs.gov/retirement-plans | Retrieved 2026-03-06
- SECURE Act of 2019 (10-Year Beneficiary Rule) | https://www.congress.gov | Retrieved 2026-03-06
- IRS RMD Final Regulations (2024) | https://www.irs.gov | [DATE-VERIFY] | Retrieved 2026-03-06
