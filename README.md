# Azure Landing Zone & Self-Service Platform

[Portfolio home](https://github.com/olumideakinseye77-glitch/it-cloud-portfolio) · [All Azure projects](https://github.com/olumideakinseye77-glitch/it-cloud-portfolio/tree/main/azure-projects)


## Purpose
I am building this project to challenge myself with reusable Terraform,
Azure governance and controlled self-service deployments.

The goal is to accept an environment request, validate it, review the
infrastructure plan, approve deployment and verify the result.

## Scope
A single-subscription portfolio lab demonstrating enterprise concepts.
This is not a complete production Azure landing zone.

## Planned capabilities
- Reusable Terraform modules for networking and resource organisation.
- Python validation of deployment requests.
- Scoped Azure Policy and RBAC controls.
- GitHub Actions checks and an approval-controlled deployment workflow.
- Ownership tags, budget visibility and cleanup procedures.
- Evidence showing accepted and rejected requests.
- Architecture diagrams and explanations of design trade-offs.

## Status
Repository setup. No Project 6 Azure resources deployed.

## Cost control
Build and test locally before deploying.
Review Azure plans and costs before applying changes.
Remove billable lab resources after recording evidence.
Budgets provide visibility; they are not a spending cap.

## Evidence
Document what was tested, why each service was selected,
alternatives considered and any unverified limitations.
Never commit credentials or Terraform state.
