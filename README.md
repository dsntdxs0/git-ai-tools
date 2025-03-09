# Git AI Tools

A collection of AI-powered tools for Git, making your Git workflow eas.

Currently includes:

- Commit message generation
- Commit message suggestions
- Support for multiple AI providers:
  - [x] OpenAI
  - [x] Google Gemini
  - [x] DeepSeek
  - [ ] Claude

## Installation

Install directly from PyPI:

```bash
pip install git-ai-tools
```

Or install from source:

```bash
git clone https://github.com/Mik1337/git-ai-tools.git
cd git-ai-tools
pip install -e .
```

## Configuration

### 1. Choose your AI provider

You can choose between OpenAI (default), Gemini, or DeepSeek:

```bash
git config --global git-ai.ai-model openai  # or 'gemini' or 'deepseek'
```

### 2. Configure API Key

Set the API key for your chosen provider:

For OpenAI:

```bash
git config --global git-ai.openai-key "your-openai-api-key"
# or export OPENAI_API_KEY="your-openai-api-key"
```

For Gemini:

```bash
git config --global git-ai.gemini-key "your-gemini-api-key"
# or export GEMINI_API_KEY="your-gemini-api-key"
```

For DeepSeek:

```bash
git config --global git-ai.deepseek-key "your-deepseek-api-key"
# or export DEEPSEEK_API_KEY="your-deepseek-api-key"
```

## Available Commands

### Commit Messages

1. Quick commit with AI-generated message:

```bash
git add .              # Stage your changes
git ai commit          # Creates a commit with AI-generated message
```

2. Get commit message suggestions:

```bash
# Basic usage - suggests message for staged changes
git ai suggest

# Use unstaged changes instead
git ai suggest --unstaged

# Get suggestion for last commit (useful for amending)
git ai suggest --last

# Customize the message
git ai suggest --shorter          # Get a shorter message
git ai suggest --longer           # Get a more detailed message
git ai suggest "context here"     # Add custom context
```

#### Understanding the --last flag

The `--last` flag is used to generate a commit message based on your last commit's changes instead of the current changes in your working directory. This is particularly useful when:

- You want to improve/rewrite the message of your last commit
- You made a quick commit with a poor message and want a better suggestion
- You plan to amend your last commit and want a better message

Without `--last` (default behavior):

- The tool looks at your current changes (either staged or unstaged)
- Generates a commit message based on what you've modified

With `--last`:

- The tool looks at your most recent commit (HEAD)
- Shows what changes were made in that commit
- Generates a new commit message for those changes

Example workflow for improving your last commit:

```bash
# Get a suggestion for your last commit's changes
git ai suggest --last

# If you like the suggestion, amend your commit with the new message
git commit --amend -m "new message"
```

### Common Workflows

1. Normal commit workflow:

```bash
git add .
git ai commit
```

2. Review and edit suggestion before committing:

```bash
git add .
git ai suggest > msg.txt
$EDITOR msg.txt
git commit -F msg.txt
rm msg.txt
```

3. Amend last commit with better message:

```bash
git ai suggest --last
git commit --amend
```

4. Direct pipe to commit:

```bash
git ai suggest | git commit -F -
```

### Features

- [x] AI-powered commit message generation
- [x] Multiple AI provider support
- [x] Git plugin integration
- [x] Support for staged/unstaged changes
- [x] Support for amending commits
- [x] Customizable message style (shorter/longer)
- [x] Context-aware suggestions
- [ ] More AI-powered Git tools coming soon

### Requirements

- Python 3.8 or higher
- Git
- API key for your chosen AI provider

### Contributing

1. Fork the repository
2. Make your changes
3. Create a pull request

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
