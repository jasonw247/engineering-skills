module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [2, 'always', ['feat', 'fix', 'docs', 'refactor', 'test', 'chore']],
    'scope-enum': [2, 'always', ['sync', 'gateway', 'cli', 'docs']],
    'scope-empty': [2, 'never'],
    'header-max-length': [2, 'always', 60],
  },
};
