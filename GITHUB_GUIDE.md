# GitHub Issues & PRs - How to Populate Tabs

## Why Tabs Look Empty

✅ **Templates ARE created** (they auto-populate when you create new issues/PRs)  
❌ **But no actual issues/PRs exist yet** (because we haven't created any)

This guide shows you how to create sample issues and PRs to populate those tabs.

---

## 📋 Step-by-Step: Create Sample Issues

### **Issue #1: Bug Report** (Using Template)

**Go to:** https://github.com/Manvendra420/payment-dispute-engine/issues

1. Click **"New Issue"** button
2. Select **"Bug Report"** template
3. Fill in as follows:

```
Title: [BUG] SLA calculation incorrect for CHARGEBACK type

Describe the Bug:
SLA deadline calculation appears to add extra hours for CHARGEBACK disputes.

Steps to Reproduce:
1. Create a CHARGEBACK dispute
2. Check the sla_deadline field
3. Compare with expected 45-hour deadline

Expected Behavior:
CHARGEBACK disputes should have exactly 45-hour SLA

Actual Behavior:
The calculated deadline shows 47 hours instead of 45

Environment:
- OS: Windows 10
- Python Version: 3.11
- Dispute Engine Version: 0.1.0
- Docker: No

Error Message:
Expected deadline 2026-03-02 19:00:00, got 2026-03-02 21:00:00
```

4. Click **"Submit new issue"**

---

### **Issue #2: Feature Request** (Using Template)

**Go to:** https://github.com/Manvendra420/payment-dispute-engine/issues

1. Click **"New Issue"** button
2. Select **"Feature Request"** template
3. Fill in as follows:

```
Title: [FEATURE] Add email notifications for SLA approaching

Is Your Feature Request Related to a Problem?
Yes, our team is missing SLA deadline notifications and often misses 24-hour windows.

Describe the Solution You'd Like:
Add email notification system that alerts users when:
- SLA deadline is within 24 hours
- SLA deadline has been breached
- New evidence has been uploaded

Describe Alternatives You've Considered:
- SMS notifications (but email more reliable)
- In-app notifications only (but users don't check app)
- Slack webhooks (but not all teams use Slack)

Use Case / Scenario:
Operations team works in shifts. They need proactive notifications to avoid missing 
SLA deadlines which impact merchant relationships and revenue.

Acceptance Criteria:
- [ ] Email sent 24 hours before SLA deadline
- [ ] Email sent immediately if SLA breached
- [ ] Template customizable per environment
- [ ] Email addresses configurable per merchant
- [ ] Delivery confirmed with logging
```

4. Click **"Submit new issue"**

---

### **Issue #3: Documentation** (Using Template)

**Go to:** https://github.com/Manvendra420/payment-dispute-engine/issues

1. Click **"New Issue"** button
2. Select **"Documentation"** template
3. Fill in as follows:

```
Title: [DOCS] Add database schema documentation

What Documentation Needs to be Updated?
Database schema diagram and description missing from IMPLEMENTATION.md

Current State:
IMPLEMENTATION.md explains the code but doesn't show:
- Table structure
- Relationships between entities
- Indexing strategy
- Migration process

Expected State:
Should include:
- ER diagram showing disputes, events, evidence relationships
- SQL schema with DDL statements
- Explanation of indexing on frequently queried fields
- Migration guide using Alembic

Additional Context:
New developers onboarding would benefit from seeing database design before diving 
into ORM code.
```

4. Click **"Submit new issue"**

---

### **Issue #4-7: Roadmap Issues** (Phase 2-5)

Create one for each phase:

**Issue #4: PostgreSQL Integration**
```
Title: [PHASE-2] PostgreSQL Database Integration

Database integration work from ROADMAP Phase 2

Tasks:
- [ ] Set up PostgreSQL connection pool
- [ ] Create schema migrations with Alembic
- [ ] Implement SQLAlchemy ORM models
- [ ] Replace in-memory storage with real database
- [ ] Add transaction management
- [ ] Implement retry logic

Estimated: 2-3 weeks
Complexity: Medium
```

**Issue #5: Event Queue Implementation**
```
Title: [PHASE-3] Azure Service Bus Event Queue

Event queue system from ROADMAP Phase 3

Tasks:
- [ ] Set up Azure Service Bus connection
- [ ] Create message queue for dispute events
- [ ] Implement async event publishing
- [ ] Build event consumer/processor
- [ ] Error handling and dead-letter queue
- [ ] Message retry logic

Estimated: 3-4 weeks
Complexity: High
```

**Issue #6: Frontend Application**
```
Title: [PHASE-4] Next.js Frontend Application

Frontend from ROADMAP Phase 4

Tasks:
- [ ] Set up Next.js with TypeScript
- [ ] Create authentication/authorization
- [ ] Build dispute dashboard
- [ ] Build evidence portal
- [ ] Status transition UI
- [ ] Search and filtering

Estimated: 4-6 weeks
Complexity: High
```

**Issue #7: Advanced Features**
```
Title: [PHASE-5] Advanced Analytics & ML Integration

Advanced features from ROADMAP Phase 5

Tasks:
- [ ] Prediction model for dispute outcomes
- [ ] ML confidence scoring
- [ ] Anomaly detection
- [ ] Advanced analytics dashboard
- [ ] External integrations (Stripe, PayPal)

Estimated: 6-8 weeks
Complexity: Very High
```

---

## 🔀 Step-by-Step: Create Sample PR

**Go to:** https://github.com/Manvendra420/payment-dispute-engine/pulls

1. Click **"New Pull Request"** button
2. Select base: `main`, compare: `feature/add-dispute-filtering` (create branch if needed)
3. The PR template auto-populates, fill in:

```
## Description
Added filtering capabilities to dispute list endpoint allowing merchants to filter by status.

## Type of Change
- [ ] Bug fix
- [x] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issue
Closes # [Optional]

## Changes Made
- Added status filter parameter to GET /api/v1/disputes endpoint
- Added merchant_id filter parameter
- Added limit and offset for pagination
- Updated dispute list response to include total count

## Testing
- [x] Unit tests added/updated
- [x] Integration tests added/updated
- [x] Manual testing completed
- [x] All existing tests pass

## Testing Details
Tested filters with:
- Single status filter (e.g., OPEN)
- Multiple merchant IDs
- Pagination with offset/limit
- Combination of all filters

## Screenshots
N/A - Backend API only

## Checklist
- [x] Code follows style guidelines
- [x] Self-review completed
- [x] Comments added for complex areas
- [x] Documentation updated
- [x] No new warnings generated
- [x] Tests pass locally
- [x] No breaking changes

## Breaking Changes
None - backwards compatible, new parameters are optional.
```

3. Click **"Create pull request"**

---

## ✅ What You'll See After Creating These

| Tab | Before | After |
|-----|--------|-------|
| **Issues** | 0 open, 0 closed | 7 open issues |
| **Pull Requests** | Empty | 1 PR visible |
| **Insights** | No activity | Activity graph populated |

---

## 📊 Result: Populated Repository

After creating these:

```
✅ Issues Tab: 7 active issues (bugs, features, docs, roadmap)
✅ Pull Requests Tab: 1 PR with auto-populated template
✅ Insights Tab: Activity graph showing contributions
✅ Repository looks: Professional & active
```

---

## 🎯 Quick Checklist

- [ ] Create Bug Report issue
- [ ] Create Feature Request issue
- [ ] Create Documentation issue
- [ ] Create Phase-2 roadmap issue
- [ ] Create Phase-3 roadmap issue
- [ ] Create Phase-4 roadmap issue
- [ ] Create Phase-5 roadmap issue
- [ ] Create sample PR

---

## 💡 Tips

1. **Use Labels:** After creating issues, click "Labels" and add:
   - `bug` (for bug reports)
   - `enhancement` (for features)
   - `documentation` (for docs)
   - `roadmap` (for phase issues)

2. **Use Milestones:** Click "Milestones" and create:
   - Phase 2 - Database
   - Phase 3 - Event Queue
   - Phase 4 - Frontend
   - Phase 5 - Advanced

3. **Assign to Yourself:** When creating, click "Assignees" and select yourself

4. **Link to Roadmap:** In issue description, reference ROADMAP.md

---

## 🚀 After You Do This

Your repository will have:
- ✅ 7 issues showing active development
- ✅ 1 PR demonstrating the template
- ✅ Professional appearance
- ✅ Clear roadmap items
- ✅ Contribution guidelines in action

**Go try it!** 👉 https://github.com/Manvendra420/payment-dispute-engine/issues
