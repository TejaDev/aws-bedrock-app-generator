# Quick Reference

## Commands

### Interactive Mode
```bash
python3 generate.py
```

### Non-Interactive Mode
```bash
python3 cli.py --name myapp --requirements "description" --type api --stack python
```

## Arguments

```
--name TEXT              Application name
--requirements TEXT      App requirements
--type [api|web|cli|backend]  App type (default: web)
--stack [python|nodejs|typescript|java]  Tech stack (default: python)
--output-dir PATH        Output directory
--no-tests              Skip test generation
--region TEXT           AWS region
-i, --interactive       Run interactively
-h, --help             Show help
```

## Project Structure

```
generated_apps/
└── your-app/
    ├── src/                # Source code
    │   ├── api/
    │   ├── models/
    │   ├── middleware/
    │   └── utils/
    ├── your-app/           # Main package
    │   ├── __main__.py
    │   ├── main.py
    │   └── config.py
    ├── tests/
    ├── requirements.txt
    ├── setup.py
    ├── README.md
    └── APP_SPECIFICATION.json
```

## After Generation

```bash
cd generated_apps/your-app
./setup.sh              # Setup
python -m your_app     # Run
```

## Tips

- Use kebab-case for app names: `my-app`
- Be detailed in requirements
- Check generated README.md for app-specific info
