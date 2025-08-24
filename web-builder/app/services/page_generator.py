import os
import json
import re
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Callable
from openai import AzureOpenAI

from ..config import settings
from ..models import ProjectPlan, PageInfo

class PageGeneratorService:
    def __init__(self):
        # Azure OpenAI configuration (following notebook logic)
        self.client = AzureOpenAI(
            api_version=settings.AZURE_API_VERSION,
            azure_endpoint=settings.AZURE_ENDPOINT,
            api_key=settings.AZURE_OPENAI_API_KEY
        )
        self.logger = logging.getLogger(__name__)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    async def generate_project_plan(
        self,
        user_prompt: str,
        framework: str,
        language: str
    ) -> ProjectPlan:
        """Generate project plan based on user prompt"""
        try:
            # Load system prompt
            system_prompt = self._load_prompt_template("project/project-plan-sys.md")
            
            # Create user prompt
            user_instruction = self._load_prompt_template("project/project-plan-user.md").format(
                FRAMEWORK=framework,
                LANGUAGE=language,
                USER_REQUIREMENT=user_prompt
            )
            
            # Call LLM
            response = await self._call_llm(user_instruction, system_prompt)
            
            # Parse JSON response
            project_data = json.loads(response)
            
            # Convert to ProjectPlan model
            pages = [
                PageInfo(**page) for page in project_data.get("pages", [])
            ]
            
            return ProjectPlan(
                framework=project_data.get("framework", framework),
                language=project_data.get("language", language),
                project_name=project_data.get("projectName", "Generated Project"),
                description=project_data.get("description", "AI Generated Web Application"),
                pages=pages
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate project plan: {str(e)}")
            # Return a default plan if generation fails
            return self._create_default_project_plan(user_prompt, framework, language)
    
    async def generate_pages(
        self,
        project_plan: ProjectPlan,
        progress_callback: Optional[Callable[[int, str], None]] = None
    ) -> Dict[str, str]:
        """Generate all pages for the project"""
        generated_pages = {}
        total_pages = len(project_plan.pages)
        
        # Load templates
        common_sys = self._load_prompt_template("page/gen/common.md")
        react_sys = self._load_prompt_template("page/gen/react-only.md")
        sys_prompt = common_sys + react_sys
        user_template = self._load_prompt_template("page/gen/user.md")
        
        # Load CSS resources
        css_variables = self._load_prompt_template("css/variables_small.md")
        css_selectors = self._load_prompt_template("css/selectors.md")
        
        for i, page in enumerate(project_plan.pages):
            try:
                if progress_callback:
                    progress = 30 + int((i / total_pages) * 50)  # 30-80% range
                    progress_callback(progress, f"Generating {page.name}...")
                
                # Create enhanced user prompt
                user_prompt = user_template.format(
                    CSS_VARIABLES=css_variables,
                    CSS_SELECTORS=css_selectors,
                    PROJECT_PLAN=project_plan.model_dump_json(),
                    PAGE_NAME=page.name
                )
                
                # Add UI examples
                user_prompt += self._get_ui_examples()
                
                # Generate page
                page_code = await self._call_llm(user_prompt, sys_prompt, temperature=0.3)
                
                # Save the raw response for debugging (following notebook logic)
                debug_response_path = os.path.join(settings.OUTPUT_PATH, f"debug_page_response_{page.name}.md")
                os.makedirs(os.path.dirname(debug_response_path), exist_ok=True)
                with open(debug_response_path, "w", encoding="utf-8") as f:
                    f.write(page_code)
                self.logger.info(f"Raw page response for {page.name} saved to {debug_response_path}")
                
                # Extract and clean code
                clean_code = self._extract_code_from_response(page_code, page.filepath)
                
                generated_pages[page.filepath] = clean_code
                page.generated = True
                
                # Quality checks for modern UI requirements (following notebook logic)
                quality_issues = []
                
                # Check for React import
                if 'import React' not in clean_code:
                    quality_issues.append("Missing React import")
                    
                # Check for full page layout
                if 'min-height: 100vh' not in clean_code and 'height: 100vh' not in clean_code:
                    quality_issues.append("Missing full-page layout")
                    
                # Check for Unsplash images
                if 'source.unsplash.com' not in clean_code and ('coverImage' in clean_code or 'img' in clean_code):
                    quality_issues.append("Missing real image URLs")
                    
                # Check for responsive design
                if '@media' not in clean_code:
                    quality_issues.append("Missing responsive breakpoints")
                    
                if quality_issues:
                    self.logger.warning(f"⚠️ Quality issues in {page.name}: {', '.join(quality_issues)}")
                else:
                    self.logger.info(f"✅ Quality check passed for {page.name}")
                
                self.logger.info(f"✅ Generated {page.name}")
                
            except Exception as e:
                self.logger.error(f"❌ Failed to generate {page.name}: {str(e)}")
                page.error = str(e)
                # Generate a fallback page
                generated_pages[page.filepath] = self._create_fallback_page(page, project_plan.framework)
        
        return generated_pages
    
    async def generate_router(self, project_plan: ProjectPlan) -> str:
        """Generate router configuration"""
        try:
            # Load router templates
            router_sys = self._load_prompt_template("router/router-plan-sys.md")
            router_user = self._load_prompt_template("router/router-gen-user.md")
            
            # Create page routes
            page_routes = [
                {
                    "name": page.name,
                    "route": page.route,
                    "filepath": page.filepath
                }
                for page in project_plan.pages
            ]
            
            # Format user prompt
            router_filepath = "src/App.jsx" if project_plan.language == "JS" else "src/App.tsx"
            
            user_prompt = router_user.replace("{{FRAMEWORK}}", project_plan.framework) \
                                  .replace("{{LANGUAGE}}", project_plan.language) \
                                  .replace("{{PAGE_ROUTES}}", json.dumps(page_routes, indent=2)) \
                                  .replace("{{FILEPATH}}", router_filepath)
            
            # Add React-specific guidance
            if project_plan.framework.lower() == "react":
                user_prompt += """

Please provide the complete code within a standard code block like this:

```jsx
import React, { Suspense, lazy } from 'react';
import { Routes, Route, Link } from 'react-router-dom';

// Lazy-loaded page components
const HomePage = lazy(() => import('./pages/HomePage'));

function App() {
  return (
    <div className="app">
      <main>
        <Suspense fallback={<div>Loading...</div>}>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="*" element={<div>Page Not Found</div>} />
          </Routes>
        </Suspense>
      </main>
    </div>
  );
}

export default App;
```

IMPORTANT: DO NOT include BrowserRouter in App component!
"""
            
            # Generate router
            router_code = await self._call_llm(user_prompt, router_sys, temperature=0.2)
            
            # Save the raw response for debugging (following notebook logic)
            debug_response_path = os.path.join(settings.OUTPUT_PATH, "debug_router_response.md")
            os.makedirs(os.path.dirname(debug_response_path), exist_ok=True)
            with open(debug_response_path, "w", encoding="utf-8") as f:
                f.write(router_code)
            self.logger.info(f"Raw router response saved to {debug_response_path}")
            
            # Extract and clean code
            clean_code = self._extract_code_from_response(router_code, router_filepath)
            
            # Remove BrowserRouter if present (following notebook logic)
            if "BrowserRouter" in clean_code:
                clean_code = clean_code.replace("<BrowserRouter>", "").replace("</BrowserRouter>", "")
                self.logger.info("✅ Removed BrowserRouter from App component to prevent nested router errors")
            
            return clean_code
            
        except Exception as e:
            self.logger.error(f"Failed to generate router: {str(e)}")
            return self._create_fallback_router(project_plan)
    
    async def _call_llm(
        self,
        user_instruction: str,
        system_instruction: str,
        temperature: float = 0.0
    ) -> str:
        """Call Azure OpenAI API (following notebook logic)"""
        try:
            start_time = datetime.now()
            self.logger.info(f"Calling Azure OpenAI with {len(system_instruction)} chars system prompt and {len(user_instruction)} chars user prompt")
            
            conversation = [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_instruction}
            ]

            response = self.client.chat.completions.create(
                model=settings.AZURE_MODEL,
                messages=conversation,
                timeout=600,
                temperature=temperature
            )
            
            elapsed_time = (datetime.now() - start_time).total_seconds()
            self.logger.info(f"Azure OpenAI call completed in {elapsed_time:.2f} seconds")
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"Azure OpenAI API call failed: {str(e)}")
            raise
    
    def _load_prompt_template(self, relative_path: str) -> str:
        """Load prompt template from file"""
        full_path = os.path.join(settings.PROMPTS_PATH, relative_path)
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            self.logger.error(f"Failed to load template {full_path}: {str(e)}")
            return ""
    
    def _extract_code_from_response(self, response: str, filepath: str) -> str:
        """
        Extract code from markdown code block and clean it.
        Enhanced to handle multiple code block formats following notebook logic.
        """
        try:
            # Try multiple patterns for code extraction in order of preference
            
            # Pattern 1: Standard markdown code blocks with language identifier (```jsx, ```python, etc.)
            pattern1 = r"```(?:\w+)?\n(.*?)```"
            match1 = re.search(pattern1, response, re.DOTALL)
            
            # Pattern 2: Code blocks with no language identifier (just ```)
            pattern2 = r"```\n(.*?)```"
            match2 = re.search(pattern2, response, re.DOTALL)
            
            # Pattern 3: Any code block with or without language identifier
            pattern3 = r"```.*?\n(.*?)```"
            match3 = re.search(pattern3, response, re.DOTALL)
            
            # Pattern 4: Import statements as fallback (for identifying code without proper formatting)
            pattern4 = r"(?:^|\n)(import [^\n]+.*?(?:function|class|const|let|var).*?(?:export default|\}))"
            match4 = re.search(pattern4, response, re.DOTALL)
            
            # Try each pattern in sequence
            if match1:
                code = match1.group(1).strip()
                self.logger.info(f"Code extracted using pattern 1 (standard markdown code block)")
            elif match2:
                code = match2.group(1).strip()
                self.logger.info(f"Code extracted using pattern 2 (simple code block)")
            elif match3:
                code = match3.group(1).strip()
                self.logger.info(f"Code extracted using pattern 3 (any code block)")
            elif match4:
                code = match4.group(1).strip()
                self.logger.info(f"Code extracted using pattern 4 (import statements fallback)")
            else:
                self.logger.warning("No code block found, trying last resort extraction")
                
                # Last resort - try to extract any text that looks like code
                # Look for imports or typical code patterns
                potential_code_lines = []
                lines = response.split('\n')
                in_code_section = False
                
                for line in lines:
                    # Detect start of what might be code
                    if ('import ' in line or 'function ' in line or 'class ' in line or 
                        'const ' in line or 'let ' in line or 'var ' in line or 
                        line.strip().startswith('//') or line.strip().startswith('/*')):
                        in_code_section = True
                    
                    if in_code_section:
                        potential_code_lines.append(line)
                
                if potential_code_lines:
                    code = '\n'.join(potential_code_lines)
                    self.logger.warning(f"Used last resort code extraction - extracted {len(potential_code_lines)} lines that look like code")
                else:
                    raise ValueError("No code block found in the LLM response")
            
            # Perform framework-specific checks and fixes
            
            # For React files, ensure React is imported if JSX is used
            if filepath.endswith(('.jsx', '.tsx')) and 'import React' not in code and ('<' in code and '/>' in code):
                code = 'import React from "react";\n\n' + code
                self.logger.info(f"Added React import to {filepath} as JSX was detected")
            
            # For React router files, remove BrowserRouter if present
            if 'App.jsx' in filepath or 'App.tsx' in filepath:
                if '<BrowserRouter>' in code or '<Router>' in code:
                    code = code.replace('<BrowserRouter>', '').replace('</BrowserRouter>', '')
                    code = code.replace('<Router>', '').replace('</Router>', '')
                    self.logger.info(f"Removed BrowserRouter/Router from {filepath} to prevent nesting issues")
            
            return code
            
        except Exception as e:
            self.logger.error(f"Error extracting code from response: {str(e)}")
            # Return the response as-is as fallback
            return response
    
    def _get_ui_examples(self) -> str:
        """Get UI component examples (enhanced from notebook)"""
        return """

EXAMPLE COMPONENTS TO IMPLEMENT:

Hero Section:
```jsx
<section className="hero-section">
  <div className="hero-content">
    <h2>Discover Amazing Books</h2>
    <p>Find your next favorite read from our curated collection</p>
  </div>
  <img src="https://source.unsplash.com/random/600x400?library,books" className="hero-image" alt="Books" />
</section>
```

Search Bar:
```jsx
<div className="search-container">
  <input type="text" placeholder="Search books..." className="search-input" />
  <button className="btn-primary">
    <svg className="icon-svg" viewBox="0 0 24 24">
      <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
    </svg>
    Search
  </button>
</div>
```

Book Card:
```jsx
<div className="card">
  <img src="https://source.unsplash.com/random/300x450?book,novel" className="card-image" alt="Book cover" />
  <div className="card-content">
    <h3 className="card-title">Book Title</h3>
    <p className="card-description">Author Name</p>
    <div className="rating">
      <svg className="icon-svg" viewBox="0 0 24 24">
        <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
      </svg>
      4.5
    </div>
    <Link to="/book/1" className="btn-primary">View Details</Link>
  </div>
</div>
```
"""
    
    def _create_default_project_plan(self, user_prompt: str, framework: str, language: str) -> ProjectPlan:
        """Create a default project plan when generation fails"""
        return ProjectPlan(
            framework=framework,
            language=language,
            project_name="Default Project",
            description=f"Generated project based on: {user_prompt}",
            pages=[
                PageInfo(
                    name="HomePage",
                    filepath="src/pages/HomePage.jsx",
                    route="/",
                    description="Main landing page"
                )
            ]
        )
    
    def _create_fallback_page(self, page: PageInfo, framework: str) -> str:
        """Create a fallback page when generation fails"""
        return f"""import React from 'react';

const {page.name} = () => {{
  return (
    <div className="page-container">
      <header className="page-header">
        <h1>{page.name.replace('Page', '')}</h1>
        <p>Welcome to {page.name.replace('Page', '')} page</p>
      </header>
      
      <main className="page-content">
        <section className="content-section">
          <h2>Content</h2>
          <p>This page is under construction. Content will be available soon.</p>
        </section>
      </main>
      
      <style jsx>{{`
        .page-container {{
          min-height: 100vh;
          padding: 2rem;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
        }}
        
        .page-header {{
          text-align: center;
          margin-bottom: 2rem;
        }}
        
        .page-content {{
          max-width: 800px;
          margin: 0 auto;
        }}
        
        .content-section {{
          background: rgba(255, 255, 255, 0.1);
          padding: 2rem;
          border-radius: 12px;
          backdrop-filter: blur(10px);
        }}
      `}}</style>
    </div>
  );
}};

export default {page.name};
"""
    
    def _create_fallback_router(self, project_plan: ProjectPlan) -> str:
        """Create a fallback router when generation fails"""
        imports = []
        routes = []
        
        for page in project_plan.pages:
            component_name = page.name
            imports.append(f"const {component_name} = lazy(() => import('./pages/{component_name}'));")
            routes.append(f'            <Route path="{page.route}" element={{<{component_name} />}} />')
        
        return f"""import React, {{ Suspense, lazy }} from 'react';
import {{ Routes, Route }} from 'react-router-dom';

// Lazy-loaded page components
{chr(10).join(imports)}

const NotFound = () => (
  <div style={{{{ textAlign: 'center', padding: '2rem' }}}}>
    <h1>404 - Page Not Found</h1>
    <p>The page you are looking for does not exist.</p>
  </div>
);

function App() {{
  return (
    <div className="app">
      <main>
        <Suspense fallback={{<div>Loading...</div>}}>
          <Routes>
{chr(10).join(routes)}
            <Route path="*" element={{<NotFound />}} />
          </Routes>
        </Suspense>
      </main>
    </div>
  );
}}

export default App;
"""
