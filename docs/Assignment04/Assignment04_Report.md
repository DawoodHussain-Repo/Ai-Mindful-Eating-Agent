# Assignment 04: Resource Management and Leveling
## Mindful Eating Agent Project

---

**Course:** Fundamentals of Software Project Management  
**Section:** E  
**Submission Date:** December 4, 2025

---

## Team Members

| Name | Roll Number | Role |
|------|-------------|------|
| Dawood Hussain | 22i-2410 | Project Manager |
| Gulsher Khan | 22i-2637 | Technical Lead |
| Ahsan Faraz | 22i-8791 | AI/ML Developer |

---

## Tech Stack Update

Following a last-minute technical decision, the project tech stack has been updated:

- **Backend Framework:** Flask (Python)
- **Frontend:** HTML/CSS (served via Flask templates)
- **AI/Agent Framework:** LangGraph (for agent workflow orchestration)

This change from the original React Native mobile app to a web-based application impacts development timelines and resource allocation.

---

## Executive Summary

This assignment presents a comprehensive resource management analysis for the Mindful Eating Agent project, including:

1. **Resource Assignment Matrix (RAM)** - RACI matrix showing clear responsibility assignments
2. **Resource Loading Analysis** - Week-by-week workload distribution for each team member
3. **Resource Leveling** - Identification and resolution of resource conflicts
4. **Updated Schedule** - Adjusted project timeline reflecting resource constraints

### Key Findings

**Initial Schedule Issues:**
- **Gulsher Khan:** Over-allocated at 120% (48 hours/week) during Weeks 8-13
- **Ahsan Faraz:** Over-allocated at 120% (48 hours/week) during Weeks 8-13
- **Dawood Hussain:** Under-allocated at 60-70% during development phase

**After Resource Leveling:**
- All team members balanced at ≤100% allocation
- Project duration extended from 112 to 119 days (+7 days)
- New completion date: December 24, 2025 (was December 15, 2025)
- Sustainable workload distribution achieved
- Quality risk reduced through adequate task time allocation

---

## Task 1: Resource Assignment Matrix (RAM)

### RACI Matrix Overview

The Responsibility Assignment Matrix uses the RACI model:
- **R** = Responsible (Does the work)
- **A** = Accountable (Final authority/approval)
- **C** = Consulted (Provides input)
- **I** = Informed (Kept updated)

### Key Assignments

#### Dawood Hussain (Project Manager)
- **Primary Responsibilities:**
  - Project Coordination (R)
  - Risk Management (R)
  - Requirements Gathering (R)
  - Schedule Development (R)
  - User Acceptance Testing (R)
  - All closure activities (R)

#### Gulsher Khan (Technical Lead)
- **Primary Responsibilities:**
  - System Architecture Design (R)
  - Backend API Development - Flask (R)
  - Frontend Development - HTML/CSS/Flask (R)
  - Environment Setup (R)
  - Production Deployment (R)

#### Ahsan Faraz (AI/ML Developer)
- **Primary Responsibilities:**
  - LangGraph Agent Development (R)
  - Agent Workflow Design (R)
  - LangGraph Implementation (R)
  - Agent Testing & Validation (R)
  - Database Design (R)
  - Functional Testing (R)

### Collaborative Tasks

Several critical tasks require collaboration:
- **Integration Testing:** All team members (Gulsher R, Ahsan A, Dawood C)
- **Agent Integration:** Ahsan & Gulsher (joint R)
- **Quality Management:** Dawood & Ahsan (joint R)
- **Risk Planning:** Dawood & Gulsher (Dawood R, Gulsher A)

**Complete RACI Matrix:** See `resource_assignment_matrix.csv`

---

## Task 2: Resource Loading

### Initial Resource Loading (Before Leveling)

#### Week-by-Week Analysis

**Weeks 1-7 (Sep 1 - Oct 19): Planning Phase**
- Balanced workload across team
- Average utilization: 80-100%
- No significant conflicts

**Weeks 8-13 (Oct 20 - Nov 30): Development Phase - CRITICAL OVER-ALLOCATION**
- **Gulsher:** 48 hours/week (120% allocation)
  - Backend API Development (Flask)
  - Frontend Development (HTML/CSS) overlap
  - Environment setup responsibilities
  
- **Ahsan:** 48 hours/week (120% allocation)
  - LangGraph Agent Development (complex, 29 days)
  - Agent workflow design
  - LangGraph implementation
  - Testing and validation
  
- **Dawood:** 24 hours/week (60% allocation)
  - Under-utilized during critical development phase
  - Available capacity not leveraged

**Weeks 14-16 (Dec 1 - Dec 15): Testing & Deployment**
- Return to balanced allocation
- All team members at 80-100%

### Resource Histograms

**Individual Histograms (Initial):**
- Visual representation showing over-allocation in red
- Under-allocation in orange
- Standard capacity line at 40 hours/week

**Project-Level Histogram (Initial):**
- Total team capacity: 120 hours/week
- Weeks 8-13 show exactly 120 hours (at capacity limit)
- Risk of burnout and quality issues

**Generated Files:**
- `initial_individual_histograms.png`
- `project_level_comparison.png`
- `stacked_comparison.png`

---

## Task 3: Resource Leveling

### Identified Conflicts

#### Conflict 1: Gulsher Khan (Technical Lead)
**Period:** Weeks 8-13 (Oct 20 - Nov 30)  
**Allocation:** 120% (48 hours/week)  
**Conflicting Tasks:**
- Backend API Development (Flask) - 14 days
- Frontend Development (HTML/CSS/Flask) - 28 days (overlapping start)
- Integration testing preparation

**Impact:**
- High burnout risk
- Quality degradation on critical path activities
- Potential schedule delays
- Technical debt accumulation

#### Conflict 2: Ahsan Faraz (AI/ML Developer)
**Period:** Weeks 8-13 (Oct 20 - Nov 30)  
**Allocation:** 120% (48 hours/week)  
**Conflicting Tasks:**
- LangGraph Agent Development - 24 days (most complex component)
- Agent workflow design
- LangGraph implementation
- Agent testing & validation
- Continuous quality management duties

**Impact:**
- Risk to AI agent quality (accuracy requirements)
- Insufficient testing time
- Extended development timeline
- Critical path at risk

#### Conflict 3: Dawood Hussain (Project Manager)
**Period:** Weeks 7-13 (Oct 13 - Nov 30)  
**Allocation:** 60-80% (24-32 hours/week)  
**Issue:** Under-allocation

**Opportunity:**
- Available capacity to absorb tasks from over-allocated members
- Can increase coordination and support activities
- Better utilization of PM skills during critical phase

### Leveling Strategy Applied

#### Strategy 1: Task Redistribution
1. **Delayed Frontend Development Start**
   - Original: Oct 25 (Week 9)
   - Revised: Nov 6 (Week 10)
   - Impact: Reduces Gulsher's peak from 120% to 100%
   - Rationale: Frontend depends on API completion; delay is feasible

2. **Extended LangGraph Development Timeline**
   - Original: 24 days (Oct 20 - Nov 15)
   - Revised: 29 days (Oct 20 - Nov 20) with reduced daily intensity
   - Impact: Reduces Ahsan's allocation from 120% to 100%
   - Rationale: Complex AI work benefits from sustainable pace

3. **Increased PM Involvement**
   - Dawood takes on more integration testing preparation
   - Increased coordination during Weeks 11-13
   - Impact: Better capacity utilization (60% → 85%)

#### Strategy 2: Task Decomposition
- Broke down large tasks into smaller, manageable chunks
- Created clear handoff points for collaborative work
- Distributed sub-tasks based on availability

#### Strategy 3: Buffer Management
- Used available project buffer (7 days)
- Extended critical activities rather than compress
- Prioritized quality over aggressive timeline

### Leveling Results

**Resource Utilization After Leveling:**
- **Gulsher:** Peak reduced from 120% to 100% (20% improvement)
- **Ahsan:** Peak reduced from 120% to 100% (20% improvement)
- **Dawood:** Average increased from 70% to 85% (15% improvement)

**Schedule Impact:**
- Project duration: 112 → 119 days (+7 days)
- New completion: December 24, 2025
- Critical path maintained but extended
- All milestones shifted proportionally

**Quality & Risk Benefits:**
- Eliminated burnout risk
- Adequate time for complex LangGraph development
- Improved testing coverage
- Sustainable team morale
- Reduced technical debt risk

### Leveled Resource Histograms

**Individual Histograms (Leveled):**
- All bars in green (balanced allocation)
- No over-allocation periods
- Smooth workload distribution

**Project-Level Histogram (Leveled):**
- Extended to 17 weeks
- Peak utilization at 120 hours (Week 14)
- Sustainable distribution throughout

**Generated Files:**
- `leveled_individual_histograms.png`
- `project_level_comparison.png` (before/after)
- `stacked_comparison.png` (before/after)

---

## Task 4: Updated Network Diagram & Schedule

### Schedule Adjustments

#### Major Changes

1. **LangGraph Agent Development**
   - Duration: 24 → 29 days (+5 days)
   - Sub-tasks extended proportionally:
     - Agent Workflow Design: 6 → 7 days
     - LangGraph Implementation: 9 → 12 days
     - Testing & Validation: 6 → 8 days
     - Integration: 2 → 3 days

2. **Frontend Development (HTML/CSS/Flask)**
   - Start date delayed: Oct 25 → Nov 6 (+12 days)
   - Duration unchanged: 28 days
   - Finish date: Nov 30 (instead of Nov 20)

3. **Integration Testing**
   - Duration: 10 → 14 days (+4 days)
   - More thorough testing with balanced team
   - Start: Dec 1 (delayed from Nov 21)

4. **All Subsequent Activities**
   - Shifted by 10-12 days
   - Proportional delay maintained
   - Dependencies preserved

#### Updated Critical Path

**Critical Path Sequence (119 days):**
```
1.2.1 (Market Research) → 1.2.2 (Stakeholder ID) → 1.2.4 (Business Case) → 
M1 (Authorization) → 1.3.1 (Requirements) → M2 (Approved) → 
1.3.2 (System Arch) → 1.3.6 (Risk Planning) → M3 (Design Approved) → 
1.4.1 (Environment) → 1.4.2 (Backend API) → 1.4.4 (Frontend) → 
1.4.5 (Integration Testing) → M4 (Dev Complete) → 
1.5.1 (Functional Test) → 1.5.2 (UAT) → 1.5.4 (Deployment) → 
1.5.5 (Training) → M5 (Go Live) → 
1.6.1 → 1.6.2 → 1.6.3 → 1.6.4 → M6 (Project Closed)
```

**Parallel Critical Path:**
```
M3 → 1.4.3 (LangGraph) → 1.4.3.1 → 1.4.3.2 → 1.4.3.3 → 1.4.3.4 → 
1.4.5 (Integration Testing)
```

### Updated Network Diagram

**Format:** Draw.io XML  
**File:** `updated_network_diagram.drawio`

**Key Features:**
- Color-coded by criticality:
  - Red: Critical path (TS=0)
  - Blue: Non-critical (TS>0)
  - Purple: Resource-leveled tasks (extended/delayed)
  - Yellow: Milestones
- Shows all dependencies
- Includes ES, EF, LS, LF, TS for each activity
- Highlights resource leveling changes

### Updated WBS

**Format:** CSV  
**File:** `updated_wbs.csv`

**Columns:**
- WBS_ID
- Task_Name
- Duration_Days
- Start_Date
- Finish_Date
- Responsible
- ES, EF, LS, LF
- Total_Slack, Free_Slack
- Critical_Path
- Resource_Change
- Tech_Stack

### Gantt Chart for Visio

**Format:** CSV (Visio-compatible)  
**File:** `gantt_chart_visio.csv`

**Import Instructions:**
1. Open Microsoft Visio
2. File → New → Schedule → Gantt Chart
3. Import → `gantt_chart_visio.csv`
4. Map columns appropriately
5. Adjust formatting as needed

**Columns Included:**
- Task ID
- Task Name
- Start Date
- Finish Date
- Duration (Days)
- % Complete
- Predecessors
- Resource Names
- Milestone (Yes/No)
- Critical (Yes/No)

---

## Comparison: Initial vs Updated Schedule

| Metric | Initial Schedule | Updated Schedule | Change |
|--------|-----------------|------------------|--------|
| **Project Duration** | 112 days | 119 days | +7 days |
| **Start Date** | Sep 1, 2025 | Sep 1, 2025 | No change |
| **End Date** | Dec 15, 2025 | Dec 24, 2025 | +9 calendar days |
| **Critical Path Length** | 112 days | 119 days | +7 days |
| **Gulsher Peak Allocation** | 120% | 100% | -20% |
| **Ahsan Peak Allocation** | 120% | 100% | -20% |
| **Dawood Avg Allocation** | 70% | 85% | +15% |
| **Over-allocated Weeks** | 6 weeks | 0 weeks | Eliminated |
| **LangGraph Development** | 24 days | 29 days | +5 days |
| **Frontend Start** | Oct 25 | Nov 6 | +12 days |
| **Integration Testing** | 10 days | 14 days | +4 days |

---

## Benefits of Resource Leveling

### 1. Sustainable Workload
- No team member exceeds 100% allocation
- Reduced burnout risk
- Improved work-life balance
- Better long-term productivity

### 2. Improved Quality
- Adequate time for complex LangGraph development
- More thorough integration testing (14 days vs 10)
- Reduced technical debt
- Better code review opportunities

### 3. Risk Mitigation
- Lower schedule risk due to realistic allocation
- Reduced dependency on over-worked individuals
- Better contingency for unexpected issues
- Improved team morale and retention

### 4. Better Resource Utilization
- Dawood's capacity better utilized (70% → 85%)
- More balanced team collaboration
- Clearer task ownership and accountability

### 5. Realistic Schedule
- Stakeholder expectations properly set
- Buffer time for quality assurance
- Flexibility for scope adjustments
- Achievable milestones

---

## Risks and Mitigation

### Risk 1: Extended Timeline
**Impact:** Project completes 7 days later than originally planned  
**Mitigation:**
- Communicate early with stakeholders
- Emphasize quality benefits
- Use buffer time wisely
- Monitor progress weekly

### Risk 2: Tech Stack Change Impact
**Impact:** Flask/LangGraph may have learning curve  
**Mitigation:**
- Allocated extra time in LangGraph development
- Team training during early phases
- Technical documentation emphasis
- Pair programming for knowledge transfer

### Risk 3: Integration Complexity
**Impact:** Flask backend + LangGraph + HTML frontend integration  
**Mitigation:**
- Extended integration testing (14 days)
- Early integration checkpoints
- Continuous integration practices
- Dedicated integration task (1.4.3.4)

---

## Recommendations

### 1. Maintain Leveled Schedule
- Do not compress timeline to meet original deadline
- Quality and team health are priorities
- Communicate benefits to stakeholders

### 2. Monitor Resource Utilization Weekly
- Track actual hours vs planned
- Adjust allocations proactively
- Address emerging conflicts early

### 3. Leverage Dawood's Increased Capacity
- More active involvement in testing
- Enhanced stakeholder communication
- Risk monitoring and mitigation
- Documentation and knowledge management

### 4. Protect LangGraph Development Time
- Most complex and critical component
- Requires sustained focus
- Quality directly impacts project success
- Do not compress this timeline

### 5. Plan for Contingencies
- 7-day extension provides some buffer
- Identify tasks that could be fast-tracked if needed
- Maintain risk register
- Regular status reviews

---

## Conclusion

Resource leveling has transformed the Mindful Eating Agent project schedule from an aggressive, risky timeline to a sustainable, achievable plan. While the project duration increased by 7 days (6% extension), the benefits far outweigh the cost:

- **Eliminated all resource over-allocations**
- **Improved team utilization and balance**
- **Reduced quality and schedule risks**
- **Created realistic stakeholder expectations**
- **Enabled sustainable development pace**

The updated schedule, with completion on December 24, 2025, provides a solid foundation for successful project delivery with high quality and team satisfaction.

---

## Appendices

### Appendix A: Files Delivered
1. `resource_assignment_matrix.csv` - RACI matrix
2. `initial_resource_loading.csv` - Pre-leveling data
3. `leveled_resource_loading.csv` - Post-leveling data
4. `resource_conflicts_analysis.md` - Detailed conflict analysis
5. `updated_schedule.csv` - Complete schedule with changes
6. `updated_wbs.csv` - Updated work breakdown structure
7. `gantt_chart_visio.csv` - Visio-compatible Gantt data
8. `updated_network_diagram.drawio` - AON diagram
9. `initial_individual_histograms.png` - Resource histograms (before)
10. `leveled_individual_histograms.png` - Resource histograms (after)
11. `project_level_comparison.png` - Before/after comparison
12. `stacked_comparison.png` - Stacked resource distribution

### Appendix B: Tools Used
- **Microsoft Excel** - Resource calculations
- **Python (matplotlib, pandas)** - Histogram generation
- **Draw.io** - Network diagram
- **CSV** - Data exchange format
- **Markdown** - Documentation

### Appendix C: References
- PMBOK Guide (7th Edition) - Resource Management
- Project Management Institute (PMI) - Resource Leveling Techniques
- Assignment 02 & 03 - Previous WBS and schedule data

---

**End of Report**
