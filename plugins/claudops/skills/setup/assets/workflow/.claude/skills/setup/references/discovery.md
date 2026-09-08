# Discovery outputs

Use when configuring a new project or re-detecting changed values. Read only the categories needed for the requested scope; each result needs a source path or an explicit unknown.

**Tech stack:**
```
Detect the project's technology stack by examining:
- package.json / go.mod / pyproject.toml / Gemfile / Cargo.toml / pom.xml
- Import patterns in source files (framework detection)
- ORM/database config files (prisma/, alembic/, db/migrate/, etc.)
- Auth configuration (firebase config, auth0, clerk, passport setup)
- Test configuration (jest.config, pytest.ini, vitest.config, .rspec)
- CI/CD files (.github/workflows/, .gitlab-ci.yml, Jenkinsfile)

Return a structured report:
- Language: [TypeScript/Python/Go/Ruby/Java/Rust/etc.]
- Framework: [NestJS/Express/Next.js/Django/FastAPI/Rails/Gin/Spring/etc.]
- ORM: [Prisma/TypeORM/Drizzle/SQLAlchemy/GORM/ActiveRecord/etc.] or "none"
- Auth: [Firebase JWT/Auth0/Clerk/Passport/custom JWT/etc.] or "none detected"
- Test framework: [Jest/Vitest/pytest/RSpec/go test/JUnit/etc.]
- Package manager: [npm/yarn/pnpm/pip/poetry/bundler/cargo/etc.]
- CI system: [GitHub Actions/GitLab CI/etc.] or "none detected"
```

**Project structure:**
```
Map the project's directory structure:
- Is this a monorepo? (multiple package.json, workspaces, nx.json, turbo.json)
- Source directories (src/, app/, lib/, cmd/, backend/src/, etc.)
- Test directories (tests/, __tests__/, test/, spec/, *_test.go, etc.)
- Documentation directories (docs/, doc/, documentation/)
- Config files (tsconfig.json, pyproject.toml, go.mod, etc.)
- Schema/migration files (prisma/schema.prisma, db/schema.rb, alembic/, etc.)
- Architecture docs (any file describing project structure or conventions)

Return a structured report:
- Monorepo: yes/no (if yes, list workspace names and paths)
- Source dir(s): [paths]
- Test dir(s): [paths]
- Docs dir: [path] or "none"
- Config files: [list]
- Schema path: [path] or "N/A"
- Architecture docs found: [paths] or "none"
```

**Commands and conventions:**
```
Detect the project's standard commands and conventions:
- Read package.json scripts / Makefile / pyproject.toml scripts / taskfile.yml
- Identify: test command, lint command, build command, format command, typecheck command, coverage command
- Check for existing .claude/ or .cursor/ configuration
- Read any architecture docs found to understand patterns (DDD, MVC, hexagonal, etc.)
- Detect architecture layers from directory structure (controllers/, services/, models/, etc.)

Return a structured report:
- Test command: [command]
- Lint command: [command] or "none"
- Build command: [command] or "none"
- Format command: [command] or "none"
- Typecheck command: [command] or "none"
- Coverage command: [command] or "none"
- Architecture pattern: [description] or "not detected"
- Layer structure: [description of layers and their responsibilities]
- Layer rules: [dependency direction, encapsulation rules]
- Existing .claude/: yes/no (if yes, list what's configured)
```

