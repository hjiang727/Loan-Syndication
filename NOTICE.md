# CONFIDENTIAL — Internal CTBC use only

**Read this before sharing, hosting, or pushing anywhere.**

## Confidentiality
This project contains confidential market analysis and internal CTBC positioning. It is for internal CTBC use only and **must not be shared outside CTBC** or published to any public location.

## Third-party source material
The underlying weekly readings are from **IFR / LSEG LPC**, a licensed subscription service. The raw reading PDFs are deliberately **excluded from version control** (see `.gitignore`) and must not be redistributed. The summaries here rely on that licensed source plus public reporting, and are for internal use.

## Hosting rules (important)
A shareable link must enforce **CTBC identity** (single sign-on / corporate directory) — not just be an unlisted URL.

- **A private GitHub repo does NOT make a published page private.** On Free/Pro accounts, GitHub Pages is public to anyone with the link.
- **Approved routes:** CTBC intranet / SharePoint (already login-gated), or — if available — GitHub **Enterprise Cloud private Pages** behind CTBC SSO.
- **Not permitted:** public GitHub Pages, personal hosting accounts, or any external host without CTBC IT / compliance sign-off (even a *private* repo stores the data on a third party).

## Before you publish
Get sign-off from your manager / CTBC IT / compliance, and host via a CTBC-controlled, access-restricted system. When in doubt, keep it **local** (this repo on your machine is fine).

## Git remotes
This is intended as a **local** repository. Do **not** run `git remote add` / `git push` to a personal or public GitHub. Any remote must be a CTBC-owned, private/internal repository approved for this data.
