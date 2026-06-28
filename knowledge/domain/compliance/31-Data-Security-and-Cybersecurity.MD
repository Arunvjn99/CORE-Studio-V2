# Skill: Data Security and Cybersecurity
**Skill-ID:** 31-Data-Security-and-Cybersecurity
**World:** Retirement World v1.0
**Category:** Technology & System Landscape
**Last-Reviewed:** 2026-03-06

---

## Purpose

This skill defines cybersecurity requirements for the CORE platform — PII handling, encryption standards, access controls, authentication requirements, DOL cybersecurity guidance, and the SPARK Institute DSOB standards. Retirement account data is among the most sensitive and valuable personal financial data that exists. A breach can cause irreversible financial harm to participants.

---

## 1. Why Retirement Platform Cybersecurity Is High-Stakes

Retirement accounts contain:
- Social Security Numbers (SSNs)
- Dates of birth
- Home addresses
- Compensation history
- Account balances and transaction history
- Bank account information (for distributions)

This data combination enables identity theft, account takeover, and fraudulent distributions. A $500,000 retirement account drained by an attacker is effectively an irreversible loss for the participant.

---

## 2. PII Handling Requirements

**Highly sensitive PII in the retirement platform:**
- Social Security Numbers (SSNs) — highest sensitivity
- Dates of birth
- Compensation data
- Account balances and transaction history
- Beneficiary information
- Bank account information for distributions

**Access controls:**
- SSNs and other PII must be accessible only to roles that require it for their function
- Role-based access control (RBAC): each user role has a defined set of data fields it may access
- Access to SSNs must be explicitly authorized per role; bulk export of SSNs must be logged and require supervisor approval

**Encryption:**
- SSNs and other high-sensitivity PII must be encrypted **at rest** (in the database) and **in transit** (API, file transfer, email)
- Encryption standards: industry-standard encryption algorithms (AES-256 or equivalent for at rest; TLS 1.2+ for in transit)

**Display masking:**
- SSNs must be masked in all user interface displays except for explicitly authorized contexts (e.g., XX-XXXXX displayed; last 4 digits shown for verification)
- Account numbers must be masked in display
- Masking must apply to all portals: participant, plan sponsor, TPA, admin

**Audit logging of PII access:**
- Every access to SSN or full account number must be logged: who accessed it, what system, timestamp
- Bulk data exports containing PII must be logged and require approval

---

## 3. DOL Cybersecurity Guidance (2021)

In 2021, the DOL issued cybersecurity guidance applicable to retirement plan service providers and plan sponsors. [DATE-VERIFY — confirm current DOL cybersecurity guidance in effect]

**Three components of DOL 2021 guidance:**
1. **Tips for Hiring a Service Provider with Strong Cybersecurity Practices** — guidance for plan sponsors evaluating service providers
2. **Cybersecurity Program Best Practices** — guidance for service providers covering 12 best practice areas
3. **Online Security Tips for Participants** — guidance for participants protecting their accounts

**12 Best Practice Areas (DOL Cybersecurity Program Best Practices):**
1. Formal, well-documented cybersecurity program
2. Prudent annual risk assessments
3. Reliable annual third-party audits
4. Defined and assigned information security roles and responsibilities
5. Strong access control procedures
6. Asset/data management practices
7. Data privacy compliance
8. Cybersecurity training for all personnel
9. Effective business continuity, disaster recovery, and incident response programs
10. Encryption of all sensitive data
11. Strong technical controls (firewalls, endpoint protection, SIEM, vulnerability management)
12. Prompt reporting and mitigation of cybersecurity incidents

**Platform requirements:**
- The CORE platform must operate in compliance with the DOL cybersecurity best practices
- Annual third-party security audits must be performed
- Incident response plan must address retirement data breach scenarios including notification to affected participants and regulators

---

## 4. SPARK Institute Data Security Oversight Board (DSOB) Standards

The SPARK Institute's Data Security Oversight Board has published cybersecurity standards for retirement industry data handlers covering: [INDUSTRY PRACTICE — reference SPARK DSOB for current requirements]

- Access controls and identity management
- Encryption standards (at rest and in transit)
- Incident response and breach notification
- Vendor/third-party management
- Security assessment and audit requirements
- Cybersecurity training program requirements

**Platform requirements:**
- CORE platform security program should align with SPARK DSOB standards as the industry benchmark for retirement technology providers
- Third-party integrations (payroll providers, custodians, fund companies) should be evaluated against DSOB standards as part of vendor management

---

## 5. Authentication Standards

**Multi-Factor Authentication (MFA):**

MFA is the industry standard for all participant, plan sponsor, TPA, and administrator portal access. Single-factor authentication (username + password only) is insufficient given:
- High value of retirement accounts to attackers
- Prevalence of credential stuffing attacks (automated use of leaked password databases)
- DOL guidance recommending MFA

[INDUSTRY PRACTICE]

**Authentication requirements by user type:**

| Portal | Authentication Standard |
|---|---|
| Participant portal | MFA required; supports authenticator app, SMS, or email OTP |
| Plan sponsor portal | MFA required |
| TPA portal | MFA required |
| Admin/operations portal | MFA required; consider hardware security keys for privileged access |
| API integrations | OAuth 2.0 or equivalent; API keys must be rotated periodically |

**Session management:**
- Sessions must time out after a period of inactivity (plan-configurable; reasonable default ≤ 30 minutes for participant portal)
- Re-authentication required for sensitive actions (distribution initiation, beneficiary change, bank account update)

---

## 6. Sensitive Action Authorization

High-risk participant actions require additional verification beyond standard authentication:
- Distribution requests (especially to external bank accounts)
- Beneficiary designation changes
- Address changes (especially immediately before a distribution request)
- Bank account addition or change

**Platform requirements:**
- Out-of-band verification for sensitive actions (e.g., email confirmation, SMS OTP to a registered device)
- Delay period after contact information changes before a distribution can be processed (configurable cooling-off period)
- Alert participant via the prior address/email when contact information changes

---

## 7. Cybersecurity Incident Response

A cybersecurity incident involving retirement plan data requires:
1. Immediate containment and investigation
2. Notification to affected participants within required timeframes (state breach notification laws vary — do not hardcode deadlines) [DATE-VERIFY — confirm applicable breach notification requirements]
3. Notification to plan sponsors (as contractual obligation and fiduciary matter)
4. Documentation of the incident, response actions, and remediation
5. Assessment of regulatory reporting obligations (DOL, state regulators)

**Platform requirements:**
- Incident detection capabilities (anomaly detection, failed login monitoring, unusual transaction patterns)
- Incident response runbooks for retirement-specific scenarios (account takeover, fraudulent distribution)
- Participant notification workflow
- Incident audit trail

---

## 8. Vendor and Third-Party Security Management

The CORE platform integrates with multiple third parties: payroll providers, custodians, fund companies, TPA systems, and document delivery vendors. Each integration is a potential attack surface.

**Platform requirements:**
- Evaluate all third-party integrations against SPARK DSOB security standards
- Secure file transfer (SFTP with key authentication or equivalent) for file-based integrations
- API integrations must use authenticated, encrypted connections
- Third-party security assessments should be conducted periodically
- Contracts with third parties must include data security and breach notification provisions

---

## Agent Rules

- **[COMPLIANCE-SENSITIVE]** — SSN encryption at rest and in transit is non-negotiable. Plaintext SSN storage or transmission is unacceptable.
- MFA is mandatory for all user-facing portals. Any requirement that bypasses MFA for convenience must be flagged and rejected.
- Display masking of SSNs must be enforced at the application layer — not only at the UI layer. An API response that returns a full SSN to a role that should not have it is a data leak.
- Sensitive action authorization (cooling-off periods, out-of-band verification) is specifically required for distribution requests and contact information changes — these are the highest-risk participant actions.
- Security requirements must be written into every feature that handles participant PII — do not treat security as a separate workstream.

---

## Sources

- DOL Cybersecurity Guidance (2021) | https://www.dol.gov/agencies/ebsa/employers-and-advisers/plan-administration-and-compliance/cybersecurity | Retrieved 2026-03-06
- SPARK Institute DSOB Cybersecurity Standards | https://www.sparkinstitute.org | Retrieved 2026-03-06
- NIST Cybersecurity Framework | https://www.nist.gov/cyberframework | Retrieved 2026-03-06
- WCAG 2.1 Accessibility Guidelines | https://www.w3.org/WAI/standards-guidelines/wcag/ | Retrieved 2026-03-06
