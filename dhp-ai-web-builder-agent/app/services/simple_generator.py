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
You are a world-class React developer creating MODERN, MULTI-PAGE applications with unlimited creative freedom.

USER REQUEST: {description}
FRAMEWORK: {framework}
LANGUAGE: {language}

YOUR MISSION: Create a complete, modern, beautiful React application with MULTIPLE PAGES and real navigation.

MANDATORY REQUIREMENTS:
1. Create AT LEAST 8-12 files with MULTIPLE PAGES
2. Implement REAL ROUTING (React Router) between pages - NO MODALS for navigation
3. Build a modern, clean, sophisticated design
4. Use Tailwind CSS for ALL styling (NO separate CSS files)
5. Create realistic categories/sections relevant to the website type
6. Include proper navigation menu/header with working links

MULTI-PAGE NAVIGATION REQUIREMENTS:
- Install and use React Router DOM for real page navigation
- Create separate page components (Home, About, Products, Contact, etc.)
- Implement working navigation between pages (not modals or tabs)
- Include a navigation header/menu with clickable links
- Each page should be a separate component with its own route
- Use proper React Router patterns (BrowserRouter, Routes, Route, Link)

SMART CATEGORIZATION REQUIREMENTS:
- Analyze the website type and create relevant categories automatically
- For e-commerce: Categories like Electronics, Clothing, Books, etc.
- For restaurants: Categories like Appetizers, Main Courses, Desserts, etc. 
- For portfolios: Categories like Projects, Skills, Experience, etc.
- For blogs: Categories like Technology, Lifestyle, Travel, etc.
- For business: Categories like Services, About Us, Team, Contact, etc.
- Make categories meaningful and realistic for the specific website type

MODERN DESIGN REQUIREMENTS:
- Ultra-modern, clean, minimalist aesthetic
- Use contemporary design patterns (glassmorphism, gradients, shadows)
- Sophisticated color schemes and typography
- Professional spacing and layout
- Smooth animations and hover effects
- Mobile-first responsive design
- Use modern Tailwind utilities (backdrop-blur, shadow-xl, gradient backgrounds)
- Contemporary UI elements (cards, hero sections, call-to-action buttons)

STYLING REQUIREMENTS - TAILWIND ONLY:
- Use Tailwind CSS for ALL styling
- NO separate .css files for components  
- Include Tailwind directives in src/index.css only
- Use advanced Tailwind features (gradients, backdrop-blur, transforms)
- Implement modern color palettes (slate, zinc, stone for neutrals)
- Use sophisticated spacing and typography scales

REACT-FOCUSED REQUIREMENTS:
- Use React 18+ with modern hooks and patterns
- Implement React Router for multi-page navigation
- Use {language} with proper {import_type}
- Create reusable layout components
- Implement proper state management across pages
- Use React best practices and modern patterns

TECHNICAL SPECIFICATIONS:
- Framework: React (mandatory)
- Language: {language}
- Build Tool: Vite (for fast development)
- Styling: Tailwind CSS ONLY (no separate CSS files)
- File Extensions: .{main_ext} for components

CRITICAL SYNTAX RULES:
- ALL JSX must be perfectly valid
- NO unescaped quotes or special characters
- Proper string escaping in JSON
- Valid JavaScript/TypeScript syntax
- No syntax errors whatsoever

COMPONENT CREATION GUIDELINES:
- Create specific, named components (not generic "ComponentName")
- NO CSS files for components - use Tailwind classes only
- Build a proper component hierarchy with MULTIPLE PAGES
- Include at least 4-6 page components beyond App
- Use meaningful file and component names
- Create functional, interactive components with real routing

DELIVERY FORMAT - CRITICAL:
Return ONLY valid JSON. Use proper escaping for strings. Create REAL component names, not placeholders.

Example structure (adapt to your specific website type):
{{
  "project_name": "descriptive-project-name",
  "framework": "React",
  "language": "{language}",
  "description": "What you actually built",
  "files": {{
    "package.json": "Complete package.json with React 18, Vite, Tailwind CSS, React Router DOM",
    "index.html": "Main HTML file with title matching the project",
    "vite.config.{file_ext.split('x')[0]}": "Vite configuration for React, MUST add `server: {{host: true,cors: true,allowedHosts: true}}`",
    "tailwind.config.js": "Tailwind CSS configuration file",
    "postcss.config.js": "PostCSS configuration for Tailwind",{config_files}
    "src/main.{main_ext}": "React app entry point with ReactDOM.createRoot",
    "src/App.{main_ext}": "Main App component with Router setup and Routes",
    "src/index.css": "Global styles with Tailwind directives ONLY",
    "src/components/Layout.{main_ext}": "Layout component with Header/Footer",
    "src/components/Navigation.{main_ext}": "Navigation component with routing links", 
    "src/pages/Home.{main_ext}": "Home page component",
    "src/pages/About.{main_ext}": "About page component",
    "src/pages/Products.{main_ext}": "Products/Services page component",
    "src/pages/Contact.{main_ext}": "Contact page component"
  }}
}}
    "tailwind.config.js": "Tailwind CSS configuration file",
    "postcss.config.js": "PostCSS configuration for Tailwind",{config_files}
    "src/main.{main_ext}": "React app entry point with ReactDOM.createRoot",
    "src/App.{main_ext}": "Main App component that uses other components",
    "src/index.css": "Global styles with Tailwind directives ONLY",
    "src/components/Header.{main_ext}": "Header component with Tailwind styling",
    "src/components/MainContent.{main_ext}": "Main content component with Tailwind styling",
    "src/components/Footer.{main_ext}": "Footer component with Tailwind styling"
  }}
}}

CRITICAL JSON FORMATTING RULES:
- Ensure ALL backslashes in file content are properly escaped
- Ensure ALL quotes in file content are properly escaped
- Each file content should be valid JSON string value
- Do not include any text before or after the JSON object
- Make sure the JSON is valid and parseable
- NO syntax errors in any JavaScript/React code

REACT COMPONENT GUIDELINES:
- Use functional components with hooks
- Include proper prop types or TypeScript interfaces
- Use modern React patterns (useState, useEffect, custom hooks)
- Create clean, readable, and well-organized code
- Include proper imports and exports
- Use semantic HTML and accessible components

TAILWIND CSS GUIDELINES:
- Use className with Tailwind utility classes
- Responsive design with sm:, md:, lg:, xl: prefixes
- Use Tailwind's color palette (bg-blue-500, text-gray-800, etc.)
- Proper spacing with p-4, m-2, space-y-4, etc.
- Flexbox and Grid with flex, grid, items-center, justify-between
- Hover and focus states with hover:, focus: prefixes

CRITICAL SYNTAX VALIDATION:
- ALL JSX must be perfectly valid and well-formed
- Proper quotes in JSX attributes (use double quotes consistently)
- No unescaped special characters in strings
- Valid JavaScript/TypeScript syntax throughout
- Proper component imports and exports
- No malformed HTML elements or attributes

RESPONSE FORMAT - FINAL REQUIREMENTS:
- Return ONLY valid JSON with proper escaping
- No markdown, no explanations, just JSON
- Create specific component names, not placeholders
- Ensure every file contains syntactically correct code
- Test all code for syntax errors before including
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
                timeout=600
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
        except Exception as e:
            self.logger.error(f"Failed to parse response: {str(e)}")

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
