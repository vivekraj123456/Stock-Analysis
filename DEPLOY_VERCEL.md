# Deploy To Vercel

This repository is configured to run the Dash app on Vercel with:

- `api/index.py` as the Python entrypoint
- `requirements.txt` for dependencies
- `vercel.json` for routing all requests to Dash

## 1. Push To GitHub

Commit and push this repo to GitHub.

## 2. Import Project In Vercel

1. Go to <https://vercel.com/new>
2. Import your GitHub repo
3. Keep the project root as the repository root (`.`)
4. Click **Deploy**

## 3. Verify

After deploy finishes, open the Vercel URL and confirm the dashboard loads.

## Notes

- The app reads CSV files from `powerbi_data/` at runtime. Keep this folder in the repo.
- Current dataset size is about 50 MB, which can increase cold start time on serverless.
- If build fails due missing package, add it to `requirements.txt` and redeploy.

## Auto-Refresh On Vercel (Recommended)

Vercel does not automatically see CSV updates from your local machine. It only serves what was in Git at deploy time.

This repo now includes:

- `.github/workflows/refresh-data.yml`
- A weekday schedule at **08:00 IST** (02:30 UTC)
- Automatic `powerbi_data/*.csv` refresh + commit + push

Because Vercel is linked to GitHub, each pushed data refresh triggers a new deployment, so production shows the latest dataset date.

If your default branch is protected, allow GitHub Actions to push (or use a PAT-based push action).
