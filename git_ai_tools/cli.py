import click
import os
from .core import GitCommitAI

@click.group()
def cli():
    """Git AI Tools, a collection of ai-powered Git tools."""
    pass

@cli.command()
def commit():
    """Create a commit using AI-generated message from staged changes."""
    try:
        click.echo("🤔 Analyzing changes and generating commit message...")
        git_ai = GitCommitAI()
        suggestion = git_ai.suggest_commit(use_staged=True, use_last_commit=False)
        
        if suggestion.startswith("No"):  # Error message
            click.echo(suggestion)
            exit(1)
            
        click.echo("✨ Opening editor with the suggested message...")
        
        # Hand off to git commit with message and editor option
        os.execvp('git', ['git', 'commit', '-e', '-m', suggestion])
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        exit(1)

@cli.command()
@click.option('--staged/--unstaged', default=True, help='Use staged or unstaged changes')
@click.option('--last', is_flag=True, help='Use last commit instead of changes')
@click.option('--shorter', is_flag=True, help='Generate a shorter message')
@click.option('--longer', is_flag=True, help='Generate a more detailed message')
@click.argument('context', required=False)
def suggest(staged, last, shorter, longer, context):
    """Suggest a commit message with customizable options.
    
    You can provide additional context as a free-form argument:
    git ai suggest "make it focus on the security aspects"
    """
    try:
        git_ai = GitCommitAI()
        suggestion = git_ai.suggest_commit(
            use_staged=staged, 
            use_last_commit=last,
            style_hints={
                'shorter': shorter,
                'longer': longer,
                'context': context
            }
        )
        click.echo(suggestion)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        exit(1)

def main():
    cli()

if __name__ == "__main__":
    main() 