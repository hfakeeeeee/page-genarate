import os
import json
import logging
from datetime import datetime
from typing import Optional, Callable
from openai import AzureOpenAI

from app.config import settings
from app.models import SimpleProjectResult


class SimpleGeneratorService:
    def __init__(self):
        # Azure OpenAI configuration
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

    async def generate_complete_project(
        self,
        description: str,
        framework: str = "React",
        language: str = "JavaScript",
        progress_callback: Optional[Callable[[int, str], None]] = None
    ) -> SimpleProjectResult:
        """
        Generate a complete React project with AI freedom.
        Focused on React with JavaScript or TypeScript.
        """
        try:
            if progress_callback:
                progress_callback(10, "AI is analyzing your request...")

            # Create instruction with specific framework and language
            ultimate_instruction = self._create_ultimate_instruction(description, framework, language)

            if progress_callback:
                progress_callback(30, f"AI is designing the complete {framework} ({language}) solution...")

            # Single AI call to generate everything
            response = await self._call_llm(ultimate_instruction)

            if progress_callback:
                progress_callback(70, "AI is finalizing the project...")

            # Parse the AI's complete response
            project_result = self._parse_project_response(response)

            if progress_callback:
                progress_callback(90, "Project ready!")

            return project_result

        except Exception as e:
            self.logger.error(f"Failed to generate project: {str(e)}")
            raise

    def _create_ultimate_instruction(self, description: str, framework: str, language: str) -> str:
        """
        Create React-focused instruction that gives AI complete freedom within React ecosystem.
        """
        
        # Determine file extensions and imports based on language
        if language.lower() in ['typescript', 'ts']:
            file_ext = "tsx" if "component" in description.lower() else "ts"
            main_ext = "tsx"
            import_type = "TypeScript with proper type definitions"
            config_files = '''
    "tsconfig.json": "{\\"compilerOptions\\": {\\"target\\": \\"ES2020\\", \\"lib\\": [\\"DOM\\", \\"DOM.Iterable\\", \\"ES6\\"], \\"allowJs\\": false, \\"skipLibCheck\\": true, \\"esModuleInterop\\": false, \\"allowSyntheticDefaultImports\\": true, \\"strict\\": true, \\"forceConsistentCasingInFileNames\\": true, \\"moduleResolution\\": \\"bundler\\", \\"resolveJsonModule\\": true, \\"isolatedModules\\": true, \\"noEmit\\": true, \\"jsx\\": \\"react-jsx\\"}, \\"include\\": [\\"src\\"], \\"references\\": [{\\"path\\": \\"./tsconfig.node.json\\"}]}",'''
        else:
            file_ext = "jsx"
            main_ext = "jsx"
            import_type = "Modern JavaScript with ES6+ features"
            config_files = ""
        
        return f"""
You are a world-class React developer with unlimited creative freedom.

USER REQUEST: {description}
FRAMEWORK: {framework}
LANGUAGE: {language}

YOUR MISSION: Create a complete, modern, beautiful React application that fulfills this request perfectly.

MANDATORY REQUIREMENTS:
1. Create AT LEAST 5-8 files (not just App.{main_ext})
2. Build multiple functional React components
3. Use proper component structure and organization
4. Include styling for each component
5. Create a realistic, functional application

REACT-FOCUSED REQUIREMENTS:
- Use React 18+ with modern hooks and patterns
- Create a well-structured component hierarchy with MULTIPLE components
- Use {language} with proper {import_type}
- Include modern CSS with responsive design
- Follow React best practices and conventions
- Use appropriate React patterns (hooks, context, etc.)
- Create reusable components where appropriate

TECHNICAL SPECIFICATIONS:
- Framework: React (mandatory)
- Language: {language}
- Build Tool: Vite (for fast development)
- Styling: Modern CSS with CSS modules or styled-components
- File Extensions: .{main_ext} for components, .css for styles

COMPONENT CREATION GUIDELINES:
- Create specific, named components (not generic "ComponentName")
- Each component should have its own CSS file
- Build a proper component hierarchy
- Include at least 3-5 custom components beyond App
- Use meaningful file and component names
- Create functional, interactive components

DELIVERY FORMAT - CRITICAL:
Return ONLY valid JSON. Use proper escaping for strings. Create REAL component names, not placeholders.

Example structure (create your own real components):
{{
  "project_name": "descriptive-project-name",
  "framework": "React",
  "language": "{language}",
  "description": "What you actually built",
  "files": {{
    "package.json": "Complete package.json with React 18, Vite, and dependencies",
    "index.html": "Main HTML file with title matching the project",
    "vite.config.{file_ext.split('x')[0]}": "Vite configuration for React",{config_files}
    "src/main.{main_ext}": "React app entry point with ReactDOM.createRoot",
    "src/App.{main_ext}": "Main App component that uses other components",
    "src/App.css": "App component styles",
    "src/index.css": "Global styles and CSS reset",
    "src/components/Header.{main_ext}": "Header component example",
    "src/components/Header.css": "Header styles",
    "src/components/MainContent.{main_ext}": "Main content component",
    "src/components/MainContent.css": "Main content styles",
    "src/components/Footer.{main_ext}": "Footer component",
    "src/components/Footer.css": "Footer styles"
  }}
}}

CRITICAL JSON FORMATTING RULES:
- Ensure ALL backslashes in file content are properly escaped (use \\\\\\\\ instead of \\\\)
- Ensure ALL quotes in file content are properly escaped (use \\\\" instead of ")
- Each file content should be a valid JSON string value
- Do not include any text before or after the JSON object
- Make sure the JSON is valid and parseable

REACT COMPONENT GUIDELINES:
- Use functional components with hooks
- Include proper prop types or TypeScript interfaces
- Use modern React patterns (useState, useEffect, custom hooks)
- Create clean, readable, and well-organized code
- Include proper imports and exports
- Use semantic HTML and accessible components

CSS AND STYLING:
- Use modern CSS features (Grid, Flexbox, CSS Variables)
- Create responsive design that works on all devices
- Use meaningful class names and CSS organization
- Include hover effects and smooth animations
- Follow modern design principles

PROJECT STRUCTURE:
- Organize components logically in src/components/
- Use hooks/ folder for custom hooks
- Use utils/ folder for helper functions
- Keep styles modular and component-specific
- Include proper README and development setup

Create something amazing with React! Focus on clean code, great UX, and modern practices.

REMEMBER: The response must be ONLY valid JSON with proper escaping!
"""

    async def _call_llm(self, instruction: str) -> str:
        """Call Azure OpenAI with the ultimate instruction"""
        try:
            start_time = datetime.now()
            self.logger.info(f"Calling Azure OpenAI with ultimate instruction ({len(instruction)} chars)")

            response = self.client.chat.completions.create(
                model=settings.AZURE_MODEL,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a world-class developer with unlimited creative freedom. Create amazing web applications. IMPORTANT: Always return valid JSON with properly escaped strings."
                    },
                    {
                        "role": "user", 
                        "content": instruction
                    }
                ],
                timeout=600,
                temperature=0.8,  # Higher temperature for more creativity
            )

            elapsed_time = (datetime.now() - start_time).total_seconds()
            response_content = response.choices[0].message.content
            self.logger.info(f"Azure OpenAI call completed in {elapsed_time:.2f} seconds")
            self.logger.info(f"Response length: {len(response_content)} characters")
            
            # Log the first part of the response for debugging
            self.logger.debug(f"Response preview: {response_content[:500]}...")

            return response_content

        except Exception as e:
            self.logger.error(f"Azure OpenAI API call failed: {str(e)}")
            raise

    def _parse_project_response(self, response: str) -> SimpleProjectResult:
        """Parse the AI's response into a structured project"""
        try:
            # Try to extract JSON from the response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response[json_start:json_end]
            
            # Log the problematic JSON for debugging
            self.logger.debug(f"Attempting to parse JSON: {json_str[:500]}...")
            
            # Try to fix common JSON escape issues
            json_str = self._fix_json_escapes(json_str)
            
            project_data = json.loads(json_str)
            
            return SimpleProjectResult(
                project_name=project_data.get("project_name", "AI Generated Project"),
                framework=project_data.get("framework", "React"),
                language=project_data.get("language", "JavaScript"),
                description=project_data.get("description", "AI generated web application"),
                files=project_data.get("files", {})
            )
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON response: {str(e)}")
            self.logger.error(f"JSON error at position {e.pos}: {str(e)}")
            
            # Log problematic section for debugging
            start_pos = max(0, e.pos - 100)
            end_pos = min(len(json_str), e.pos + 100)
            problematic_section = json_str[start_pos:end_pos]
            self.logger.error(f"Problematic JSON section: {problematic_section}")
            
            # Log first 500 characters of the full JSON for context
            self.logger.debug(f"Full JSON preview: {json_str[:500]}...")
            
            # Try a more aggressive fix and retry
            try:
                fixed_json = self._aggressive_json_fix(json_str)
                project_data = json.loads(fixed_json)
                self.logger.info("Successfully parsed JSON after aggressive fix")
                return SimpleProjectResult(
                    project_name=project_data.get("project_name", "AI Generated Project"),
                    framework=project_data.get("framework", "React"),
                    language=project_data.get("language", "JavaScript"),
                    description=project_data.get("description", "AI generated web application"),
                    files=project_data.get("files", {})
                )
            except Exception as e2:
                self.logger.error(f"Aggressive fix also failed: {str(e2)}")
                # Fallback: create a minimal project
                return self._create_fallback_project()
        except Exception as e:
            self.logger.error(f"Failed to parse response: {str(e)}")
            return self._create_fallback_project()

    def _fix_json_escapes(self, json_str: str) -> str:
        """Fix common JSON escape issues that cause parsing errors"""
        
        # Simple but effective approach: fix the most common issues
        # 1. Replace Windows-style paths with forward slashes in keys
        # 2. Convert multiline string values to single line with proper escaping
        
        lines = json_str.split('\n')
        result_lines = []
        in_multiline_string = False
        current_multiline_content = []
        current_line_prefix = ""
        
        for line in lines:
            stripped = line.strip()
            
            # Skip empty lines
            if not stripped:
                continue
                
            # Check if this line starts a potential multiline string value
            if '": "' in stripped and not stripped.endswith('",') and not stripped.endswith('"'):
                # This might be starting a multiline string
                parts = stripped.split('": "', 1)
                if len(parts) == 2:
                    key_part = parts[0]
                    value_start = parts[1]
                    
                    # Fix backslashes in the key (file paths)
                    key_part = key_part.replace('\\', '/')
                    
                    # Start collecting multiline content
                    in_multiline_string = True
                    current_line_prefix = key_part + '": "'
                    current_multiline_content = [value_start]
                    continue
            
            # If we're in a multiline string, collect content until we find the end
            if in_multiline_string:
                if stripped.endswith('",') or stripped.endswith('"'):
                    # End of multiline string
                    if stripped.endswith('",'):
                        current_multiline_content.append(stripped[:-2])
                        suffix = '",'
                    else:
                        current_multiline_content.append(stripped[:-1])
                        suffix = '"'
                    
                    # Join all content and escape it properly
                    full_content = '\n'.join(current_multiline_content)
                    
                    # Escape the content for JSON
                    full_content = full_content.replace('\\', '\\\\')  # Escape backslashes
                    full_content = full_content.replace('"', '\\"')   # Escape quotes
                    full_content = full_content.replace('\n', '\\n')  # Escape newlines
                    full_content = full_content.replace('\r', '\\r')  # Escape carriage returns
                    full_content = full_content.replace('\t', '\\t')  # Escape tabs
                    
                    # Reconstruct the line
                    result_lines.append(current_line_prefix + full_content + suffix)
                    
                    # Reset state
                    in_multiline_string = False
                    current_multiline_content = []
                    current_line_prefix = ""
                else:
                    # Continue collecting multiline content
                    current_multiline_content.append(stripped)
                continue
            
            # Regular line processing
            if '": "' in stripped and (stripped.endswith('",') or stripped.endswith('"')):
                # Single line key-value pair
                parts = stripped.split('": "', 1)
                if len(parts) == 2:
                    key_part = parts[0]
                    value_part = parts[1]
                    
                    # Fix backslashes in the key
                    key_part = key_part.replace('\\', '/')
                    
                    # The value should already be properly formatted, but fix just in case
                    result_lines.append(key_part + '": "' + value_part)
                else:
                    result_lines.append(stripped)
            else:
                # Fix backslashes in keys that might be object keys
                if stripped.startswith('"') and '": {' in stripped:
                    result_lines.append(stripped.replace('\\', '/'))
                else:
                    result_lines.append(stripped)
        
        return '\n'.join(result_lines)
    
    def _aggressive_json_fix(self, json_str: str) -> str:
        """More aggressive JSON fixing for severely malformed JSON"""
        
        # Last resort: try to extract key-value pairs and reconstruct valid JSON
        try:
            # Look for the basic structure and extract what we can
            import re
            import json
            
            project_name = "AI Generated Project"
            framework = "React"
            language = "JavaScript"
            description = "AI generated web application"
            files = {}
            
            # Try to extract project_name
            name_match = re.search(r'"project_name":\s*"([^"]*)"', json_str)
            if name_match:
                project_name = name_match.group(1)
            
            # Try to extract framework
            framework_match = re.search(r'"framework":\s*"([^"]*)"', json_str)
            if framework_match:
                framework = framework_match.group(1)
            
            # Try to extract language
            language_match = re.search(r'"language":\s*"([^"]*)"', json_str)
            if language_match:
                language = language_match.group(1)
            
            # Extract description
            desc_match = re.search(r'"description":\s*"([^"]*)"', json_str)
            if desc_match:
                description = desc_match.group(1)
            
            # For files, create a simple default structure
            files = {
                "src/App.js": f"import React from 'react'; function App() {{ return <div><h1>{project_name}</h1></div>; }} export default App;",
                "package.json": f'{{"name": "{project_name.lower().replace(" ", "-")}", "version": "1.0.0", "dependencies": {{"react": "^18.0.0"}}}}'
            }
            
            # Construct valid JSON manually
            result = {
                "project_name": project_name,
                "framework": framework,
                "language": language,
                "description": description,
                "files": files
            }
            
            return json.dumps(result)
            
        except Exception:
            # If even this fails, return minimal valid JSON
            import json
            return json.dumps({
                "project_name": "Fallback Project",
                "framework": "React",
                "language": "JavaScript",
                "description": "Fallback project due to parsing errors",
                "files": {
                    "src/App.js": "import React from 'react'; function App() { return <div>Fallback App</div>; } export default App;"
                }
            })

    def _create_fallback_project(self) -> SimpleProjectResult:
        """Create a fallback project if AI response parsing fails"""
        return SimpleProjectResult(
            project_name="Fallback Project",
            framework="React",
            language="JavaScript",
            description="A simple fallback project",
            files={
                "package.json": '''{{
  "name": "fallback-project",
  "version": "1.0.0",
  "type": "module",
  "scripts": {{
    "dev": "vite",
    "build": "vite build"
  }},
  "dependencies": {{
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  }},
  "devDependencies": {{
    "@vitejs/plugin-react": "^4.0.0",
    "vite": "^4.4.0"
  }}
}}''',
                "index.html": '''<!DOCTYPE html>
<html>
<head>
    <title>Fallback Project</title>
</head>
<body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
</body>
</html>''',
                "src/main.jsx": '''import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'

ReactDOM.createRoot(document.getElementById('root')).render(<App />)''',
                "src/App.jsx": '''import React from 'react'

function App() {
  return (
    <div style={{padding: '2rem', textAlign: 'center'}}>
      <h1>Welcome to Your AI Generated Project!</h1>
      <p>This is a fallback project. The AI will create something much better!</p>
    </div>
  )
}

export default App'''
            }
        )
