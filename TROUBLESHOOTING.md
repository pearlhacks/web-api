# Pearl Hacks API - Troubleshooting & Maintenance Guide

## Quick Reference - Critical Items to Monitor

**🔴 HIGHEST PRIORITY (Check Weekly)**:
1. **Memory Usage**: `flyctl vm status` - Alert if >80%, scale up if >90%
2. **Token Expiration**: Check `token.json` expiry date - Re-authorize before it expires
3. **API Health**: Test all endpoints - Ensure 200 status codes
4. **Health Check Status**: `flyctl status` - Verify health checks are passing

**🟡 HIGH PRIORITY (Check Before Pearl Hacks Event)**:
1. **Scale memory to 2GB** if expecting high traffic: `flyctl scale memory 2048`
2. **Load test** all endpoints with expected traffic volume
3. **Set up real-time monitoring** for memory and crashes

**📊 Quick Commands**:
```bash
# Check overall status (includes health checks)
flyctl status

# Check memory usage
flyctl vm status

# Check token expiration
python -c "import json; print(json.load(open('token.json'))['expiry'])"

# Test health endpoint
curl https://google-sheets-api-pearl-hacks.fly.dev/health

# Monitor logs
flyctl logs --app google-sheets-api-pearl-hacks

# Emergency restart
flyctl apps restart google-sheets-api-pearl-hacks

# Scale memory
flyctl scale memory 2048
```

---

## Issue: Google Sheets API 403 Permission Error

**Date**: January 21, 2026
**Severity**: Critical - API completely non-functional
**Affected Endpoints**: All `/sheet/*` endpoints (faqs, schedules, resources, sponsors, directors, prizes)

---

## Problem Description

### Error Message
```
googleapiclient.errors.HttpError: <HttpError 403 when requesting
https://sheets.googleapis.com/v4/spreadsheets/16YJSaBwjpGRq81ryZ-Z284HkgKwYvg2MHjkBpD0IaJk/values/faq%21A1%3AX99?alt=json
returned "The caller does not have permission".
Details: "The caller does not have permission">
```

### Symptoms
- API returns 500 Internal Server Error
- All Google Sheets endpoints fail
- Error logs show 403 permission denied from Google Sheets API

---

## Root Cause

1. **Expired OAuth Token**: The `token.json` file contained credentials that expired on November 7, 2024
2. **Wrong Authentication Type**: Using OAuth 2.0 with `InstalledAppFlow.run_local_server()` which requires browser interaction
3. **Production Environment Issue**: Docker containers on Fly.io cannot open a browser to re-authorize when tokens expire
4. **Previous Team Member's Credentials**: The original token was authorized with a former team member's Google account who no longer has access to the project

---

## Solution Applied

### Immediate Fix (Temporary)

1. **Created Python virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Updated OAuth port** (to avoid port conflicts):
   - File: `apis/sheets.py`
   - Line 51: Changed from `port=5000` to `port=8080`

3. **Deleted expired token**:
   ```bash
   rm token.json
   ```

4. **Re-authorized with current team member's Google account**:
   ```bash
   python -c "from apis.sheets import get_sheets_service; get_sheets_service()"
   ```
   - This opened a browser for OAuth authorization
   - Generated new `token.json` with fresh credentials

5. **Verified locally**:
   ```bash
   uvicorn main:app --reload
   curl http://localhost:8000/sheet/faqs
   ```

6. **Deployed to Fly.io**:
   ```bash
   flyctl deploy
   ```

### Prerequisites for This Solution
- Google Sheet (ID: `16YJSaBwjpGRq81ryZ-Z284HkgKwYvg2MHjkBpD0IaJk`) must be shared with the authorizing Google account
- The authorizing person must have at least "Viewer" permission on the spreadsheet

---

## Potential Issues & Regular Maintenance

### 1. Token Expiration (HIGH PRIORITY)

**Issue**: OAuth tokens expire periodically (typically every few weeks to months)

**Symptoms**:
- Same 403 permission error will recur
- API stops working without warning

**Prevention**:
```bash
# Check token expiration date
python -c "import json; print(json.load(open('token.json'))['expiry'])"
```

**Fix**: Follow the re-authorization steps above

**Frequency**: Check every 2-4 weeks

---

### 2. Google Cloud Project Credentials

**Issue**: The `credentials.json` file could be deleted, rotated, or the OAuth client could be disabled in Google Cloud Console

**Symptoms**:
- Cannot re-authorize even after deleting `token.json`
- OAuth flow fails

**Prevention**:
- Keep a backup of `credentials.json` in a secure location
- Document who has access to the Google Cloud project `pearlhacks-master`

**Check**: Monthly or when team members change

---

### 3. Spreadsheet Access Permissions

**Issue**: The Google account that authorized `token.json` loses access to the spreadsheet

**Symptoms**:
- 403 error even with valid token
- Specific sheets return "No data found"

**Prevention**:
- Ensure the authorizing Google account maintains "Viewer" or higher permission
- Document the authorizing account email

**Check**: When team members change or access is updated

---

### 4. Port Conflicts During Re-authorization

**Issue**: Port 8080 (or configured port) is already in use when running local re-authorization

**Symptoms**:
```
OSError: [Errno 48] Address already in use
```

**Fix**:
```bash
# Check what's using the port
lsof -ti:8080

# Kill the process if needed
kill -9 $(lsof -ti:8080)

# Or change port in apis/sheets.py line 51
```

---

### 5. Cache Issues

**Issue**: Stale data served from cache even after Google Sheet is updated

**Symptoms**:
- API returns old data
- Changes to spreadsheet not reflected

**Fix**:
```bash
# Manually refresh cache via API
curl -X POST "https://google-sheets-api-pearl-hacks.fly.dev/sheet/refresh"

# Or refresh specific cache
curl -X POST "https://google-sheets-api-pearl-hacks.fly.dev/sheet/refresh?cache_type=faqs"
```

**Note**: Cache automatically expires after 5 minutes (configurable via `CACHE_TTL_SECONDS` env var)

---

### 6. Memory Limit Issues (CRITICAL)

**Issue**: Application crashes due to exceeding Fly.io memory limits

**Date Occurred**: January 2026 (resolved by upgrading to 1GB RAM)

**Symptoms**:
- API becomes unresponsive
- Fly.io sends email alert: "Machine crashed - out of memory"
- Application restarts automatically but crashes again
- 502 Bad Gateway errors
- Logs show: "Out of memory: Killed process"

**Root Causes**:
1. **Cache Growth**: In-memory cache (`_cache` dict in `apis/sheets.py`) storing data for 6 different endpoints
2. **Google API Client Libraries**: Memory overhead from `google-api-python-client` and dependencies
3. **Concurrent Requests**: Multiple simultaneous requests loading data into memory
4. **Python Memory Management**: Python's garbage collection may not release memory immediately

**Current Configuration**:
- Memory: 1GB RAM (upgraded from default 256MB)
- Location: `fly.toml` file

**Monitor Memory Usage**:
```bash
# Check current memory usage on Fly.io
flyctl status

# View detailed metrics
flyctl vm status

# Check real-time logs for memory issues
flyctl logs --app google-sheets-api-pearl-hacks

# SSH into container to check memory
flyctl ssh console
free -m
ps aux --sort=-%mem | head -10
```

**Prevention & Optimization**:

1. **Monitor Memory Trends**:
   ```bash
   # Check Fly.io dashboard for memory graphs
   # https://fly.io/dashboard
   ```

2. **Optimize Cache**:
   - Current cache stores data indefinitely until TTL expires
   - Consider setting max cache size limit
   - Consider using external cache (Redis) if memory issues persist

3. **Reduce Cache TTL** (if needed):
   ```bash
   # In .env or Fly.io secrets
   CACHE_TTL_SECONDS=180  # Reduce from 300 to 180 seconds
   ```

4. **Monitor Peak Usage Times**:
   - Memory usage likely spikes during Pearl Hacks event
   - Monitor before/during/after the event

**When to Scale Up Further**:

Upgrade to 2GB if you see:
- Memory usage consistently >80% (check with `flyctl vm status`)
- Frequent out-of-memory crashes
- High traffic during Pearl Hacks event (100+ concurrent users)

**Scale Up Command**:
```bash
# Check current configuration
flyctl scale show

# Upgrade to 2GB
flyctl scale memory 2048

# Or edit fly.toml and set:
# [vm]
#   memory = '2048mb'
# Then: flyctl deploy
```

**Cost Implications**:
- 256MB: ~$1.94/month
- 512MB: ~$3.88/month
- 1GB: ~$7.76/month
- 2GB: ~$15.52/month

**Emergency Response**:
If app crashes due to memory:
1. Check logs: `flyctl logs --app google-sheets-api-pearl-hacks`
2. Restart app: `flyctl apps restart google-sheets-api-pearl-hacks`
3. Clear cache: `curl -X POST "https://google-sheets-api-pearl-hacks.fly.dev/sheet/refresh"`
4. If persistent, scale up memory immediately

---

### 7. Environment Variables

**Issue**: Missing or incorrect environment variables

**Required Variables**:
```bash
SHEET_ID=16YJSaBwjpGRq81ryZ-Z284HkgKwYvg2MHjkBpD0IaJk
CACHE_TTL_SECONDS=300  # Optional, defaults to 300 (5 minutes)
```

**Check**: Verify in `.env` file locally and Fly.io secrets in production
```bash
flyctl secrets list
```

---

### 8. Port Configuration Issues

**Issue**: Fly Doctor warns "App is not listening to the expected port" or shows 502 Bad Gateway errors

**Symptoms**:
- Fly Doctor warning: "App is not listening on 0.0.0.0 at port specified by fly.toml"
- 502 Bad Gateway errors when accessing API
- App appears to start but isn't accessible

**Common Causes**:
1. **Stale Fly Doctor cache**: Warning persists after fixing the issue
2. **App listening on wrong port**: Mismatch between fly.toml and application code
3. **App binding to localhost**: Should bind to 0.0.0.0, not 127.0.0.1
4. **Port conflict**: Another process using the port

**Current Configuration** (CORRECT):
```toml
# fly.toml
[http_service]
  internal_port = 8000  # Fly.io expects app on port 8000
```

```dockerfile
# Dockerfile (line 16)
CMD ["/app/.venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```python
# main.py (line 20) - Only used for local development
if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

**Verification Steps**:

1. **Check if app is running correctly**:
   ```bash
   flyctl logs --app google-sheets-api-pearl-hacks
   # Look for: "Uvicorn running on http://0.0.0.0:8000"
   ```

2. **Test the API endpoint**:
   ```bash
   curl https://google-sheets-api-pearl-hacks.fly.dev/sheet/faqs
   # Should return JSON, not 502
   ```

3. **Check Fly.io status**:
   ```bash
   flyctl status
   # Should show app as "running" with health checks passing
   ```

4. **SSH into container to verify**:
   ```bash
   flyctl ssh console
   netstat -tuln | grep 8000
   # Should show: "0.0.0.0:8000" (not "127.0.0.1:8000")
   ```

**Important: OAuth Port vs App Port**:
- **OAuth port 8080** (apis/sheets.py:51): Only used during LOCAL re-authorization, not in production
- **App port 8000**: The actual FastAPI application port in production
- These are DIFFERENT ports for DIFFERENT purposes!

**Fix for Port Mismatch**:

If ports don't match, update all three locations:

1. **fly.toml**:
   ```toml
   [http_service]
     internal_port = 8000
   ```

2. **Dockerfile**:
   ```dockerfile
   CMD ["/app/.venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

3. **Deploy**:
   ```bash
   flyctl deploy
   ```

**Stale Fly Doctor Warning**:

If API is working but Fly Doctor still shows warnings:
- Fly Doctor cache may take 5-10 minutes to update
- Force a check: `flyctl doctor` (wait a few minutes, then run again)
- If working correctly, ignore the stale warning

**Prevention**:
- Always use `0.0.0.0` as host (never `localhost` or `127.0.0.1`)
- Keep port consistent across fly.toml and Dockerfile
- Test endpoints after every deployment

---

### 9. Health Check Failures / Proxy Connection Errors

**Issue**: Fly.io proxy cannot connect to the application, causing deployment failures or app unavailability

**Date Resolved**: January 21, 2026

**Symptoms**:
- Logs show: `INFO: Uvicorn running on http://0.0.0.0:8000` (app starts successfully)
- Followed by: `error.message="failed to connect to machine: gave up after 15 attempts"`
- Proxy logs: `waiting for machine to be reachable on 0.0.0.0:8000`
- App appears to start but becomes unreachable
- Deployment hangs or fails health checks

**Example Error**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
waiting for machine to be reachable on 0.0.0.0:8000 (waited 5.324464312s so far)
error.message="failed to connect to machine: gave up after 15 attempts (in 8.327400313s)"
```

**Root Cause**:
- Fly.io's proxy performs health checks to verify app is ready
- Without proper health check configuration, proxy times out waiting for response
- Default timeouts may be too short for application startup

**Solution Applied**:

**Option 1: Add Health Check Endpoint (RECOMMENDED)**

1. **Add health check endpoint to `main.py`**:
   ```python
   # main.py - Add after app.include_router(sheet_router)

   @app.get("/health")
   def health_check():
       return {"status": "healthy"}
   ```

2. **Configure health checks in `fly.toml`**:
   ```toml
   [http_service]
     internal_port = 8000
     force_https = true
     auto_stop_machines = 'stop'
     auto_start_machines = true
     min_machines_running = 0
     processes = ['app']

     [[http_service.checks]]
       interval = "10s"
       timeout = "2s"
       grace_period = "5s"
       method = "GET"
       path = "/health"
   ```

3. **Deploy**:
   ```bash
   flyctl deploy
   ```

**Option 2: Adjust Health Check Timing**

If app takes longer to start (due to Google Sheets API initialization), increase grace period:

```toml
[[http_service.checks]]
  interval = "15s"
  timeout = "5s"
  grace_period = "30s"  # Give app more time to start
  method = "GET"
  path = "/health"
```

**Verification Steps**:

1. **Watch deployment logs**:
   ```bash
   flyctl logs
   ```

   Look for:
   - `✓ Application startup complete`
   - `✓ Health check passed`
   - NO proxy connection errors

2. **Test health endpoint**:
   ```bash
   curl https://google-sheets-api-pearl-hacks.fly.dev/health
   # Should return: {"status":"healthy"}
   ```

3. **Check app status**:
   ```bash
   flyctl status
   # Should show "running" with all health checks passing
   ```

**Advanced Health Check (Optional)**:

For more robust health checks that verify Google Sheets connectivity:

```python
# main.py
@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": time.time()}

@app.get("/health/ready")
def readiness_check():
    """Check if app can connect to Google Sheets"""
    try:
        # Quick check - just verify credentials exist
        if not os.path.exists('token.json'):
            return {"status": "not_ready", "reason": "token.json missing"}
        return {"status": "ready"}
    except Exception as e:
        return {"status": "not_ready", "reason": str(e)}
```

**Prevention**:
- Always include a `/health` endpoint in production APIs
- Set appropriate grace periods (30s+ for apps with external dependencies)
- Test health checks locally before deploying:
  ```bash
  uvicorn main:app --reload
  curl http://localhost:8000/health
  ```

**Related Issues**:
- If health checks pass but app still unreachable → Check port configuration (Section 8)
- If health checks intermittently fail → Check memory usage (Section 6)

---

### 10. Deployment Issues

**Issue**: `token.json` not included in Docker image

**Current Status**: `token.json` is likely in the Docker image since it's not in `.gitignore`

**Check**:
```bash
# Verify token.json exists in deployed container
flyctl ssh console
ls -la /app/token.json
```

---

## Long-Term Solution (RECOMMENDED)

### Switch to Service Account Authentication

**Why**: Service accounts don't expire and work perfectly in server environments

**Benefits**:
- No token expiration
- No browser interaction required
- Production-ready
- No re-authorization needed

**Implementation Steps**:

1. **Create Service Account** in Google Cloud Console:
   - Go to https://console.cloud.google.com
   - Select project `pearlhacks-master`
   - Navigate to "IAM & Admin" → "Service Accounts"
   - Create new service account
   - Download JSON key file

2. **Share Spreadsheet** with service account email (found in JSON file)

3. **Update `apis/sheets.py`**:
   ```python
   from google.oauth2 import service_account

   def get_sheets_service():
       creds = service_account.Credentials.from_service_account_file(
           'service-account.json',
           scopes=SCOPES
       )
       service = build('sheets', 'v4', credentials=creds)
       return service
   ```

4. **Remove OAuth dependencies** (token.json, credentials.json)

5. **Add service-account.json to .gitignore** and manage as secret

---

## Regular Maintenance Checklist

### Weekly
- [ ] Verify API endpoints are responding (automated monitoring recommended)
- [ ] **Check health check status**: `flyctl status` (ensure all checks passing)
- [ ] Test health endpoint: `curl https://google-sheets-api-pearl-hacks.fly.dev/health`
- [ ] Check Fly.io logs for any Google API errors: `flyctl logs`
- [ ] **Monitor memory usage**: `flyctl vm status` (alert if >80%)
- [ ] Check for any memory-related crashes in Fly.io dashboard

### Bi-Weekly
- [ ] Check token expiration date
- [ ] Test all 6 endpoints (/sheet/faqs, /schedules, /resources, /sponsors, /directors, /prizes)
- [ ] Review memory trends over the past 2 weeks

### Monthly
- [ ] Review Google Cloud Console for any warnings or quota issues
- [ ] Verify spreadsheet access permissions
- [ ] Check cache performance and TTL settings
- [ ] **Review memory usage patterns** and consider optimization if consistently >70%

### When Team Members Change
- [ ] Update spreadsheet sharing permissions
- [ ] Document who has access to Google Cloud project
- [ ] If the authorizing person leaves, re-authorize with new team member

### Before Major Events (e.g., Pearl Hacks)
- [ ] Force re-authorization to ensure fresh token
- [ ] Load test endpoints with expected traffic volume
- [ ] Verify all sheet tabs are accessible
- [ ] **Check current memory usage baseline**: `flyctl vm status`
- [ ] **Consider temporarily scaling to 2GB** if expecting high traffic
- [ ] Monitor memory during event and scale if needed
- [ ] Set up real-time alerts for memory/crashes
- [ ] Have rollback plan ready

---

## Monitoring Recommendations

### Set up automated monitoring for:

1. **Health Check Monitoring (CRITICAL)**:
   ```bash
   # Test health endpoint
   curl https://google-sheets-api-pearl-hacks.fly.dev/health
   # Should return: {"status":"healthy"}

   # Check Fly.io health status
   flyctl status
   # All checks should show "passing"
   ```
   Alert if: Health endpoint returns error or `flyctl status` shows failing checks

2. **Endpoint Functionality Checks**:
   ```bash
   curl https://google-sheets-api-pearl-hacks.fly.dev/sheet/faqs
   ```
   Alert if: Status code != 200 or invalid JSON

3. **Token Expiration Alerts**:
   Check `token.json` expiry date weekly and alert 1 week before expiration

4. **Google Sheets API Quota**:
   Monitor in Google Cloud Console
   Default: 100 requests per 100 seconds per user

5. **Memory Usage Monitoring (CRITICAL)**:
   ```bash
   # Check memory percentage
   flyctl vm status

   # Set up alerts for:
   # - Memory usage >80% (warning)
   # - Memory usage >90% (critical)
   # - OOM (Out of Memory) crashes
   ```

   **Recommended Tools**:
   - Fly.io Dashboard: https://fly.io/dashboard
   - Set up email alerts in Fly.io for memory warnings
   - Consider using external monitoring (UptimeRobot, Pingdom, DataDog)

6. **Fly.io Metrics**:
   - Response times
   - Error rates
   - CPU usage
   - Request throughput

---

## Emergency Contacts

**When API Goes Down**:

1. **First, check status**: `flyctl status`
   - If health checks failing → See step 6 below

2. Check Fly.io logs: `flyctl logs`

3. Look for 403 errors → Token expiration (follow re-authorization steps in Section 1)

4. Look for 404 errors → Spreadsheet ID changed or deleted

5. Look for 429 errors → Rate limit exceeded (add caching or request throttling)

6. Look for "Out of memory" or "Killed" → Memory limit exceeded (Section 6)
   - Immediate fix: `flyctl apps restart google-sheets-api-pearl-hacks`
   - Short-term: Clear cache via API
   - Long-term: Scale up memory: `flyctl scale memory 2048`

7. Look for "failed to connect to machine" or "gave up after 15 attempts" → Health check failure (Section 9)
   - Check if `/health` endpoint exists in main.py
   - Verify health check configuration in fly.toml
   - Increase grace_period if app takes long to start
   - Redeploy: `flyctl deploy`

**Key Files to Backup**:
- `credentials.json` (OAuth client credentials)
- `token.json` (generated, but keep backup)
- `.env` (environment variables)
- Service account JSON (if implementing long-term solution)

---

## Additional Resources

- Google Sheets API Documentation: https://developers.google.com/sheets/api
- OAuth 2.0 Flow: https://developers.google.com/identity/protocols/oauth2
- Service Account Setup: https://developers.google.com/identity/protocols/oauth2/service-account
- Fly.io Secrets Management: https://fly.io/docs/reference/secrets/
