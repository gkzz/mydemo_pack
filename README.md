# Mydemo Pack for StackStorm

## TL;DR
```
$ st2 packs install \
    "https://github.com/${GITHUB_ACCT}/${PACK}.git"
$ ls /opt/stackstorm/packs/ | grep -E "${PACK}"
${PACK}
```

```
$ tree -L 2
.
├── actions
│   ├── get_distro.yaml
│   ├── git_status.yaml
│   ├── my-first-wf.meta.yaml
│   ├── orquesta-ping-with-items.meta.yaml
│   ├── playbook-demo.meta.yaml
│   ├── poll-repo.meta.yaml
│   ├── rebuild-app.meta.yaml
│   ├── scripts
│   └── workflows
├── LICENSE
├── pack.yaml
├── README.md
└── rules

4 directories, 10 file
```
