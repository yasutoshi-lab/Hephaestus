"""Agent communication via tmux send-keys.

This module provides direct communication between agents by sending messages
to their tmux panes, similar to the Claude-Code-Communication reference implementation.
"""

import subprocess
import time
import logging
from pathlib import Path
from typing import Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)


class AgentCommunicator:
    """Handles agent-to-agent communication via tmux send-keys."""

    def __init__(self, session_name: str, work_dir: Path, agent_type: str = "claude"):
        """Initialize AgentCommunicator.

        Args:
            session_name: Name of the tmux session
            work_dir: Path to .hephaestus-work directory
            agent_type: Type of agent ('claude', 'gemini', 'codex')
        """
        self.session_name = session_name
        self.work_dir = work_dir
        self.agent_type = agent_type
        self.log_file = work_dir / "logs" / "communication.log"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)

        # Communication directory for Codex (file-based communication)
        self.comm_dir = work_dir / "communication"
        self.comm_dir.mkdir(parents=True, exist_ok=True)

    def get_pane_target(self, agent_name: str) -> Optional[str]:
        """Get tmux pane target for an agent.

        Args:
            agent_name: Agent name (master, worker-1, worker-2, etc.)

        Returns:
            Tmux pane target string (e.g., "hephaestus:0.0") or None if not found
        """
        try:
            # Map agent names to expected pane indices
            # Master is always pane 0, workers are panes 1, 2, 3, etc.
            agent_to_pane = {
                "master": 0
            }

            # Parse worker names like "worker-1", "worker-2", etc.
            if agent_name.startswith("worker-"):
                try:
                    worker_num = int(agent_name.split("-")[1])
                    agent_to_pane[agent_name] = worker_num
                except (IndexError, ValueError):
                    pass

            # If we have a direct mapping, use it
            if agent_name in agent_to_pane:
                pane_index = agent_to_pane[agent_name]
                return f"{self.session_name}:0.{pane_index}"

            # Fallback: Try to find by pane title (old method)
            result = subprocess.run(
                ["tmux", "list-panes", "-t", self.session_name, "-F", "#{pane_index}:#{pane_title}"],
                capture_output=True,
                text=True,
                check=True
            )

            # Parse output to find matching agent
            for line in result.stdout.strip().split("\n"):
                if ":" in line:
                    pane_index, pane_title = line.split(":", 1)
                    # Match agent name (case-insensitive)
                    if agent_name.lower() in pane_title.lower():
                        return f"{self.session_name}:0.{pane_index}"

            logger.warning(f"Agent {agent_name} not found in session {self.session_name}")
            return None

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to list panes: {e}")
            return None

    def send_message(self, target_agent: str, message: str, delay: float = 0.5) -> bool:
        """Send a message to an agent's chat pane.

        Uses tmux send-keys with agent-type specific flags:
        - Claude/Gemini: Standard send-keys (interprets key names)
        - Codex: send-keys -l (literal UTF-8 characters)

        Args:
            target_agent: Target agent name (e.g., "worker-1")
            message: Message to send
            delay: Delay between commands in seconds

        Returns:
            True if message was sent successfully, False otherwise
        """
        return self._send_message_via_tmux(target_agent, message, delay)

    def _send_message_via_tmux(self, target_agent: str, message: str, delay: float = 0.5) -> bool:
        """Send message via tmux send-keys.

        For Codex agents, uses -l flag for literal UTF-8 character input.
        For Claude/Gemini agents, uses standard send-keys.

        Args:
            target_agent: Target agent name
            message: Message to send
            delay: Delay between commands in seconds

        Returns:
            True if message was sent successfully
        """
        target = self.get_pane_target(target_agent)
        if not target:
            logger.error(f"Cannot send message: target agent {target_agent} not found")
            return False

        try:
            # Step 1: Clear any existing input with Ctrl+C (only for Claude/Gemini)
            if self.agent_type != "codex":
                subprocess.run(
                    ["tmux", "send-keys", "-t", target, "C-c"],
                    check=True
                )
                time.sleep(delay)

            # Step 2: Send the message
            if self.agent_type == "codex":
                # For Codex: Use -l flag for literal UTF-8 characters
                # This prevents interpretation of special characters and key names
                # No Ctrl+C needed as Codex composer handles input append
                subprocess.run(
                    ["tmux", "send-keys", "-l", "-t", target, message],
                    check=True
                )
            else:
                # For Claude/Gemini: Use standard send-keys
                subprocess.run(
                    ["tmux", "send-keys", "-t", target, message],
                    check=True
                )
            time.sleep(delay)

            # Step 3: Press Enter to execute
            subprocess.run(
                ["tmux", "send-keys", "-t", target, "Enter"],
                check=True
            )

            # Log the communication
            self._log_communication("master", target_agent, message)

            logger.info(f"Sent message to {target_agent} via tmux: {message[:50]}...")
            return True

        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to send message to {target_agent} via tmux: {e}")
            return False

    def _send_message_via_file(self, target_agent: str, message: str) -> bool:
        """Send message via file system (for Codex).

        Creates a message file that the target agent should monitor.

        Args:
            target_agent: Target agent name
            message: Message to send

        Returns:
            True if message file was created successfully
        """
        try:
            # Create agent-specific inbox directory
            inbox_dir = self.comm_dir / f"{target_agent}_inbox"
            inbox_dir.mkdir(parents=True, exist_ok=True)

            # Create timestamped message file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            message_file = inbox_dir / f"message_{timestamp}.md"

            # Write message to file
            with open(message_file, "w", encoding="utf-8") as f:
                f.write(f"# Message for {target_agent}\n\n")
                f.write(f"**From**: Master Agent\n")
                f.write(f"**Time**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"## Message Content\n\n")
                f.write(message)
                f.write("\n")

            # Log the communication
            self._log_communication("master", target_agent, f"[FILE] {message}")

            logger.info(f"Sent message to {target_agent} via file: {message_file}")
            return True

        except Exception as e:
            logger.error(f"Failed to send message to {target_agent} via file: {e}")
            return False

    def send_task_notification(self, target_agent: str, task_file: Path, comm_file: Path) -> bool:
        """Send task assignment notification to a worker.

        Args:
            target_agent: Target agent name (e.g., "worker-1")
            task_file: Path to task YAML file
            comm_file: Path to communication markdown file

        Returns:
            True if notification was sent successfully
        """
        # Create a concise notification message
        message = (
            f"New task assigned! Please read {comm_file.name} in the "
            f"communication/master_to_worker directory and execute the task."
        )

        return self.send_message(target_agent, message)

    def broadcast_to_workers(self, message: str, worker_count: int) -> int:
        """Broadcast a message to all workers.

        Args:
            message: Message to broadcast
            worker_count: Number of workers to send to

        Returns:
            Number of workers that received the message successfully
        """
        success_count = 0

        for i in range(1, worker_count + 1):
            worker_name = f"worker-{i}"
            if self.send_message(worker_name, message):
                success_count += 1

        return success_count

    def notify_master(self, worker_name: str, message: str) -> bool:
        """Send notification from worker to master.

        Args:
            worker_name: Name of the worker sending notification
            message: Notification message

        Returns:
            True if notification was sent successfully
        """
        return self.send_message("master", message)

    def _log_communication(self, from_agent: str, to_agent: str, message: str):
        """Log communication to file.

        Args:
            from_agent: Source agent name
            to_agent: Target agent name
            message: Message content
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {from_agent} -> {to_agent}: {message}\n"

        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except Exception as e:
            logger.warning(f"Failed to write communication log: {e}")

    def check_pane_active(self, agent_name: str) -> bool:
        """Check if an agent's pane is active and responsive.

        Args:
            agent_name: Agent name to check

        Returns:
            True if pane exists and is active
        """
        target = self.get_pane_target(agent_name)
        if not target:
            return False

        try:
            # Check if pane exists and is alive
            result = subprocess.run(
                ["tmux", "display-message", "-t", target, "-p", "#{pane_pid}"],
                capture_output=True,
                text=True,
                check=True
            )
            return bool(result.stdout.strip())
        except subprocess.CalledProcessError:
            return False

    def get_active_workers(self, worker_count: int) -> List[str]:
        """Get list of active workers.

        Args:
            worker_count: Expected number of workers

        Returns:
            List of active worker names
        """
        active_workers = []

        for i in range(1, worker_count + 1):
            worker_name = f"worker-{i}"
            if self.check_pane_active(worker_name):
                active_workers.append(worker_name)

        return active_workers
