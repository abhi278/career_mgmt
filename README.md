# Resume Analyzer 📄

AI-powered resume analyzer that compares resumes against job descriptions using OpenAI's GPT-4o-mini model. Features a modern web interface built with Plotly Dash.

## Features ✨

- 📊 **Similarity Score**: Get a 0-100 match score between resume and job description
- ✅ **Matching Skills**: Identify skills that align with the job requirements
- ❌ **Missing Skills**: Discover gaps in your resume
- 💡 **AI Recommendations**: Receive actionable improvement suggestions
- 📥 **Export Results**: Download analysis results as JSON
- 🎨 **Modern UI**: Clean, responsive interface with Bootstrap
- 📁 **Multiple Input Methods**: Upload files or paste text directly

## Supported File Formats

- `.txt` - Plain text files
- `.pdf` - PDF documents
- `.docx` - Modern Word documents

**Note**: `.doc` files are not supported. Please convert to `.docx` format.

## Quick Start 🚀

### Prerequisites

- Python 3.9+
- OpenAI API key
- Docker (optional, for containerized deployment)

### Installation

#### Option 1: Using UV (Recommended)

```bash
# Install UV if you haven't
pip install uv

# Clone the repository
git clone <your-repo-url>
cd resume-analyzer

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

#### Option 2: Using pip

```bash
# Clone the repository
git clone <your-repo-url>
cd resume-analyzer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .
```

### Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your-openai-api-key-here
```

### Running the Application

#### Development Mode

```bash
python app.py
```

The application will be available at `http://localhost:8050`

#### Production Mode (with Gunicorn)

```bash
gunicorn --bind 0.0.0.0:8050 --workers 4 --timeout 120 app:server
```

## Docker Deployment 🐳

### Prerequisites

- Docker
- Docker Compose

### Build and Run

```bash
# Build the Docker image
docker-compose build

# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

The application will be available at `http://localhost:8050`

### Environment Variables

Set your OpenAI API key in `.env`:

```env
OPENAI_API_KEY=your-openai-api-key-here
```

### Docker Commands

```bash
# Rebuild after code changes
docker-compose up -d --build

# View container status
docker-compose ps

# Access container shell
docker-compose exec resume-analyzer bash

# View real-time logs
docker-compose logs -f resume-analyzer

# Remove containers and volumes
docker-compose down -v
```

## Project Structure 📁

```
resume-analyzer/
├── app.py                          # Dash frontend application
├── Dockerfile                      # Docker configuration
├── docker-compose.yml              # Docker Compose configuration
├── pyproject.toml                  # Project dependencies
├── README.md                       # This file
├── .env                            # Environment variables (create this)
├── src/
│   └── resume_analyzer/
│       ├── __init__.py
│       └── resume_analyzer.py      # Core analyzer logic
└── tests/
    └── test_resume_analyzer.py
```

## Usage Guide 📖

### Web Interface

1. **Navigate to the home page**
2. **Upload or paste job description**:
   - Click "Upload File" tab to upload a file
   - Or click "Paste Text" tab to paste text directly
3. **Upload or paste resume**:
   - Same options as job description
4. **Click "Analyze Resume"**
5. **View results**:
   - Similarity score gauge
   - Skills comparison chart
   - Matching and missing skills
   - AI-powered recommendations
6. **Download results** (optional):
   - Click "Download Results (JSON)" button

### Python API

```python
from resume_analyzer import ResumeAnalyzer

# Initialize analyzer
analyzer = ResumeAnalyzer(api_key='your-openai-api-key')

# Analyze with file paths
results = analyzer.analyze('job_description.pdf', 'resume.docx')

# Or analyze with text
job_desc = "Job description text..."
resume_text = "Resume text..."
results = analyzer.analyze(job_desc, resume_text)

# Print results
analyzer.print_results(results)

# Save to JSON
analyzer.save_results(results, 'analysis.json')
```

## Development 🛠️

### Install Development Dependencies

```bash
uv pip install -e ".[dev]"
```

### Run Tests

```bash
pytest tests/ -v --cov=src
```

### Code Formatting

```bash
# Format code with Black
black src/ app.py

# Lint with Ruff
ruff check src/ app.py

# Type check with MyPy
mypy src/
```

## API Cost Estimation 💰

The application uses OpenAI's GPT-4o-mini model, which is cost-effective:

- **Model**: gpt-4o-mini
- **Average tokens per analysis**: ~2,000-4,000 tokens
- **Estimated cost per analysis**: $0.001-0.002 USD
- **Pricing**: $0.150 per 1M input tokens, $0.600 per 1M output tokens

## Configuration Options ⚙️

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Yes | - |
| `PYTHONUNBUFFERED` | Disable Python buffering | No | 1 |

### Gunicorn Configuration

Modify in `Dockerfile`:

```bash
gunicorn --bind 0.0.0.0:8050 \
         --workers 4 \
         --timeout 120 \
         --worker-class sync \
         app:server
```

- `--workers`: Number of worker processes (adjust based on CPU cores)
- `--timeout`: Request timeout in seconds
- `--worker-class`: Worker type (sync for CPU-bound tasks)

## Troubleshooting 🔧

### Common Issues

#### 1. OpenAI API Key Not Found

```
Error: OpenAI API key must be provided or set in OPENAI_API_KEY environment variable
```

**Solution**: Create a `.env` file with your API key or export it:
```bash
export OPENAI_API_KEY='your-key-here'
```

#### 2. PDF Extraction Fails

```
Error: Failed to extract text from PDF
```

**Solution**: Ensure the PDF is not encrypted or scanned. Try converting to text format first.

#### 3. Docker Build Fails

```
Error: Cannot connect to Docker daemon
```

**Solution**: Ensure Docker is running:
```bash
# Linux/Mac
sudo systemctl start docker

# Windows
# Start Docker Desktop
```

#### 4. Port Already in Use

```
Error: Address already in use
```

**Solution**: Change the port in `docker-compose.yml`:
```yaml
ports:
  - "8051:8050"  # Use different external port
```

#### 5. File Upload Fails

**Solution**: Check file format and size. Ensure it's one of the supported formats (.txt, .pdf, .docx) and under 10MB.

## Performance Optimization 🚀

### For Production Deployment

1. **Use multiple Gunicorn workers**:
   ```bash
   gunicorn --workers 8 --bind 0.0.0.0:8050 app:server
   ```

2. **Enable caching** (add to app.py):
   ```python
   from flask_caching import Cache
   cache = Cache(app.server, config={'CACHE_TYPE': 'simple'})
   ```

3. **Use a reverse proxy** (Nginx):
   ```nginx
   location / {
       proxy_pass http://localhost:8050;
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
   }
   ```

4. **Set resource limits** in docker-compose.yml:
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '2'
         memory: 2G
   ```

## Security Considerations 🔒

1. **API Key Protection**:
   - Never commit `.env` file to version control
   - Use environment variables or secret management systems
   - Rotate API keys regularly

2. **File Upload Security**:
   - Validate file extensions
   - Limit file sizes
   - Scan uploaded files for malware (in production)

3. **Rate Limiting**:
   - Implement rate limiting for API calls
   - Monitor OpenAI API usage

4. **HTTPS**:
   - Use HTTPS in production
   - Configure SSL certificates

## Contributing 🤝

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Standards

- Follow PEP 8 style guidelines
- Add type hints where appropriate
- Write docstrings for functions and classes
- Add tests for new features
- Update documentation

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments 🙏

- OpenAI for GPT-4o-mini API
- Plotly Dash for the web framework
- Bootstrap for UI components

## Support 💬

For issues, questions, or suggestions:

1. Check the [Troubleshooting](#troubleshooting-) section
2. Search existing GitHub issues
3. Create a new issue with detailed information

## Roadmap 🗺️

- [ ] Add support for multiple resume comparison
- [ ] Implement user authentication
- [ ] Add resume templates and suggestions
- [ ] Support for more file formats
- [ ] Advanced analytics and insights
- [ ] Integration with job boards
- [ ] Mobile app version
- [ ] Multi-language support

## Changelog 📝

### Version 1.0.0 (2025-10-26)

- Initial release
- OpenAI GPT-4o-mini integration
- Plotly Dash web interface
- File upload and text input support
- Docker deployment support
- JSON export functionality

---

Made with ❤️ using Python, Plotly Dash, and OpenAI