# Notice: status, sources and licence

## Status

This is a personal archive of a learning project from my summer 2026 internship at CTBC Bank. I no longer work there.

The repository was first written as an internal, confidential project. It is public now with the agreement of my former supervisor at the bank.

It is not an official CTBC publication. Nothing here represents the views of CTBC Bank, and any opinions in the briefing are my own.

## Where the market content came from

- The weekly deal tables and commentary summarise licensed market publications that I read during the internship (IFR / LSEG LPC coverage of Asia-Pacific syndicated loans), together with public reporting.
- The original publications are not in this repository. `.gitignore` keeps them out.
- The figures were compiled for study and have not been re-checked against their sources since June 2026. Treat them as illustrative, not as a data source.

## What the MIT licence covers

**Covered:** the code. That means `src/template.html`, the build and test scripts in `tools/`, and the project configuration.

**Not covered:** the market content. These files contain third-party information that is not mine to license:

- `src/data/jun1.json`, `jun8.json`, `jun15.json`, `jun22.json` and `shared.json`
- `dist/CTBC_Loan_Market_Dashboard.html`, which has that data built in
- `CTBC_Loan_Market_Briefing.md` and `.docx`
- `CTBC_Loan_Market_Deck.pptx`

Please do not reuse or redistribute that content. To use the code, swap in your own data.

## Not advice

Nothing here is investment, legal or financial advice.

## Removal requests

If you hold rights in any material here and want it taken down, open an issue on this repository and I will remove it.
