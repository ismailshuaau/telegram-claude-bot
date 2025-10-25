"""
Bridge between Telegram and Claude Code
Manages Claude Code sessions and command execution
"""

import asyncio
import json
import os
import re
from typing import Dict, Optional, List
from datetime import datetime
import logging
from config import config

logger = logging.getLogger(__name__)


class ClaudeCodeSession:
    """Represents a Claude Code session"""

    def __init__(self, session_id: str, context: str, user_id: int):
        self.session_id = session_id
        self.context = context
        self.user_id = user_id
        self.working_dir = self._get_working_dir()
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
        self.history = []

    def _get_working_dir(self) -> str:
        """Get working directory based on context"""
        paths = {
            'backend': config.BACKEND_PATH,
            'frontend': config.FRONTEND_PATH,
            'root': config.PROJECT_ROOT,
        }
        return paths.get(self.context, config.PROJECT_ROOT)

    def update_activity(self):
        """Update last activity timestamp"""
        self.last_activity = datetime.now()

    def add_to_history(self, prompt: str, result: dict):
        """Add interaction to history"""
        self.history.append({
            'timestamp': datetime.now().isoformat(),
            'prompt': prompt,
            'result': result
        })


class ClaudeCodeBridge:
    """Bridge between Telegram and Claude Code"""

    def __init__(self):
        self.sessions: Dict[str, ClaudeCodeSession] = {}

    async def execute_command(
        self,
        user_id: int,
        prompt: str,
        context: str = "backend"
    ) -> dict:
        """Execute a Claude Code command"""

        session_id = f"{user_id}_{context}"

        # Get or create session
        session = self._get_or_create_session(session_id, context, user_id)
        session.update_activity()

        logger.info(f"Executing command for user {user_id} in context {context}: {prompt[:50]}...")

        try:
            # Execute the command
            result = await self._run_claude_code(session, prompt)

            # Add to history
            session.add_to_history(prompt, result)

            return result

        except Exception as e:
            logger.error(f"Error executing command: {str(e)}", exc_info=True)
            return {
                'success': False,
                'error': str(e),
                'output': f"❌ Error: {str(e)}"
            }

    def _get_or_create_session(
        self,
        session_id: str,
        context: str,
        user_id: int
    ) -> ClaudeCodeSession:
        """Get existing session or create new one"""

        if session_id not in self.sessions:
            logger.info(f"Creating new session: {session_id}")
            self.sessions[session_id] = ClaudeCodeSession(
                session_id, context, user_id
            )

        return self.sessions[session_id]

    async def _run_claude_code(
        self,
        session: ClaudeCodeSession,
        prompt: str
    ) -> dict:
        """Run Claude Code and capture results"""

        from config import BotConfig

        working_dir = session.working_dir
        auth_method = BotConfig.get_auth_method()

        logger.info(f"Using auth method: {auth_method}")

        try:
            if auth_method == 'cli':
                # Use Claude Code CLI (for users with Claude subscriptions)
                result = await self._call_claude_cli(prompt, working_dir)
            elif auth_method == 'api':
                # Use Anthropic API (for users with API keys)
                result = await self._call_claude_api(prompt, working_dir)
            else:
                raise Exception("No authentication method available")

            return result

        except Exception as e:
            logger.error(f"Execution failed: {str(e)}")
            # If one method fails, try the other as fallback
            if auth_method == 'cli':
                logger.info("CLI failed, trying API fallback...")
                try:
                    return await self._call_claude_api(prompt, working_dir)
                except:
                    raise e
            elif auth_method == 'api':
                logger.info("API failed, trying CLI fallback...")
                try:
                    return await self._call_claude_cli(prompt, working_dir)
                except:
                    raise e
            raise e

    async def _call_claude_api(self, prompt: str, working_dir: str) -> dict:
        """Call Claude API directly (preferred method)"""

        # This would use the Anthropic Python SDK
        # For now, simulating the response structure

        # Import Anthropic client
        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=config.ANTHROPIC_API_KEY)

            # Construct system prompt for coding context
            system_prompt = f"""You are a helpful coding assistant working in the directory: {working_dir}

You have access to the ChefVision Analytics Platform codebase, which includes:
- Django backend (transcription-platform/)
- React Native mobile app (expo-voice-analytics-mobile-app/)
- AWS infrastructure
- PostgreSQL database
- Redis cache
- Celery workers

When making changes:
1. Explain what you're doing
2. Show files that will be modified
3. Run relevant tests
4. Provide clear summaries

Format your response to be clear and actionable."""

            # Call Claude
            response = client.messages.create(
                model=config.CLAUDE_MODEL,
                max_tokens=4096,
                system=system_prompt,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            output = response.content[0].text

            # Parse output for structured data
            result = self._parse_claude_response(output, working_dir)

            return result

        except Exception as e:
            logger.error(f"Claude API call failed: {str(e)}")
            raise e

    async def _call_claude_cli(self, prompt: str, working_dir: str) -> dict:
        """Call Claude Code CLI (for users with Claude subscriptions)"""

        logger.info("Using Claude Code CLI")

        # Escape prompt for shell
        import shlex
        escaped_prompt = shlex.quote(prompt)

        # Execute command via subprocess
        cmd = f'cd {working_dir} && echo {escaped_prompt} | timeout {config.CLAUDE_TIMEOUT} claude-code --non-interactive 2>&1 || true'

        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()
        output = stdout.decode() + stderr.decode()

        return self._parse_claude_response(output, working_dir)

    def _parse_claude_response(self, output: str, working_dir: str) -> dict:
        """Parse Claude's response into structured format"""

        # Extract files changed
        files_changed = self._extract_files_changed(output, working_dir)

        # Extract test results
        tests_run = self._extract_test_results(output)

        # Check for errors
        has_error = bool(re.search(r'(error|exception|failed|traceback)', output, re.IGNORECASE))

        return {
            'success': not has_error,
            'output': output,
            'files_changed': files_changed,
            'tests_run': tests_run,
            'working_dir': working_dir,
            'timestamp': datetime.now().isoformat()
        }

    def _extract_files_changed(self, output: str, working_dir: str) -> List[str]:
        """Extract list of files that were modified"""

        files = []

        # Look for common patterns
        patterns = [
            r'(?:Created|Modified|Updated|Edited|Wrote):\s+([^\n]+)',
            r'File\s+["\']?([^\n"\']+)["\']?\s+(?:created|modified|updated)',
            r'Writing to\s+([^\n]+)',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, output, re.IGNORECASE)
            files.extend(matches)

        # Get actual git changes
        try:
            import subprocess
            result = subprocess.run(
                ['git', 'diff', '--name-only'],
                cwd=working_dir,
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                git_files = [f.strip() for f in result.stdout.split('\n') if f.strip()]
                files.extend(git_files)
        except Exception as e:
            logger.warning(f"Could not get git diff: {e}")

        # Remove duplicates and return
        return list(set(files))

    def _extract_test_results(self, output: str) -> dict:
        """Extract test execution results"""

        tests = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'ran': False
        }

        # pytest format
        pytest_match = re.search(
            r'(\d+)\s+passed(?:,\s+(\d+)\s+failed)?(?:,\s+(\d+)\s+skipped)?',
            output
        )
        if pytest_match:
            tests['ran'] = True
            tests['passed'] = int(pytest_match.group(1))
            tests['failed'] = int(pytest_match.group(2) or 0)
            tests['skipped'] = int(pytest_match.group(3) or 0)
            tests['total'] = tests['passed'] + tests['failed'] + tests['skipped']

        # Jest/npm test format
        jest_match = re.search(
            r'Tests:\s+(?:(\d+)\s+failed,\s+)?(\d+)\s+passed,\s+(\d+)\s+total',
            output
        )
        if jest_match:
            tests['ran'] = True
            tests['failed'] = int(jest_match.group(1) or 0)
            tests['passed'] = int(jest_match.group(2))
            tests['total'] = int(jest_match.group(3))
            tests['skipped'] = tests['total'] - tests['passed'] - tests['failed']

        return tests

    async def get_status(self, working_dir: str) -> dict:
        """Get project status"""

        status = {
            'git': await self._get_git_status(working_dir),
            'services': await self._get_services_status(),
            'tests': await self._get_last_test_status(working_dir),
        }

        return status

    async def _get_git_status(self, working_dir: str) -> dict:
        """Get git status"""

        try:
            process = await asyncio.create_subprocess_exec(
                'git', 'status', '--short',
                cwd=working_dir,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, _ = await process.communicate()
            output = stdout.decode().strip()

            # Parse status
            lines = output.split('\n') if output else []
            modified = len([l for l in lines if l.startswith(' M')])
            added = len([l for l in lines if l.startswith('A')])
            deleted = len([l for l in lines if l.startswith(' D')])
            untracked = len([l for l in lines if l.startswith('??')])

            return {
                'clean': len(lines) == 0,
                'modified': modified,
                'added': added,
                'deleted': deleted,
                'untracked': untracked,
                'output': output[:500] if output else 'No changes'
            }

        except Exception as e:
            logger.error(f"Git status failed: {e}")
            return {'error': str(e)}

    async def _get_services_status(self) -> dict:
        """Check if services are running"""

        services = {}

        # Check Django
        services['django'] = await self._check_port(8000)

        # Check Celery
        services['celery'] = await self._check_process('celery worker')

        # Check Redis
        services['redis'] = await self._check_port(6379)

        return services

    async def _check_port(self, port: int) -> bool:
        """Check if a port is open"""
        try:
            process = await asyncio.create_subprocess_exec(
                'lsof', f'-i:{port}',
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await process.communicate()
            return len(stdout) > 0
        except:
            return False

    async def _check_process(self, name: str) -> bool:
        """Check if a process is running"""
        try:
            process = await asyncio.create_subprocess_exec(
                'pgrep', '-f', name,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await process.communicate()
            return len(stdout) > 0
        except:
            return False

    async def _get_last_test_status(self, working_dir: str) -> dict:
        """Get last test run status"""
        # This would check for latest test output or run quick tests
        return {'status': 'unknown'}

    def cleanup_old_sessions(self, max_age_seconds: int = 3600):
        """Remove old inactive sessions"""

        now = datetime.now()
        to_remove = []

        for session_id, session in self.sessions.items():
            age = (now - session.last_activity).total_seconds()
            if age > max_age_seconds:
                to_remove.append(session_id)

        for session_id in to_remove:
            logger.info(f"Removing old session: {session_id}")
            del self.sessions[session_id]

        return len(to_remove)


# Global bridge instance
bridge = ClaudeCodeBridge()
