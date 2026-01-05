# Security Policy

## Overview

SUB-AGI is an experimental artificial general intelligence research project. While currently in early developmental stages (targeting 3-year-old cognitive equivalence), we take security seriously to ensure responsible AGI development.

## Supported Versions

SUB-AGI is currently in **Phase 1: Symbol Grounding** (pre-alpha).

| Version | Status | Security Support |
| ------- | ------ | ---------------- |
| 0.1.x (current) | Development | Limited - experimental code |
| < 0.1.0 | Not released | N/A |

## Scope

### In Scope

- Code injection vulnerabilities in the mind kernel or environment
- Unauthorized access to internal state or memories
- Unsafe behavior generation (e.g., actions that could harm in future embodied versions)
- Privacy issues with logged data or episodic memories
- Workflow automation security (GitHub Actions)

### Out of Scope

- Theoretical AGI safety concerns (alignment, control problems) - these are research topics, not security vulnerabilities
- Performance issues or bugs that don't have security implications
- Social engineering attacks on contributors

## Known Limitations

⚠️ **Current system limitations:**

1. **No sandboxing**: SUB-AGI runs with full Python privileges
2. **State persistence**: MindState objects are not encrypted
3. **Experiment logs**: May contain sensitive debugging information
4. **No authentication**: Anyone can interact with a running instance

These are acceptable for Phase 1 research but will need addressing before any deployment.

## Reporting a Vulnerability

### How to Report

If you discover a security vulnerability in SUB-AGI:

**Do:**
- Email privately to: **sarkarsubhadip604@gmail.com**
- Include:
  - Description of the vulnerability
  - Steps to reproduce
  - Potential impact
  - Suggested fix (if you have one)

**Don't:**
- Open a public GitHub issue for security vulnerabilities
- Share exploit code publicly before we've had a chance to address it

### Response Timeline

- **Acknowledgment**: Within 48 hours
- **Initial assessment**: Within 1 week
- **Fix or mitigation**: Depends on severity (2-4 weeks for high-priority issues)
- **Public disclosure**: After fix is merged and deployed

### Responsible Disclosure

We follow a **90-day disclosure policy**:

1. You report the vulnerability privately
2. We acknowledge and work on a fix
3. After the fix is deployed, we coordinate on public disclosure
4. If no fix is available after 90 days, we may jointly decide on disclosure terms

## Safety Considerations for AGI Research

Beyond traditional software security, SUB-AGI raises unique concerns:

### Current Stage (Phase 1-2)

- **Risk Level**: Low - system has no autonomy or real-world interaction
- **Containment**: Runs in isolated processes, no network access
- **Capabilities**: Limited to text I/O and 2D grid navigation

### Future Stages (Phase 3+)

As SUB-AGI develops more advanced capabilities:

- **Goal specification**: Ensure goals can't be misinterpreted
- **Action constraints**: Hard limits on allowable actions
- **Transparency**: All decisions must be inspectable
- **Kill switch**: Ability to pause or reset the system at any time

### Red Teaming

We welcome responsible attempts to:

- Find ways to make SUB-AGI behave unexpectedly
- Identify goal misspecification scenarios
- Test safety constraints

**Please report findings through the security disclosure process above.**

## Security Best Practices for Contributors

### Code Review

- All code changes require review before merging
- Pay special attention to:
  - Input validation
  - State mutation logic
  - Reward/goal definitions
  - Action selection mechanisms

### Experiment Safety

- Always run experiments in isolated environments
- Set clear termination conditions
- Log all actions and state changes
- Never run SUB-AGI with elevated privileges

### Data Privacy

- Don't commit logs containing personal information
- Episodic memories should be anonymized before sharing
- Be cautious with `MindState.to_dict()` outputs

## Incident Response

If a security incident occurs:

1. **Containment**: Immediately halt affected workflows/instances
2. **Assessment**: Determine scope and impact
3. **Remediation**: Deploy fixes
4. **Communication**: Notify contributors and users
5. **Post-mortem**: Document what happened and how to prevent recurrence

## Security Roadmap

### Phase 2-3 (Next 6 months)

- [ ] Add input sanitization for all external data
- [ ] Implement state encryption for sensitive memories
- [ ] Create safety test suite
- [ ] Add rate limiting for action generation

### Phase 4-5 (6-12 months)

- [ ] Formal verification of core cognitive loops
- [ ] Sandboxed execution environment
- [ ] Audit logging for all state transitions
- [ ] External safety review

## Contact

- **Security Issues**: sarkarsubhadip604@gmail.com
- **General Questions**: GitHub Issues
- **Project Lead**: Subhobhai (@subhobhai943)

## Acknowledgments

We thank security researchers who responsibly disclose vulnerabilities. Contributors will be acknowledged (with permission) in:

- Release notes
- Project README
- Academic publications if applicable

---

**Remember**: SUB-AGI is experimental research software. Use in production environments is not recommended at this stage.
