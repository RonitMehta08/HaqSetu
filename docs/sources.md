# Source register

The catalogue is a demonstrator, not a live eligibility database. Re-open each
link before submitting and update the source snapshot/date only after a human
has verified the current page.

| Topic | Official source | Used for |
| --- | --- | --- |
| National scheme discovery | https://www.myscheme.gov.in/ | Problem framing and discovery model. |
| Digital India myScheme overview | https://www.digitalindia.gov.in/initiative/myscheme | National one-stop scheme marketplace context. |
| PM-KISAN | https://pmkisan.gov.in/ | Landholding farmer income-support screening signal. |
| PMFBY | https://pmfby.gov.in/ | Crop/season/area verification signal. |
| Ayushman Bharat PM-JAY | https://pmjay.gov.in/ | Household beneficiary-database verification signal. |
| NSAP / IGNOAPS | https://nsap.nic.in/ | Older-person pension route and state verification signal. |
| PMAY-G | https://pmayg.nic.in/ | Rural housing-deprivation/local verification signal. |
| PM SVANidhi | https://pmsvanidhi.mohua.gov.in/ | Street-vendor and ULB/lender verification signal. |
| National Scholarship Portal | https://scholarships.gov.in/ | Post-matric catalogue and course/category/deadline signal. |
| e-Shram (future expansion) | https://eshram.gov.in/ | Unorganised-worker expansion reference. |
| National Portal of India schemes | https://www.india.gov.in/my-government/schemes | Cross-check for public scheme discovery context. |

## Source-handling policy

- No source is represented as a guarantee of approval.
- The app attaches the source URL to each result and displays the catalogue's
  manual-verification warning.
- The app does not scrape or write to any portal at runtime.
- A future ingestion job should store page hash, retrieval timestamp, source
  owner, licence/terms, and human review status.
