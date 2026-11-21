# Bülent İmat — Apps, Books & Visual Stories

This repository automatically publishes the prepared bilingual portfolio to **https://bulentimat-ai.github.io/**.

## First-time setup

1. Download the prepared release from ChatGPT under its exact filename **site.zip**. Do **not** extract it.
2. Open **Settings → Pages → Build and deployment → Source** and choose **GitHub Actions**.
3. In this repository open **Add file → Upload files** and upload **site.zip** to the root of the **main** branch.
4. Commit the upload. The workflow in `.github/workflows/deploy.yml` extracts and publishes the complete website.
5. See the **Actions** tab for deployment status.

Subsequent updates: upload a replacement `site.zip` to the same location and the website will redeploy.

**Privacy:** The release contains only the authorized first 4 PDF pages of *AWOOO CHRONICLES* and first 6 PDF pages of *AWOOO — The Tale of a Husky*. Full manuscripts are not included.

Existing Gentian and İsviçre Rotam repositories are not modified.
