# app-template

Template for new web apps on the platform `degiwo/server-infra`.

## New app

1. **Repo:** create a new repo from this template. The repo name is the app name (lowercase, becomes the subdomain).
2. **Placeholders:** replace `<owner>` and `<app>` in `compose.yml`.
3. **Secrets:** (repo → Settings → Secrets and variables → Actions):
   | Secret               | Value                                       |
   | -------------------- | ------------------------------------------- |
   | `DEPLOY_HOST`        | Server IP                                   |
   | `DEPLOY_SSH_KEY`     | Private key matching `DEPLOY_SSH_PUBKEY`    |
   | `DEPLOY_KNOWN_HOSTS` | Output of `ssh-keyscan -t ed25519 <server>` |
4. **Server** (as `deploy`):
   ```sh
   mkdir /srv/apps/<app> /srv/backups/dumps/<app> && cd /srv/apps/<app>
   # create .env from .env.example and fill in
   chmod 600 .env
   ```
5. **Deploy:** push to `main`.

**Check:** the workflow is green; `https://<app>.apps.<domain>` asks for the login and shows the app.

## Conventions

- **No ports:** the app is only reachable though Caddy.
- **Login:** the label `caddy.import=authelia` protects the app. The app gets the user as headers.
- **Data:** everything persistent goes to `./data` (bind mount), DB dumps to `srv/backups/dumps/<app>/`.
- **Secrets:** app secrets only in `.env` on the server, never in the repo.
- **Rollback:** `git revert` and push.
