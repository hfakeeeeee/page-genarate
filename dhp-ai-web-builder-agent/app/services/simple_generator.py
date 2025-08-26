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
            # Return fallback project instead of raising exception
            return self._create_fallback_project()

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
4. Use Tailwind CSS for ALL styling (NO separate CSS files)
5. Create a realistic, functional application

STYLING REQUIREMENTS - TAILWIND ONLY:
- Use Tailwind CSS for ALL styling
- NO separate .css files for components
- Include Tailwind directives in src/index.css only
- Use Tailwind classes directly in className attributes
- Follow Tailwind best practices for responsive design
- Use Tailwind's built-in colors, spacing, and utilities

REACT-FOCUSED REQUIREMENTS:
- Use React 18+ with modern hooks and patterns
- Create a well-structured component hierarchy with MULTIPLE components
- Use {language} with proper {import_type}
- Follow React best practices and conventions
- Use appropriate React patterns (hooks, context, etc.)
- Create reusable components where appropriate

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
    "package.json": "Complete package.json with React 18, Vite, Tailwind CSS dependencies",
    "index.html": "Main HTML file with title matching the project",
    "vite.config.{file_ext.split('x')[0]}": "Vite configuration for React",
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
        """Create a better fallback project with Tailwind CSS if AI response parsing fails"""
        return SimpleProjectResult(
            project_name="React Todo App",
            framework="React",
            language="JavaScript",
            description="A complete React todo application with Tailwind CSS (AI fallback)",
            files={
                "package.json": '''{
  "name": "react-todo-app",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.0.0",
    "vite": "^4.4.0",
    "tailwindcss": "^3.3.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0"
  }
}''',
                "index.html": '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>React Todo App</title>
</head>
<body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
</body>
</html>''',
                "vite.config.js": '''import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
})''',
                "tailwind.config.js": '''/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}''',
                "postcss.config.js": '''export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}''',
                "src/main.jsx": '''import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)''',
                "src/App.jsx": '''import React, { useState } from 'react'
import Header from './components/Header.jsx'
import TodoForm from './components/TodoForm.jsx'
import TodoList from './components/TodoList.jsx'

function App() {
  const [todos, setTodos] = useState([
    { id: 1, text: 'Fix Azure OpenAI API access', completed: false },
    { id: 2, text: 'Test multi-file generation', completed: false }
  ])

  const addTodo = (text) => {
    const newTodo = {
      id: Date.now(),
      text,
      completed: false
    }
    setTodos([...todos, newTodo])
  }

  const toggleTodo = (id) => {
    setTodos(todos.map(todo => 
      todo.id === id ? { ...todo, completed: !todo.completed } : todo
    ))
  }

  const deleteTodo = (id) => {
    setTodos(todos.filter(todo => todo.id !== id))
  }

  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="max-w-md mx-auto bg-white rounded-lg shadow-md p-6">
        <Header />
        <TodoForm onAdd={addTodo} />
        <TodoList todos={todos} onToggle={toggleTodo} onDelete={deleteTodo} />
      </div>
    </div>
  )
}

export default App''',
                "src/index.css": '''@tailwind base;
@tailwind components;
@tailwind utilities;''',
                "src/components/Header.jsx": '''import React from 'react'

function Header() {
  return (
    <header className="text-center mb-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-2">📝 Todo App</h1>
      <p className="text-red-600 font-semibold bg-yellow-100 p-3 rounded-lg border border-yellow-300">
        Note: This is a fallback project. Fix Azure OpenAI API for AI-generated projects!
      </p>
    </header>
  )
}

export default Header''',
                "src/components/TodoForm.jsx": '''import React, { useState } from 'react'

function TodoForm({ onAdd }) {
  const [text, setText] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (text.trim()) {
      onAdd(text.trim())
      setText('')
    }
  }

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 mb-6">
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Add a new todo..."
        className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
      />
      <button
        type="submit"
        className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
      >
        Add
      </button>
    </form>
  )
}

export default TodoForm''',
                "src/components/TodoList.jsx": '''import React from 'react'
import TodoItem from './TodoItem.jsx'

function TodoList({ todos, onToggle, onDelete }) {
  if (todos.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-500 italic">No todos yet. Add one above!</p>
      </div>
    )
  }

  return (
    <div className="space-y-2">
      {todos.map(todo => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onToggle={onToggle}
          onDelete={onDelete}
        />
      ))}
    </div>
  )
}

export default TodoList''',
                "src/components/TodoItem.jsx": '''import React from 'react'

function TodoItem({ todo, onToggle, onDelete }) {
  return (
    <div className={`flex items-center p-3 bg-white border rounded-lg shadow-sm ${todo.completed ? 'opacity-75' : ''}`}>
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={() => onToggle(todo.id)}
        className="mr-3 h-5 w-5 text-blue-600 rounded focus:ring-blue-500"
      />
      <span className={`flex-1 ${todo.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}>
        {todo.text}
      </span>
      <button
        onClick={() => onDelete(todo.id)}
        className="ml-3 px-3 py-1 text-sm bg-red-500 text-white rounded hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 transition-colors"
      >
        Delete
      </button>
    </div>
  )
}

export default TodoItem'''
            }
        )