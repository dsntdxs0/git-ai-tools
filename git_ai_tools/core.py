import os
import requests
from git import Repo

class GitCommitAI:
    SUPPORTED_MODELS = ['openai', 'gemini', 'deepseek']
    
    API_ENDPOINTS = {
        'openai': 'https://api.openai.com/v1/chat/completions',
        'gemini': 'https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent',
        'deepseek': 'https://api.deepseek.com/chat/completions'
    }

    SYSTEM_PROMPT = (
        "You are a Git commit message generator that follows "
        "Conventional Commits format. You analyze relevant comments from the user and git diffs to create "
        "precise, meaningful commit messages. Always be concise and "
        "focus on the main changes. If the user provides additional context or requests a longer description, "
        "incorporate that into the commit message. Respond ONLY with the commit message unless the user explicitly asks for additional information."
    )

    def __init__(self):
        self.repo = Repo(os.getcwd())
        self.model = self._get_model_config()
        self.api_key = self._get_api_key(self.model)
        
        if not self.api_key:
            raise ValueError(
                f"API key not found for {self.model}. Please configure it using:\n"
                f"git config --global git-ai.{self.model}-key YOUR_API_KEY\n"
                f"Or set the {self.model.upper()}_API_KEY environment variable.\n\n"
                f"To change AI provider:\n"
                f"git config --global git-ai.ai-model [openai|gemini|deepseek]"
            )

    def _get_model_config(self):
        """Get the configured AI model from git config."""
        try:
            model = self.repo.git.config("--get", "git-ai.ai-model")
            if model and model.lower() in self.SUPPORTED_MODELS:
                return model.lower()
        except Exception:
            pass
        return 'openai'  # Default to OpenAI

    def _get_api_key(self, provider):
        """Get API key for the specified provider."""
        try:
            return self.repo.git.config("--get", f"git-ai.{provider}-key")
        except Exception:
            pass

        env_var_map = {
            'openai': 'OPENAI_API_KEY',
            'gemini': 'GEMINI_API_KEY',
            'deepseek': 'DEEPSEEK_API_KEY'
        }
        return os.getenv(env_var_map.get(provider))

    def get_changes(self, use_staged=True, use_last_commit=False):
        """Get either staged changes, unstaged changes, or last commit."""
        if use_last_commit:
            # Get the diff of the last commit
            try:
                return self.repo.git.show("HEAD", "--patch")
            except Exception:
                return None
        elif use_staged:
            # Get staged changes
            try:
                return self.repo.git.diff("--cached")
            except Exception:
                return None
        else:
            # Get unstaged changes
            if not self.repo.is_dirty():
                return None
            return self.repo.git.diff()

    def _call_api(self, prompt):
        """Make API call to the selected provider."""
        headers = {
            'Content-Type': 'application/json'
        }

        if self.model == 'openai':
            headers['Authorization'] = f'Bearer {self.api_key}'
            data = {
                'model': 'gpt-3.5-turbo',
                'messages': [
                    {
                        'role': 'system',
                        'content': self.SYSTEM_PROMPT
                    },
                    {'role': 'user', 'content': prompt}
                ],
                'max_tokens': 100,
                'temperature': 0.7
            }
        elif self.model == 'gemini':
            headers['Authorization'] = f'Bearer {self.api_key}'
            data = {
                'contents': [{
                    'parts': [{'text': prompt}]
                }]
            }
        elif self.model == 'deepseek':
            headers['Authorization'] = f'Bearer {self.api_key}'
            data = {
                'model': 'deepseek-chat',
                'messages': [
                    {
                        'role': 'system',
                        'content': self.SYSTEM_PROMPT
                    },
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 1.0,
                'max_tokens': 100,
                'stream': False
            }

        response = requests.post(
            self.API_ENDPOINTS[self.model],
            headers=headers,
            json=data
        )
        response.raise_for_status()
        return response.json()

    def _parse_response(self, response):
        """Parse API response based on provider."""
        if self.model == 'openai':
            return response['choices'][0]['message']['content'].strip()
        elif self.model == 'gemini':
            return response['candidates'][0]['content']['parts'][0]['text'].strip()
        elif self.model == 'deepseek':
            return response['choices'][0]['message']['content'].strip()

    def generate_commit_message(self, diff, style_hints=None):
        """Generate a commit message using the configured AI model."""
        if not diff:
            return None

        # Base prompt
        prompt = (
            "Generate a Git commit message based on relevant comments from the user, and following the Conventional Commits specification:\n"
            "1. Format: <type>(<scope>): <description>\n"
            "2. Types: feat, fix, docs, style, refactor, test, chore\n"
            "3. Scope is optional but encouraged\n"
            "4. Description should be:\n"
            "   - Imperative mood (e.g., 'add' not 'adds')\n"
            "   - No period at end\n"
            "   - Maximum 72 characters\n"
            "   - Clear and concise\n\n"
            "Consider the intent behind the changes and the overall impact of the modifications, in addition to the git diff provided.\n"
        )

        prompt += f"\nHere's the git diff to describe:\n\n{diff}\n\n"

        # Add style hints if provided
        if style_hints:
            if style_hints.get('shorter'):
                prompt += "Make the message very concise and brief. Respond ONLY with the commit message, nothing else.\n"
            elif style_hints.get('longer'):
                prompt += "Provide a more detailed description while still following the format. Respond ONLY with the commit message, nothing else.\n"
            
            if style_hints.get('context'):
                prompt += f"Consider the following additional context: {style_hints['context']}\n"

        # print(prompt)
        # print(style_hints)

        try:
            response = self._call_api(prompt)
            return self._parse_response(response)
        except requests.exceptions.RequestException as e:
            raise ValueError(f"API call failed: {str(e)}")

    def suggest_commit(self, use_staged=True, use_last_commit=False, style_hints=None):
        """Get changes and suggest a commit message."""
        diff = self.get_changes(use_staged, use_last_commit)
        if not diff:
            if use_last_commit:
                return "No last commit found."
            elif use_staged:
                return "No staged changes to commit."
            else:
                return "No changes to commit."

        commit_message = self.generate_commit_message(diff, style_hints)
        return commit_message 