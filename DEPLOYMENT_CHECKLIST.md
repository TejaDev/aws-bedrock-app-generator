# Deployment Checklist

Use this checklist before deploying the AWS Bedrock App Generator to any environment.

## Pre-Deployment Verification

### Development Machine Setup
- [ ] Python 3.9+ installed (`python3 --version`)
- [ ] Git installed and configured (`git --version`)
- [ ] AWS CLI installed (`aws --version`)
- [ ] AWS credentials configured (`aws sts get-caller-identity`)
- [ ] AWS Bedrock API accessible in your region
- [ ] Sufficient disk space (1+ GB free)

### Project Setup
- [ ] Repository cloned or downloaded
- [ ] Virtual environment created (`.venv/`)
- [ ] Dependencies installed (`pip list | grep boto3`)
- [ ] Project tested locally successfully
- [ ] Generated sample apps working correctly

### Code Quality
- [ ] No uncommitted changes (`git status`)
- [ ] Tests passing (if available)
- [ ] Code linted and formatted (`make lint`)
- [ ] No sensitive data in repository
- [ ] `.gitignore` properly configured

## Local Deployment Checklist

### Single Developer Setup
- [ ] Environment activated (`. .venv/bin/activate`)
- [ ] Python virtual environment working
- [ ] AWS credentials available and valid
- [ ] First test app generated successfully
- [ ] Generated apps in correct location
- [ ] Logs being written correctly

### Team Laptop Setup
- [ ] Each developer ran `./setup.sh`
- [ ] Each developer has AWS credentials
- [ ] Team using same Python version (3.11+)
- [ ] Documentation accessible to team
- [ ] Shared generated_apps repository (if applicable)

## Docker Deployment Checklist

### Image Build
- [ ] Docker installed (`docker --version`)
- [ ] `Dockerfile` reviewed and correct
- [ ] `.dockerignore` properly configured
- [ ] Image builds without errors (`docker build`)
- [ ] Image size reasonable (<500MB)
- [ ] Health check working
- [ ] All layers optimize correctly

### Container Configuration
- [ ] Volume mounts configured correctly
- [ ] Environment variables set properly
- [ ] AWS credentials mounted or passed via env
- [ ] Output directory writable
- [ ] Logging configured for container

### Local Testing
- [ ] Container runs successfully (`docker run`)
- [ ] Can execute CLI commands
- [ ] Generated apps properly stored in mounted volumes
- [ ] Logs visible and readable
- [ ] No permission issues

### Docker Compose
- [ ] `docker-compose.yml` reviewed
- [ ] Services configured correctly
- [ ] Environment variables populated
- [ ] Volumes mounted properly
- [ ] Networks configured (if multiple services)
- [ ] Compose file validates (`docker-compose config`)

## Team/Enterprise Deployment

### AWS Credentials & Security
- [ ] Using IAM roles (not hardcoded credentials)
- [ ] Minimum required IAM permissions granted
  - [ ] `bedrock:InvokeModel`
  - [ ] `bedrock:ListFoundationModels`
  - [ ] S3 access (if storing outputs)
- [ ] Credentials encrypted in transit (HTTPS)
- [ ] No credentials in `.env` file (use `.env.example` only)
- [ ] Credential rotation policy defined
- [ ] Audit logging enabled in AWS

### Shared Infrastructure
- [ ] Central repository setup (GitHub, GitLab, etc.)
- [ ] Team has read access to repository
- [ ] Team has write access to generated_apps
- [ ] SSH keys or credentials configured
- [ ] Team members can pull latest code
- [ ] Generated apps backed up appropriately

### CI/CD Integration
- [ ] Webhook configured (if auto-trigger desired)
- [ ] Pipeline variables set (AWS credentials, region)
- [ ] Pipeline secrets encrypted
- [ ] Artifact storage configured
- [ ] Logs stored and accessible
- [ ] Error notifications configured
- [ ] Deployment approval process defined

## Cloud Deployment (AWS)

### EC2 Instance
- [ ] Instance type sufficient (t3.medium or larger)
- [ ] Security group allows required access
- [ ] Elastic IP assigned (if needed)
- [ ] IAM role attached with Bedrock permissions
- [ ] OS has required packages
- [ ] Monitoring enabled (CloudWatch)
- [ ] Backups configured

### ECS/Fargate
- [ ] ECR repository created and image pushed
- [ ] Task definition created correctly
- [ ] IAM role for task execution configured
- [ ] CloudWatch logging configured
- [ ] Load balancer configured (if needed)
- [ ] Scaling policies defined
- [ ] Monitoring and alarms set up

### Lambda (if applicable)
- [ ] Function created with appropriate timeout
- [ ] Memory allocation sufficient (3+ GB)
- [ ] Execution role has Bedrock permissions
- [ ] Layer created with dependencies
- [ ] API Gateway configured (if needed)
- [ ] Async invocation configured

### Networking & Security
- [ ] VPC configured correctly
- [ ] Security groups allow Bedrock API access
- [ ] NAT Gateway configured (if in private subnet)
- [ ] VPN/Bastion access configured
- [ ] Firewall rules allow AWS Bedrock endpoints
- [ ] SSL/TLS certificates valid

## Performance & Monitoring

### Benchmarking
- [ ] Baseline performance measured
- [ ] Generation time documented
- [ ] Memory usage within limits
- [ ] CPU usage acceptable
- [ ] Network bandwidth sufficient

### Monitoring Setup
- [ ] CloudWatch metrics enabled
- [ ] Custom metrics defined
- [ ] Alarms configured for:
  - [ ] High error rate
  - [ ] Throttling events
  - [ ] Memory/CPU threshold
  - [ ] Generation timeout
- [ ] Dashboards created
- [ ] Log aggregation configured

### Logging
- [ ] Application logs sent to CloudWatch/ELK
- [ ] AWS API calls logged
- [ ] Error logging comprehensive
- [ ] Log retention policy set
- [ ] Sensitive data not logged
- [ ] Log analysis alerts configured

## Testing & Validation

### Functional Testing
- [ ] CLI works as expected
- [ ] Python projects generate correctly
- [ ] Java projects generate correctly
- [ ] All app types (web, api, cli) work
- [ ] Dependencies resolve correctly
- [ ] Generated code compiles/runs

### Load Testing
- [ ] Tested with multiple concurrent generations
- [ ] Throttling handling verified
- [ ] Rate limiting observed and documented
- [ ] Performance under load acceptable

### Disaster Recovery
- [ ] Backup/restore tested
- [ ] Failover procedure documented
- [ ] Recovery time tested
- [ ] Data loss scenarios considered
- [ ] Rollback procedure defined

## Documentation

### Setup Documentation
- [ ] Installation instructions clear and tested
- [ ] AWS configuration documented
- [ ] Environment variables documented
- [ ] Troubleshooting guide complete
- [ ] FAQ addressing common issues

### Operational Documentation
- [ ] Deployment procedure documented
- [ ] Runbook for common tasks created
- [ ] Escalation procedures defined
- [ ] On-call procedures documented
- [ ] Team responsibilities clarified

### Code Documentation
- [ ] README.md complete and accurate
- [ ] QUICKSTART.md available
- [ ] API documentation complete
- [ ] Architecture diagrams created
- [ ] Decision records documented

## Post-Deployment Verification

### Immediate (First 24 Hours)
- [ ] System running smoothly
- [ ] No critical errors in logs
- [ ] Performance meets baseline
- [ ] Team can use system
- [ ] Monitoring collecting data

### Short-term (First Week)
- [ ] No unexpected issues
- [ ] Performance stable
- [ ] Team comfortable with system
- [ ] Documentation complete and accurate
- [ ] Backup tested

### Long-term (First Month)
- [ ] System reliable and stable
- [ ] Cost within budget
- [ ] Team productivity improved
- [ ] Generated apps of high quality
- [ ] Usage patterns understood

## Rollback Plan

### If Issues Occur
- [ ] Stop deployments immediately
- [ ] Collect all error logs
- [ ] Alert team and stakeholders
- [ ] Execute rollback procedure:
  1. [ ] Revert to previous version
  2. [ ] Verify system functionality
  3. [ ] Check data integrity
  4. [ ] Restore from backup if needed
- [ ] Post-mortem scheduled
- [ ] Root cause identified

## Sign-Off

### Deployment Manager
- [ ] Name: ___________________
- [ ] Date: ___________________
- [ ] Signature: ___________________

### Team Lead
- [ ] Name: ___________________
- [ ] Date: ___________________
- [ ] Signature: ___________________

### Operations
- [ ] Name: ___________________
- [ ] Date: ___________________
- [ ] Signature: ___________________

---

**Last Updated:** November 15, 2025  
**Status:** Ready for Production
