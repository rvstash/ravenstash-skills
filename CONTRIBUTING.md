# Contributing

Keep changes focused on one demonstrated Ravenstash workflow, product boundary, or eval gap.

1. Verify the behavior against the released `rvs` command and current public documentation.
2. Update the narrowest `SKILL.md` or reference file that owns the decision.
3. Add or revise an eval case when the change addresses agent routing, command selection, context safety, credentials, or mutation behavior.
4. Run `python3 scripts/validate.py` and `git diff --check`.
5. Describe the compatible `rvs` version and the observable behavior reviewed in the pull request.

Do not add generic prompting advice, duplicate public manuals, real account names, credentials, internal environment URLs, or speculative product behavior.
