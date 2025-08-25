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
        progress_callback: Optional[Callable[[int, str], None]] = None
    ) -> SimpleProjectResult:
        """
        Generate a complete project with total AI freedom.
        No constraints, no rules, just pure creativity.
        """
        try:
            if progress_callback:
                progress_callback(10, "AI is analyzing your request...")

            # The ONE ultimate instruction - let AI decide everything
            ultimate_instruction = self._create_ultimate_instruction(description)

            if progress_callback:
                progress_callback(30, "AI is designing the complete solution...")

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

    def _create_ultimate_instruction(self, description: str) -> str:
        """
        The ONE ultimate instruction that gives AI complete freedom.
        No micro-management, no detailed constraints.
        """
        return f"""
You are a world-class full-stack developer and designer with unlimited creative freedom.

USER WANTS: {description}

YOUR MISSION: Create a complete, modern, beautiful web application that fulfills this request perfectly.

TOTAL CREATIVE FREEDOM:
- Choose ANY framework (React, Vue, Svelte, vanilla JS, etc.)
- Choose ANY language (JavaScript, TypeScript, etc.)
- Design ANY architecture you think is best
- Create ANY visual design that looks amazing
- Include ANY features that would make this great
- Use ANY modern web technologies and patterns
- Make ANY creative decisions that result in an outstanding product

DELIVERY FORMAT:
Return a JSON object with this structure:
{{
  "project_name": "YourChosenName",
  "framework": "YourChoice",
  "language": "YourChoice", 
  "description": "Brief description of what you created",
  "files": {{
    "package.json": "...",
    "index.html": "...",
    "src/main.js": "...",
    "src/App.vue": "...",
    "src/components/Component1.vue": "...",
    "src/style.css": "...",
    "any/other/files.js": "..."
  }}
}}

GUIDELINES:
- Make it BEAUTIFUL - use modern design principles
- Make it FUNCTIONAL - include real features, not just placeholders
- Make it COMPLETE - a fully working application
- Make it MODERN - use current best practices
- Be CREATIVE - surprise and delight
- Include realistic content and data
- Ensure it's responsive and accessible
- Use proper project structure for your chosen framework

Create something amazing. No limitations. No rules. Just pure excellence.
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
                        "content": "You are a world-class developer with unlimited creative freedom. Create amazing web applications."
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
            self.logger.info(f"Azure OpenAI call completed in {elapsed_time:.2f} seconds")

            return response.choices[0].message.content

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
            # Fallback: create a minimal project
            return self._create_fallback_project()
        except Exception as e:
            self.logger.error(f"Failed to parse response: {str(e)}")
            return self._create_fallback_project()

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
