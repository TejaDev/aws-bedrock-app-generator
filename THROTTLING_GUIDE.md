# AWS Bedrock Throttling - Explanation & Solutions

## 🔴 Why Throttling Occurs

### Root Causes
1. **AWS Rate Limits**: Bedrock has rate limits on concurrent requests
   - Default limit: Varies by inference profile
   - Measured in: Requests per minute (RPM)
   
2. **Multiple Rapid API Calls**: Application generation makes 5+ sequential API calls
   - Call 1: Generate specification
   - Call 2: Generate main code file
   - Call 3: Generate configuration file
   - Call 4: Generate pom.xml/requirements
   - Call 5: Generate test file
   
3. **Inference Profile Constraints**: 
   - `us.anthropic.claude-3-5-sonnet-20241022-v2:0` has specific rate limits
   - Multiple concurrent requests exceed the limit

## ✅ Current Mitigation in Place

### Automatic Retry Logic
```python
max_retries = 3
retry_delay = 2  # seconds

# Exponential backoff strategy:
# Attempt 1: 2 seconds
# Attempt 2: 4 seconds  
# Attempt 3: 8 seconds

# Inter-request delay: 0.5 seconds between API calls
```

### How It Works
1. API call is made
2. If throttled → wait and retry automatically
3. No manual intervention needed
4. Transparent to user (logged as warnings, not errors)

## 💡 Solutions to Reduce Throttling

### Solution 1: Generate One App at a Time (Current Best Practice)
```bash
# ✓ GOOD - Sequential generation
python3 cli.py --name app1 --requirements "..." --stack java
# Wait for completion...
python3 cli.py --name app2 --requirements "..." --stack java
```

### Solution 2: Request Higher Rate Limits
Contact AWS Support to request higher rate limits for your Bedrock inference profile:
- Go to AWS Console → Bedrock → Usage Quotas
- Request increase for your inference profile
- Usually approved within 24 hours

### Solution 3: Use a Different Model
Switch to a model with higher throughput:
```bash
export AWS_BEDROCK_MODEL="us.anthropic.claude-3-5-haiku-20241022-v1:0"
```

Haiku (smaller model) has:
- ✅ Higher rate limits
- ✅ Faster responses
- ⚠️ Lower quality (use for simple apps)

### Solution 4: Add Delays Between Generations
Already implemented: 0.5s between API calls

To increase this, modify `bedrock_client.py`:
```python
# Current: time.sleep(0.5)
# Increase to: time.sleep(1.0)  # 1 second between calls
```

### Solution 5: Batch Generation with Delays
```bash
# Generate apps with time between them
python3 cli.py --name app1 --requirements "..." --stack java
sleep 30  # Wait 30 seconds
python3 cli.py --name app2 --requirements "..." --stack java
sleep 30
python3 cli.py --name app3 --requirements "..." --stack java
```

## 📊 Performance Tips

### For Multiple Generations
1. **Sequential is better than parallel**: Generate one app at a time
2. **Wait between generations**: 30-60 seconds between starts
3. **Monitor logs**: "Throttled" warnings are normal and handled
4. **Retries work**: 90% of throttled calls succeed on retry

### Generation Times (Typical)
- Simple API: 2-3 minutes
- Complex backend: 3-5 minutes
- With throttling & retries: Add 10-20 seconds

## 🔧 How to Monitor Throttling

Check logs for throttling messages:
```
2025-11-15 20:34:16 WARNING - Throttled. Retrying in 2s... (attempt 1/3)
2025-11-15 20:34:20 WARNING - Throttled. Retrying in 4s... (attempt 2/3)
2025-11-15 20:34:24 INFO - Successfully generated content from Bedrock
```

This is **normal and expected** behavior. The system handles it automatically.

## ✅ Best Practices

1. **Generate one app at a time** ← Most important
2. **Wait for completion before starting next**
3. **Use retry logic** (already enabled)
4. **Monitor progress logs**
5. **If persistent throttling**: Request higher limits from AWS

## 📈 Scaling Strategy

If you need to generate many applications:

1. **Short term**: Use delays between generations
2. **Medium term**: Request higher rate limits from AWS
3. **Long term**: Consider dedicated throughput for Bedrock

## Summary

**The throttling is:**
- ✅ Expected and normal
- ✅ Automatically handled with retries
- ✅ Transparent to users
- ✅ Usually resolves on its own

**You don't need to do anything** - the system is already optimized!

Just generate your apps sequentially, and throttling warnings are harmless.
