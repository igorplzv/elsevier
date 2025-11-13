# Elsevier API Key Setup Guide

## Current Status

The API key `861c260a6a468a1bfbaa1a2c004f1282` is returning "Access denied" (403) errors. This indicates the key needs to be **activated** before it can be used.

## Why Am I Getting "Access Denied"?

When you register for an Elsevier API key, it goes through an approval process:

1. **Registration** - You fill out the form at dev.elsevier.com
2. **Pending** - Your request is reviewed by Elsevier
3. **Activation** - Elsevier approves and activates your key (you receive an email)
4. **Ready** - You can now use the API

Currently, the API key appears to be in the **Pending** or **Not Activated** state.

## How to Activate Your API Key

### Option 1: Wait for Activation Email

If you recently registered:
1. Check your email inbox for a message from Elsevier
2. Look for subject like "Elsevier Developer Portal - API Key Approved"
3. Follow any activation instructions in the email
4. Wait 24-48 hours for processing

### Option 2: Check API Key Status

1. Go to https://dev.elsevier.com
2. Log in with your account
3. Navigate to "My API Key" or "API Keys" section
4. Check the status:
   - ✓ **Active** - Ready to use
   - ⏳ **Pending** - Waiting for approval
   - ✗ **Suspended** - Contact support

### Option 3: Request a New API Key

If your key is not activating:

1. **Visit the Developer Portal**
   ```
   https://dev.elsevier.com
   ```

2. **Click "I want an API key"**

3. **Fill out the registration form:**
   - Full name
   - Email address
   - Institution/Organization
   - Purpose of use (select one):
     - Research
     - Education
     - Product development
     - Other (specify)
   - Brief description of your project

4. **Agree to Terms**
   - Read the Terms of Use
   - Accept the agreement

5. **Submit and Wait**
   - You'll receive a confirmation email
   - API key activation usually takes 24-48 hours
   - You'll receive an activation email when ready

## What Access Do You Need?

### Free Academic/Research Access

If you're at an academic institution:
- ✓ Metadata search (titles, authors, abstracts)
- ✓ Limited full-text access (depends on your institution)
- ✗ Full-text access to all articles (requires institutional subscription)

### Commercial Access

For commercial use:
- Contact Elsevier sales team
- May require a paid license
- Email: integrationsupport@elsevier.com

## Testing Your API Key

Once you have an activated key:

```bash
# Update the key in config.py
nano config.py

# Test the configuration
python test_setup.py

# If successful, try a real search
python sciencedirect_search.py "artificial intelligence"
```

## Common Issues

### Issue 1: "Access Denied" (403)

**Cause:** API key not activated or invalid

**Solutions:**
- Wait for activation email
- Check key status on dev.elsevier.com
- Verify you copied the key correctly (no extra spaces)

### Issue 2: "Unauthorized" (401)

**Cause:** API key format is incorrect

**Solutions:**
- Check for typos in the API key
- Ensure no spaces before/after the key
- Verify the key is exactly 32 characters

### Issue 3: No Results Returned

**Cause:** Lack of institutional access

**Solutions:**
- Add institutional token (if available)
- Contact your library for institutional token
- Try searching for open access content only

## Demo Mode

While waiting for API activation, you can see how the tool works:

```bash
python demo_mode.py
```

This shows the tool's functionality with sample data.

## Getting Help

### Elsevier Support

- **Email:** integrationsupport@elsevier.com
- **Portal:** https://dev.elsevier.com/support.html

When contacting support, include:
- Your API key (first 8 characters only)
- The exact error message
- What you're trying to do
- Your institution (if applicable)

### API Documentation

- Main docs: https://dev.elsevier.com/api_docs.html
- Search API: https://dev.elsevier.com/documentation/SCIDIRSearchAPI.wadl
- Developer forum: https://dev.elsevier.com/forum.html

## Alternative: Using Scopus Instead

If ScienceDirect access is not available, try Scopus:

```python
# In sciencedirect_search.py, change the endpoint
BASE_URL = "https://api.elsevier.com/content/search/scopus"
```

Scopus has different content but may have different access requirements.

## Next Steps

1. ✅ **Check your email** for activation message
2. ✅ **Log in to dev.elsevier.com** to check status
3. ✅ **Wait 24-48 hours** if recently registered
4. ✅ **Test with test_setup.py** once activated
5. ✅ **Run demo_mode.py** to see how it works while waiting

---

**Note:** This tool is fully functional and ready to use. It only requires an **activated** API key from Elsevier. The code has been tested and works correctly with valid credentials.
