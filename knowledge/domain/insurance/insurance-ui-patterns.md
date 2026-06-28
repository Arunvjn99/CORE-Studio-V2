# Insurance UI Patterns

## 1. Core Insurance UI Principles

### Clarity Over Complexity
- Insurance is inherently complex — UI must translate policy language into plain English
- Flesch-Kincaid reading ease score ≥ 60 for all customer-facing policy descriptions
- Critical exclusions must be as visible as the benefits — not buried in fine print
- Coverage limits shown in dollar amounts AND plain descriptions

### Regulatory Compliance
- FCA (UK): product information must be clear, fair, and not misleading
- State DOI (US): rate filing, form filing requirements vary by state
- ACA (Health insurance): must display Essential Health Benefits coverage
- GDPR/CCPA: explain how health/vehicle/life data is used for underwriting

## 2. Quote & Comparison Flow

### Property & Casualty (Home/Auto) Quote
```
Step 1: Risk information
  - Auto: year, make, model, trim, VIN (auto-populate remaining fields)
  - Home: address (auto-populate square footage, year built from property records)
  - Drivers/occupants: names, dates of birth, driving history

Step 2: Coverage selection
  - Coverage levels displayed as cards: Basic / Standard / Comprehensive
  - Each card: premium, deductible, key coverages included, exclusions summary
  - Custom configuration: allow adjusting each coverage type with real-time premium update

Step 3: Discount identification
  - Auto-surface applicable discounts: multi-policy, good driver, home owner, paperless
  - Show amount saved per discount
  - Prompt for additional info to unlock more discounts

Step 4: Comparison summary
  - Side-by-side of 3 coverage options with price and key features
  - "Most popular" badge for middle option
  - Detailed coverage modal on click

Step 5: Checkout
  - Full premium disclosure: base premium + taxes + fees = total
  - Payment options: monthly (with finance charge) vs. annual (show savings)
  - Binding confirmation with coverage effective date
```

### Coverage Level Cards Design
- Price is secondary to coverage — lead with what's protected, then price
- Use simple icons for each coverage type
- Colour coding: grey (basic) → blue (standard) → gold (comprehensive)
- Toggle view: "What's covered" / "What's NOT covered" — show both with equal prominence

## 3. Policy Dashboard

### Policy Overview
- Policy number and status (Active / Pending / Expired / Cancelled) with clear colour coding
- Coverage period: start date → end date, with renewal date prominent
- Premium: next payment amount + due date
- Quick actions: Pay Premium, File a Claim, Update Policy, Download Documents

### Coverage Summary
- Visual coverage map: for home insurance, show dwelling/personal property/liability/medical payments
- Dollar limits for each coverage type
- Deductible amounts for each category
- Exclusions: clearly listed, not hidden

### Named Insured & Additional Interests
- Primary insured and co-insured names
- Additional insured (for business/landlord policies)
- Loss payee (lender for financed vehicles/property)
- Beneficiaries: for life insurance

## 4. Claims Management

### First Notice of Loss (FNOL)
```
Step 1: Incident type selection
  - Accident / Theft / Weather Damage / Fire / Liability / Other
  - Date and time of incident
  - Brief description

Step 2: Loss details
  - Location of incident
  - Other parties involved (auto accident)
  - Police report number (if applicable)
  - Estimated damage amount

Step 3: Documentation upload
  - Photos of damage (multiple, clear guidance on what to photograph)
  - Police report PDF
  - Receipts for damaged items (renters/home)
  - Medical records (liability/health)
  - File types: JPEG, PNG, PDF; max 10MB per file, 50MB total

Step 4: Claim submission
  - Claim number assigned immediately
  - Adjuster assignment notification
  - Next steps timeline

Step 5: Claim tracking
```

### Claim Status Tracking
- Status timeline: Filed → Under Review → Inspection Scheduled → Assessment Complete → Payment Issued
- Current step highlighted; estimated completion date
- Assigned adjuster: name, phone, email, office hours
- Document requests: clear list of outstanding documents with upload button
- Settlement offer: amount, breakdown, accept/dispute options
- Payment status: pending/issued/received with payment method and expected date

### Claims History
- Each claim: number, date, type, status, settlement amount
- Claim status affects premium renewal — show transparency here
- Time since last claim: "Your last claim was X years ago" (affects rates)

## 5. Life Insurance UI

### Coverage Calculator
- Income replacement: typical 10–12× annual income guideline
- Outstanding debts: mortgage, loans, credit cards
- Children's education fund
- Final expenses estimate
- Existing coverage: subtract existing life coverage
- Net gap: recommended additional coverage amount

### Policy Types Comparison
Side-by-side comparison table:
| Feature | Term Life | Whole Life | Universal Life | Variable Life |
|---|---|---|---|---|
| Coverage period | Specified term | Lifetime | Lifetime | Lifetime |
| Cash value | No | Yes | Yes | Yes |
| Premium | Fixed | Fixed | Flexible | Flexible |
| Investment component | No | No | No | Yes |
| Best for | Income replacement | Estate planning | Flexibility | Investment + protection |

### Beneficiary Management
- Primary + contingent beneficiaries with percentage allocation
- Must sum to 100% (validate in real-time)
- Options: individuals (name/DOB/relationship/SSN) or entities (charity/trust)
- Change beneficiary: require e-signature; some policies require spousal consent

## 6. Health Insurance UI

### Plan Comparison (ACA Marketplace Style)
- Metal tier: Bronze / Silver / Gold / Platinum — explain each clearly
- Key numbers: monthly premium, deductible, out-of-pocket max, copay, coinsurance
- Essential Health Benefits: coverage list with checkmarks
- Provider network: search for specific doctors/hospitals before enrolling
- Prescription drug coverage: formulary search

### Explanation of Benefits (EOB)
- What the service cost (billed amount)
- What the plan paid (plan payment)
- What your discount is (negotiated rate savings)
- What you owe (your responsibility)
- Running total: deductible met, out-of-pocket progress bar for the year

### Pre-authorisation UI
- Search by procedure code or plain-language description
- Status: Required / Not Required / Conditional
- How to request: online form link, phone number, fax number
- Typical response time for urgent vs. routine requests
- Denial appeal: clear steps and timeline

## 7. Renewal & Mid-Term Changes

### Renewal UI
- Premium change: clearly show old vs. new premium with change amount and %
- Reason for change: transparent explanation (claims history, risk factors, market changes)
- Coverage change recommendations: proactive suggestions based on life events
- Renewal deadline: countdown timer for final decision date

### Mid-Term Endorsements
- Changes that can be made: add/remove drivers, update address, increase coverage
- Pro-rata refund/charge: show exactly how much is owed or refunded for mid-term changes
- Effective date: immediate, next payment, or custom date

## 8. Insurance Document Management

- Declarations page (one-page policy summary): always downloadable as PDF
- Full policy wording: searchable, with definitions section
- Proof of insurance / Certificate of Insurance: generate on demand (auto/home)
- Premium receipts: downloadable for business/tax purposes
- Regulatory notices: required by law to be delivered; confirmation of receipt logged

## 9. Accessibility Requirements for Insurance

- Policy documents must meet PDF accessibility standards (tagged PDFs, reading order)
- Claims photos: image upload must work with camera app or file picker (assistive technology compatible)
- Phone-based claims option: for users who cannot complete digital FNOL
- Large print and Braille: mention availability for physical documents
- Language access: translate UI for common languages in service area
- Coverage explanation videos: must be captioned
