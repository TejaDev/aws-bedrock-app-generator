# Getting Started

## Quick Start

```bash
python3 generate.py
```

## Usage Modes

### Interactive (Recommended)
```bash
python3 generate.py
```

### With CLI Arguments
```bash
python3 cli.py --name myapp --requirements "Your description" --type web --stack python
```

### Using CLI Help
```bash
python3 cli.py --help
```

## After Generation

Your app will be in `generated_apps/your-app-name/`

```bash
cd generated_apps/your-app-name
cat README.md          # Read app-specific instructions
./setup.sh             # Setup environment
python -m your_app_name  # Run the app
```

## Example Requirements

### REST API
```
Create a REST API for task management with:
- CRUD operations
- User authentication with JWT
- Task filtering and sorting
- Pagination support
- Database persistence
```

### Web Application
```
Build an analytics dashboard with:
- Real-time data visualization
- User authentication
- Responsive design
- Dark/light theme support
```

### CLI Tool
```
Create a data processing tool:
- Read and parse CSV files
- Validate and transform data
- Export to multiple formats
- Progress reporting
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Command not found | Ensure you're in project root |
| Module not found | Run `pip install -r requirements.txt` |
| AWS credential error | Run `aws configure` |

## Documentation

- **QUICK_REFERENCE.md** - Commands and examples
- **README.md** - Project overview
- **IMPLEMENTATION_GUIDE.md** - Technical details
