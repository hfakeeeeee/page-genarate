# AI Web Builder - Independent Project

An intelligent web application generator that creates modern React/Vue applications using AI. This is a complete, standalone FastAPI service that provides both API endpoints and a web interface for generating production-ready web projects.

## Features

🎨 **AI-Powered Generation**: Create complete web applications from simple text descriptions  
🚀 **Multiple Frameworks**: Support for React and Vue with JavaScript/TypeScript  
💡 **Modern UI Patterns**: Generates responsive layouts with real images and icons  
📦 **Complete Projects**: Full project structure with routing and components  
⚡ **Real-time Progress**: Live updates during generation process  
💾 **Project Management**: Store, download, and manage generated projects  

## Getting Started

### Prerequisites
- Python 3.8+
- Azure OpenAI API key (primary) or OpenAI API key (fallback)

### Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your Azure OpenAI API key (or OpenAI API key as fallback)
   ```

3. **Start the application:**
   ```bash
   uvicorn app.main.main:app --reload
   ```

4. **Access the service:**
   - **API Documentation**: http://localhost:8000/docs
   - **Page Generator UI**: http://localhost:8000/generator/
   - **Health Check**: http://localhost:8000/healthcheck

## API Endpoints

### Core Endpoints
- `GET /healthcheck` - Service health status
- `GET /hello` - Hello world endpoint

### Page Generator
- `GET /generator/` - Web interface for page generation
- `POST /generator/generate` - Start page generation process
- `GET /generator/status/{id}` - Check generation progress
- `GET /generator/projects` - List all generated projects
- `GET /generator/download/{id}` - Download project ZIP
- `DELETE /generator/projects/{id}` - Delete project

## Usage

### Web Interface
1. Navigate to http://localhost:8000/generator/
2. Enter your project description (e.g., "A modern bookstore with search and shopping cart")
3. Choose framework (React/Vue) and language (JavaScript/TypeScript)
4. Select AI model based on quality/cost preference
5. Click "Generate Project" and monitor progress
6. Download your complete project when ready

### API Usage
```python
import requests

# Start generation
response = requests.post("http://localhost:8000/generator/generate", json={
    "user_prompt": "A modern e-commerce store for books",
    "framework": "React",
    "language": "JS",
    "model": "gpt-4o"
})

generation_id = response.json()["generation_id"]

# Check status
status = requests.get(f"http://localhost:8000/generator/status/{generation_id}")

# Download when complete
if status.json()["status"] == "completed":
    project_zip = requests.get(f"http://localhost:8000/generator/download/{generation_id}")
```

## Configuration

Set these environment variables in `.env`:

```env
# Azure OpenAI Configuration (Primary)
AZURE_ENDPOINT=https://dhp-search-east-npe-0.openai.azure.com/
AZURE_MODEL=gpt-4.1
AZURE_API_VERSION=2024-02-01
AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here

# Fallback OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
MODEL=gpt-4o

# Application Settings
OUTPUT_PATH=./output
BASE_PROJECTS_PATH=./base_projects
PROMPTS_PATH=./prompts
```

## Architecture

```
app/
├── main/
│   ├── main.py              # FastAPI application setup
│   └── routers/
│       ├── hello_world.py   # Example endpoints
│       └── page_generator.py # Page generation API
├── services/
│   ├── page_generator.py    # AI page generation logic
│   └── project_manager.py   # Project packaging & management
├── models.py                # Pydantic data models
└── config.py               # Configuration management
```

## Generated Projects

Each generated project includes:
- ✅ Complete React/Vue project structure
- ✅ Modern, responsive pages with full-height layouts
- ✅ Real images from Unsplash
- ✅ Inline SVG icons
- ✅ Router configuration
- ✅ Ready to run with `npm start`

## Cost Optimization

- **GPT-4o**: ~$0.15-0.30 per project (best quality)
- **GPT-4-turbo**: ~$0.10-0.20 per project (good balance)
- **GPT-3.5-turbo**: ~$0.02-0.05 per project (most economical)

Enable "Cost Optimization" to generate fewer pages for testing.

## Development

### Running Tests
```bash
# TODO: Add test commands
```

### Building for Production
```bash
# TODO: Add build commands
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.