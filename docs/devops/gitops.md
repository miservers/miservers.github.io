---
layout: default
title: GitOps
parent: DevOps
nav_order: 3
---

### Principes

| Principe | Détail |
|----------|--------|
| **Directories, pas branches** | Un dossier par env sur `main`. Pas de branche `dev`/`staging`/`prod`. Tout est diffable depuis un seul endroit. |
| **2 repos séparés** | Code applicatif dans `my-app`, configuration de déploiement dans `my-app-config`. Les devs n'accèdent qu'au premier. |
| **Path-based restrictions** | Bitbucket Data Center applique des reviewers obligatoires selon le path modifié. `prod/**` → approbation ops obligatoire. |
| **CI = seul writer sur config** | Seul le compte de service CI peut ouvrir des PRs sur `my-app-config`. Les humains approuvent, ils ne pushent jamais directement. |


### `my-app-config` — accès restreint (write: ci-bot + ops uniquement)

```
my-app-config/
└── environments/
    ├── dev/
    │   └── values.yaml   # push direct par ci-bot ou devs
    ├── staging/
    │   └── values.yaml        # PR auto CI ou ops→ approbation  ops-team
    └── prod/
        └── values.yaml        # PR manuelle → approbation ops-team
```

## Configuration Bitbucket

### 1. Protéger `main` (Branch permissions)

```
Branch       : main
Type         : Branch
─────────────────────────────────────
✅ Prevent direct push     → tout le monde
✅ Require pull request
✅ Minimum approvals       → 1
```

### 2. Required Reviewers par path

`Repo Settings → Branch permissions → Required reviews`

```
Pattern : environments/prod/**
Group   : ops-team
Min     : 1

Pattern : environments/staging/**
Group   : leads-team
Min     : 1
```

### 3. Permissions sur `my-app-config`

```
ops-team   → Write
leads-team → Write
devs-team  → Read    ← les devs ne peuvent pas push
ci-bot     → Write   ← seul compte de service autorisé à ouvrir des PRs
```
