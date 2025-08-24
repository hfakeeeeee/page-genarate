import os
import json
import re
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Callable
from openai import OpenAI

from ..config import settings
from ..models import ProjectPlan, PageInfo

class PageGeneratorService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
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
                
                # Extract and clean code
                clean_code = self._extract_code_from_response(page_code, page.filepath)
                
                generated_pages[page.filepath] = clean_code
                page.generated = True
                
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
            
            # Extract and clean code
            clean_code = self._extract_code_from_response(router_code, router_filepath)
            
            # Remove BrowserRouter if present
            if "BrowserRouter" in clean_code:
                clean_code = clean_code.replace("<BrowserRouter>", "").replace("</BrowserRouter>", "")
            
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
        """Call OpenAI API"""
        try:
            response = self.client.chat.completions.create(
                model=settings.MODEL,
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_instruction}
                ],
                temperature=temperature,
                timeout=600
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"OpenAI API call failed: {str(e)}")
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
        """Extract code from LLM response"""
        # Try multiple patterns
        patterns = [
            r"```(?:\w+)?\n(.*?)```",  # Standard code blocks
            r"```\n(.*?)```",         # Simple code blocks
            r"```.*?\n(.*?)```"       # Any code block
        ]
        
        for pattern in patterns:
            match = re.search(pattern, response, re.DOTALL)
            if match:
                code = match.group(1).strip()
                
                # Add React import if needed
                if filepath.endswith(('.jsx', '.tsx')) and 'import React' not in code and ('<' in code and '/>' in code):
                    code = 'import React from "react";\n\n' + code
                
                return code
        
        # Fallback: return the response as-is
        return response
    
    def _get_ui_examples(self) -> str:
        """Get UI component examples"""
        return """

EXAMPLE COMPONENTS TO IMPLEMENT:

Hero Section:
```jsx
<section className="hero-section">
  <div className="hero-content">
    <h2>Discover Amazing Content</h2>
    <p>Find what you're looking for in our collection</p>
  </div>
  <img src="https://source.unsplash.com/random/600x400?website" className="hero-image" alt="Hero" />
</section>
```

Search Bar:
```jsx
<div className="search-container">
  <input type="text" placeholder="Search..." className="search-input" />
  <button className="btn-primary">
    <svg className="icon-svg" viewBox="0 0 24 24">
      <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
    </svg>
    Search
  </button>
</div>
```

Card Component:
```jsx
<div className="card">
  <img src="https://source.unsplash.com/random/300x200?content" className="card-image" alt="Content" />
  <div className="card-content">
    <h3 className="card-title">Title</h3>
    <p className="card-description">Description</p>
    <Link to="/details/1" className="btn-primary">View Details</Link>
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
