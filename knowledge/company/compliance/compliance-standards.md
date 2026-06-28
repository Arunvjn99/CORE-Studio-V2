# Compliance Standards for UI/UX Design

## 1. Web Accessibility Compliance

### ADA (Americans with Disabilities Act)
- Web content must be accessible to people with disabilities under ADA Title III
- Courts consistently apply WCAG 2.1 AA as the technical standard for ADA compliance
- Non-compliance risk: federal lawsuits, settlements averaging $25,000–$100,000
- Required: accessible forms, keyboard navigation, screen reader support, captioned media

### Section 508 (US Federal)
- Applies to federal agencies and any organisation receiving federal funding
- References WCAG 2.0 AA as technical standard
- Requires: accessibility conformance reports (ACR/VPAT) for software products
- Design deliverable: include accessibility annotations for every component

### EN 301 549 (European Standard)
- EU equivalent of Section 508, now referenced by the European Accessibility Act (EAA)
- EAA enforcement deadline: June 2025 for private sector products and services
- Covers websites, mobile apps, self-service terminals, e-commerce, banking services

## 2. Data Privacy & GDPR

### GDPR Core Principles for UI Design
- **Lawful basis display**: clearly show why data is collected and on what legal basis
- **Consent UI**: cookie banners and consent forms must present Accept and Reject options equally prominently — dark patterns that hide Reject are illegal
- **Data minimisation**: only ask for data you actually need; justify every field in the form
- **Right to access**: provide a "Download my data" option in account settings
- **Right to erasure**: provide "Delete my account" option; confirm deletion with timeline
- **Privacy by default**: default settings must be privacy-protective; users opt IN, not opt out

### Cookie Consent Design (GDPR/PECR)
- Cookie banner must appear before non-essential cookies fire
- Granular controls: separate toggles for Analytics, Marketing, Functional cookies
- "Accept All" and "Reject All" buttons must be equally easy to find and click
- Pre-ticked boxes for non-essential cookies are illegal
- Users must be able to withdraw consent as easily as they gave it (accessible in footer)

### CCPA (California Consumer Privacy Act)
- "Do Not Sell or Share My Personal Information" link required in footer
- Privacy policy must disclose categories of data collected and purpose
- Right to opt out of data selling must be honoured within 15 business days

### COPPA (Children's Online Privacy Protection Act)
- Never collect data from users under 13 without verifiable parental consent
- Age gates must be present if any chance of under-13 users
- Avoid design patterns that encourage children to provide personal information

## 3. Financial Services Compliance

### KYC (Know Your Customer) UI Requirements
- Identity verification flows must collect: full legal name, date of birth, address, government ID
- Progress must be saveable — do not force completion in one session
- Document upload: accept JPEG, PNG, PDF; show clear guidance on photo quality
- Status communication: clear messaging on verification pending/approved/rejected states
- Data handling notice: explain how identity documents are stored and for how long

### PCI DSS (Payment Card Industry Data Security Standard)
- Never display full card numbers — mask as `•••• •••• •••• 1234`
- CVV must never be stored or re-displayed after initial entry
- Payment form must be served over HTTPS with valid TLS certificate
- Use hosted payment fields or iframes from PCI-compliant processors (Stripe, Braintree) — do not build card input from scratch
- 3D Secure (3DS): support redirect or inline challenge flow

### TILA (Truth in Lending Act) — US Lending UI
- APR must be disclosed prominently before application submission
- Loan terms (principal, interest rate, total repayment amount, payment schedule) must be clearly displayed
- Right of rescission notice for mortgage products (3-day cooling off period)
- No dark patterns that obscure total cost of credit

### MiFID II (EU Financial Instruments) — Investment UI
- Risk warnings must be prominently displayed before investment decisions
- Past performance disclaimers required near performance charts
- Complexity and risk classification (KIID) must be accessible before purchase
- Appropriateness test results must be clearly communicated

## 4. Healthcare Compliance

### HIPAA (Health Insurance Portability and Accountability Act)
- Protected Health Information (PHI) must never be displayed in notifications, email subjects, or URL parameters
- Session timeout: automatic logout after 15 minutes of inactivity (recommended)
- Audit trail: log all access to PHI with user ID, timestamp, action
- Minimum necessary rule: only display PHI fields required for the current task
- Encryption in transit and at rest required for all PHI
- Login screen: do not prefill username or hint at account existence

### FDA 21 CFR Part 11 (Electronic Records/Signatures)
- Electronic signatures must be validated, timestamped, and linked to the signer
- Audit trails must be computer-generated and tamper-evident
- System access controls: unique user IDs, no shared logins

## 5. Financial UI Dark Patterns to Avoid
These are prohibited by FTC (US) and FCA (UK) regulations:

- **Hidden fees**: total cost must be shown before checkout, not revealed only at confirmation
- **Pre-ticked add-ons**: insurance, warranties, subscriptions must be opt-in
- **Roach motel**: cancellation must be as easy as sign-up (no "call to cancel" for online sign-ups)
- **Disguised ads**: sponsored content must be clearly labelled
- **Countdown timers**: fake urgency timers that reset are deceptive
- **Confirm-shaming**: "No thanks, I don't want to save money" button labels are manipulative
- **Drip pricing**: hiding mandatory fees until the final checkout step

## 6. ePrivacy & Cookie Compliance

Required UI elements:
- Cookie banner on first visit (for EU/UK users)
- Cookie policy accessible from footer
- Consent management platform (CMP) for third-party cookie management
- Clear distinction between first-party and third-party cookies
- Session cookies vs persistent cookies must be differentiated

## 7. Insurance UI Compliance (FCA / State DOI)

- Policy terms must be in plain English; Flesch reading ease score ≥ 60
- Material terms (exclusions, waiting periods, caps) must be prominently displayed
- Quote comparison must show like-for-like coverage
- No misleading imagery suggesting coverage extends to excluded scenarios
- Claims process must be clearly explained before purchase

## 8. Compliance Checklist for UI Reviews

### Privacy
- [ ] Privacy policy link in footer
- [ ] Cookie consent implemented correctly (no pre-ticked boxes)
- [ ] Data collection minimised — only required fields
- [ ] Account deletion flow exists
- [ ] HTTPS everywhere

### Accessibility
- [ ] WCAG 2.1 AA contrast ratios met
- [ ] Keyboard navigation complete
- [ ] Screen reader labels on all interactive elements
- [ ] Focus management correct for modals/dialogs
- [ ] Error messages linked to form fields

### Financial
- [ ] APR/total cost displayed before commitment
- [ ] No hidden fees
- [ ] Card data handled via PCI-compliant processor
- [ ] Risk warnings present (investment products)
- [ ] KYC flow complete and saveable

### Healthcare
- [ ] PHI not in URLs, notifications, or email subjects
- [ ] Session timeout configured (≤ 15 minutes idle)
- [ ] Minimum necessary PHI displayed
- [ ] Audit logging in place
