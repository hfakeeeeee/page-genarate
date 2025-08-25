import os
import json
import re
import logging
from datetime import datetime
from typing import Dict, Optional, Callable
from openai import AzureOpenAI

from app.config import settings
from app.models import ProjectPlan, PageInfo


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
            system_prompt = self._load_prompt_template(
                "project/project-plan-sys.md"
            )

            # Create user prompt
            user_instruction = self._load_prompt_template(
                "project/project-plan-user.md"
              ).format(
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
                project_name=project_data.get("projectName",
                                              "Generated Project"),
                description=project_data.get("description",
                                             "AI Generated Web Application"),
                pages=pages
            )

        except Exception as e:
            self.logger.error(f"Failed to generate project plan: {str(e)}")
            # Return a default plan if generation fails
            return self._create_default_project_plan(user_prompt,
                                                     framework,
                                                     language)

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

                # Generate page
                page_code = await self._call_llm(user_prompt,
                                                 sys_prompt)

                # Save the raw response for debugging
                debug_response_path = os.path.join(
                    settings.OUTPUT_PATH,
                    f"debug_page_response_{page.name}.md")
                os.makedirs(os.path.dirname(debug_response_path),
                            exist_ok=True)
                with open(debug_response_path,
                          "w",
                          encoding="utf-8") as f:
                    f.write(page_code)
                self.logger.info(f"Raw page response for {page.name} \
                                 saved to {debug_response_path}")

                # Extract and clean code
                clean_code = self._extract_code_from_response(page_code,
                                                              page.filepath)

                generated_pages[page.filepath] = clean_code
                page.generated = True

                # Quality checks for modern UI requirements
                quality_issues = []

                # Check for React import
                if 'import React' not in clean_code:
                    quality_issues.append("Missing React import")

                if quality_issues:
                    self.logger.warning(
                        f"Quality issues in {page.name}: \
                        {', '.join(quality_issues)}")
                else:
                    self.logger.info(f"Quality check passed for {page.name}")

                self.logger.info(f"Generated {page.name}")

            except Exception as e:
                self.logger.error(f"Failed to generate {page.name}: {str(e)}")
                page.error = str(e)
                # Generate a fallback page
                generated_pages[page.filepath] = self._create_fallback_page(
                    page, project_plan.framework)

        return generated_pages

    async def generate_router(self, project_plan: ProjectPlan) -> str:
        """Generate router configuration"""
        try:
            # Load router templates
            router_sys = self._load_prompt_template(
                "router/router-plan-sys.md")
            router_user = self._load_prompt_template(
                "router/router-gen-user.md")

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
            if project_plan.language == "JS":
                router_filepath = "src/App.jsx"
            else:
                router_filepath = "src/App.tsx"

            user_prompt = router_user.replace(
                "{{FRAMEWORK}}", project_plan.framework).replace(
                "{{LANGUAGE}}", project_plan.language).replace(
                "{{PAGE_ROUTES}}", json.dumps(page_routes, indent=2)).replace(
                "{{FILEPATH}}", router_filepath)

            # Generate router
            router_code = await self._call_llm(user_prompt,
                                               router_sys)

            # Save the raw response for debugging (following notebook logic)
            debug_response_path = os.path.join(settings.OUTPUT_PATH,
                                               "debug_router_response.md")
            os.makedirs(os.path.dirname(debug_response_path), exist_ok=True)
            with open(debug_response_path, "w", encoding="utf-8") as f:
                f.write(router_code)
            self.logger.info(f"Raw router response \
                             saved to {debug_response_path}")

            # Extract and clean code
            clean_code = self._extract_code_from_response(router_code,
                                                          router_filepath)

            # Remove BrowserRouter if present (following notebook logic)
            if "BrowserRouter" in clean_code:
                clean_code = clean_code.replace("<BrowserRouter>", "").replace(
                    "</BrowserRouter>", "")

            return clean_code

        except Exception as e:
            self.logger.error(f"Failed to generate router: {str(e)}")
            return self._create_fallback_router(project_plan)

    async def _call_llm(
        self,
        user_instruction: str,
        system_instruction: str,
    ) -> str:
        """Call Azure OpenAI API (following notebook logic)"""
        try:
            start_time = datetime.now()
            self.logger.info(f"Calling Azure OpenAI with \
                              {len(system_instruction)} chars system prompt \
                              and {len(user_instruction)} chars user prompt")

            conversation = [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_instruction}
            ]

            response = self.client.chat.completions.create(
                model=settings.AZURE_MODEL,
                messages=conversation,
                timeout=600,
            )

            elapsed_time = (datetime.now() - start_time).total_seconds()
            self.logger.info(f"Azure OpenAI call completed in \
                             {elapsed_time:.2f} seconds")

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
        Enhanced to handle multiple code block following notebook logic.
        """
        try:

            # Pattern 1: Standard markdown code blocks with identifier
            pattern1 = r"```(?:\w+)?\n(.*?)```"
            match1 = re.search(pattern1, response, re.DOTALL)

            # Pattern 2: Code blocks with no language identifier (just ```)
            pattern2 = r"```\n(.*?)```"
            match2 = re.search(pattern2, response, re.DOTALL)

            # Pattern 3: Any code block with or without language identifier
            pattern3 = r"```.*?\n(.*?)```"
            match3 = re.search(pattern3, response, re.DOTALL)

            # Pattern 4: Import statements as fallback

            pattern4 = (
                r"(?:^|\n)"
                r"(import [^\n]+.*?"
                r"(?:function|class|const|let|var).*?"
                r"(?:export default|\}))"
            )
            match4 = re.search(pattern4, response, re.DOTALL)

            # Try each pattern in sequence
            if match1:
                code = match1.group(1).strip()
            elif match2:
                code = match2.group(1).strip()
            elif match3:
                code = match3.group(1).strip()
            elif match4:
                code = match4.group(1).strip()
            else:
                self.logger.warning("No code block found")

                # Last resort - try to extract any text that looks like code
                # Look for imports or typical code patterns
                potential_code_lines = []
                lines = response.split('\n')
                in_code_section = False

                for line in lines:
                    if (
                        'import ' in line
                        or 'function ' in line
                        or 'class ' in line
                        or 'const ' in line
                        or 'let ' in line
                        or 'var ' in line
                        or line.strip().startswith('//')
                        or line.strip().startswith('/*')
                    ):
                        in_code_section = True

                    if in_code_section:
                        potential_code_lines.append(line)

                if potential_code_lines:
                    code = '\n'.join(potential_code_lines)
                    self.logger.warning("Used last resort code extraction")
                else:
                    raise ValueError("No code block found in the LLM response")

            # Perform framework-specific checks and fixes

            # For React files, ensure React is imported if JSX is used
            if filepath.endswith(('.jsx', '.tsx')) \
                    and 'import React' not in code \
                    and ('<' in code and '/>' in code):
                code = 'import React from "react";\n\n' + code

            # For React router files, remove BrowserRouter if present
            if 'App.jsx' in filepath or 'App.tsx' in filepath:
                if '<BrowserRouter>' in code or '<Router>' in code:
                    code = code.replace('<BrowserRouter>', '').replace(
                        '</BrowserRouter>', '')
                    code = code.replace('<Router>', '').replace(
                        '</Router>', '')
                    self.logger.info("Removed BrowserRouter/Router")

            return code

        except Exception as e:
            self.logger.error(f"Error extracting code from response: {str(e)}")
            # Return the response as-is as fallback
            return response

    def _create_default_project_plan(self, user_prompt: str,
                                     framework: str,
                                     language: str) -> ProjectPlan:
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
